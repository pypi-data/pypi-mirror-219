# MIT License

# Copyright (c) 2023 MatrixEditor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

__all__ = [
    "IndexEntryType",
    "ISUHeader",
    "ISUDataField",
    "ISUArchiveIndexEntry",
    "ISUArchiveIndexFileEntry",
    "ISUArchiveIndexDirectoryEntry",
    "ISUArchiveIndex",
    "ISUArchive",
    "ISUDataField",
    "ISUDataSection",
    "ISU",
]

import typing as t
import io
import mmap
import enum
import construct as cs

from construct_dataclasses import dataclass_struct, csfield, tfield, subcsfield


# -- Enums -------------------------------------------------------------------
class IndexEntryType(enum.IntEnum):
    File = 0x00
    Directory = 0x01


# -- Adapters ----------------------------------------------------------------
class SpacePaddedString(cs.Adapter):
    def __init__(self, length):
        super().__init__(cs.PaddedString(length, "utf-8"))

    def _decode(self, obj: str, context, path):
        return obj.strip("\x20")

    def _build(self, obj: str, stream, context, path):
        padding = self.subcon.sizeof() - len(obj)
        self.subcon._build(obj + "\x20" * padding, stream, context, path)


class ArchiveIndexEntryAdapter(cs.Construct):
    def __init__(self):
        super().__init__()

    def _parse(self, stream, context, path):
        value = context.type
        if isinstance(value, cs.EnumIntegerString):
            value = value.intvalue

        if value == IndexEntryType.Directory:
            return ISUArchiveIndexDirectoryEntry.parser.parse_stream(stream)
        elif value == IndexEntryType.File:
            return ISUArchiveIndexFileEntry.parser.parse_stream(stream)
        else:
            raise cs.ValidationError(f"Invalid type: {value}", path)

    def _build(self, obj, stream, context, path):
        return obj.parser.build(obj)


# -- Structs -----------------------------------------------------------------
@dataclass_struct
class ISUHeader:
    magic: int = csfield(cs.Const(0x1176, cs.Int32ul))  # "76 11 00 00"
    length: int = csfield(cs.Int32ul)
    isu_version: int = csfield(cs.Int32ul)
    version: str = csfield(SpacePaddedString(32))
    customisation: str = csfield(SpacePaddedString(64))
    # We have to create a Conditional object here as these fields
    # are only present in FS2028 firmware binaries
    os_major_version: str | None = csfield(
        cs.If(cs.this.length == 0xA2, SpacePaddedString(6))
    )
    os_minor_version: str | None = csfield(
        cs.If(cs.this.length == 0xA2, SpacePaddedString(32))
    )
    uuid: bytes = csfield(cs.Bytes(16))


@dataclass_struct
class ISUDataField:
    length: int = csfield(cs.Int16ul)
    unknown_1: int = csfield(cs.Int16ul)
    name_length: int = csfield(cs.Int16ul)
    flags: int = csfield(cs.Int16ul)
    name: str = csfield(cs.PaddedString(cs.this.name_length, "utf-8"))
    value: int | None = csfield(cs.If(cs.this.length == 32, cs.Int32ul))
    unknown_2: int | None = csfield(cs.If(cs.this.length == 32, cs.Int32ul))


@dataclass_struct
class ISUArchiveIndexEntry:
    type: IndexEntryType = tfield(IndexEntryType, cs.Enum(cs.Int8ul, IndexEntryType))
    name_length: int = csfield(cs.Int8ul)
    name: str = csfield(cs.PaddedString(cs.this.name_length, "utf-8"))
    content: ISUArchiveIndexDirectoryEntry | ISUArchiveIndexFileEntry = csfield(
        ArchiveIndexEntryAdapter()
    )


@dataclass_struct
class ISUArchiveIndexFileEntry:
    size: int = csfield(cs.Int32ul)
    offset: int = csfield(cs.Int32ul)
    compressed_size: int = csfield(cs.Int32ul)

    def is_compressed(self) -> bool:
        return self.compressed_size != self.size


@dataclass_struct
class ISUArchiveIndexDirectoryEntry:
    entry_count: int = csfield(cs.Int8ul)
    entries: list[ISUArchiveIndexEntry] = subcsfield(
        ISUArchiveIndexEntry, cs.Array(cs.this.entry_count, ISUArchiveIndexEntry.struct)
    )


@dataclass_struct
class ISUArchiveIndex:
    length: int = csfield(cs.Int8ul)
    name: bytes = csfield(cs.Bytes(cs.this.length))  # always 0
    entry_count: int = csfield(cs.Int8ul)
    entries: list[ISUArchiveIndexEntry] = subcsfield(
        ISUArchiveIndexEntry, cs.Array(cs.this.entry_count, ISUArchiveIndexEntry.struct)
    )


@dataclass_struct
class ISUArchive:
    magic: bytes = csfield(cs.Const(b"FSH1"))
    size: int = csfield(cs.Int32ul)
    unknown_1: int = csfield(cs.Int16ul)
    index_size: int = csfield(cs.Int32ul)
    index: ISUArchiveIndex = csfield(ISUArchiveIndex)
    data: bytes = csfield(cs.Bytes(cs.this.size - cs.this.index_size - 4))


@dataclass_struct
class ISUDataField:
    length: int = csfield(cs.Int16ul)
    unknown_1: int = csfield(cs.Int16ul)
    name_length: int = csfield(cs.Int16ul)
    flags: int = csfield(cs.Int16ul)
    name: str = csfield(cs.PaddedString(16, "utf-8"))
    value: int | None = csfield(cs.If(cs.this.length == 32, cs.Int32ul))
    unknown_2: int | None = csfield(cs.If(cs.this.length == 32, cs.Int32ul))


@dataclass_struct
class ISUDataSection:
    magic: int = csfield(cs.Int8ul)
    length: int = csfield(cs.Int8ul)
    data: bytes = csfield(cs.Bytes(cs.this.length))


# -- Core Classes ------------------------------------------------------------
class it_data_fields:
    def __init__(self, isu: ISU) -> None:
        self.isu = isu
        self._fields = self._parse_fields()

    def _parse_fields(self) -> list[ISUDataField]:
        index = self.isu.stream.find(b"DecompBuffer")
        if index == -1:
            # Rather return empty list than raising an error
            return []

        index -= 8
        result = []
        while True:
            data_field = self.isu._create(ISUDataField, index)
            result.append(data_field)

            index += data_field.length
            # REVISIT: this is very unsafe
            if self.isu.stream[index] not in (0x20, 0x18):
                break

        return result

    def __iter__(self) -> t.Iterator[ISUDataField]:
        return iter(self._fields)

    def __getitem__(self, key: int | str) -> ISUDataField:
        if isinstance(key, str):
            for field in self._fields:
                if field.name == key:
                    return field

        elif isinstance(key, int):
            return self._fields[key]

        return None

    def __len__(self) -> int:
        return len(self._fields)


class isu_t(type):
    def __lshift__(cls, path: str) -> ISU:
        return ISU.parse_file(path)


class ISU(metaclass=isu_t):
    """Class to interact with binary ISU files.

    You can use this class to conveniently inspect ISU files. Regardless of the
    underlying file, the following attributes can be parsed:

    - header (:class:`ISUHeader`): the header of the parsed file
    - archive (:class:`ISUArchive`): if present, the stored directory archive
    - data_fields (list of :class:`ISUDataField`): A list of data fields that store various attributes

    :param stream: The memory map that stores the internal file data or an IOBase
                   object that supports the following modes: ``r+b`` and ``fileno()``.
    :type stream: IOBase or mmap

    Parse ISU Headers
    ~~~~~~~~~~~~~~~~~

    Note that each time you access the *header* attribute of an :class:`ISU` object,
    the header will be parsed again.

    >>> header = isu.header
    >>> header.customisation
    'ir-mmi-FS2026-0500-0795'

    Parse Directory Archives
    ~~~~~~~~~~~~~~~~~~~~~~~~

    As described in the :ref:`isu_firmware_structure` document, sometimes there is a
    directory archive that contains compressed and uncompressed files.

    >>> archive = isu.archive
    >>> for entry in archive.index.entries:
    ...     ... # inspect attributes here

    Parse Data Fields
    ~~~~~~~~~~~~~~~~~

    Data fields can be quite useful as they may define the size of the compressed/encrypted
    data block present in all ISU files. You can retrieve them using a property.

    >>> fields = isu.data_fields
    >>> if len(fields) > 0:
    ...     field = fields[0]
    ...     ... # inspect attributes here
    """

    def __init__(self, stream: io.IOBase | mmap.mmap) -> None:
        if isinstance(stream, io.IOBase):
            self.stream = mmap.mmap(stream.fileno(), 0)
        elif isinstance(stream, mmap.mmap):
            self.stream = stream
        else:
            raise TypeError(f"Expected mmap or IOBase - got {type(stream)}")

    @staticmethod
    def parse_file(name: str) -> ISU:
        """Opens the given file and prepares it for parsing.

        :param name: the path to an ISU file
        :type name: str
        :return: the created ISU instance
        :rtype: ISU
        """
        with open(name, "r+b") as fp:
            stream = mmap.mmap(fp.fileno(), 0)

        return ISU(stream)

    @property
    def header(self) -> ISUHeader:
        """Parses the header of an ISU file

        :return: the parsed header instance.
        :rtype: ISUHeader
        """
        return self._create(ISUHeader)

    @property
    def archive(self) -> ISUArchive | None:
        """Parses a stored directory archive if present.

        :return: the parsed archive; None otherwise
        :rtype: ISUArchive | None
        """
        index = self.stream.rfind(b"FSH1")
        if index == -1:
            return None

        return self._create(ISUArchive, index)

    @property
    def data_fields(self) -> it_data_fields:
        """Returns all data fields defined in the underlying ISU file.

        :return: an object storing all data fields.
        :rtype: it_data_fields
        """
        return it_data_fields(self)

    def get_data_section(self, index: int) -> ISUDataSection:
        """Parses a data section starting at the given index.

        :param index: the starting position (absolute)
        :type index: int
        :return: the parsed data section
        :rtype: ISUDataSection
        """
        return self._create(ISUDataSection, index)

    def get_archive_file(
        self, entry: ISUArchiveIndexFileEntry, archive: ISUArchive
    ) -> bytes:
        """Returns the file entry's data within the directory archive.

        :param entry: the data of a file entry
        :type entry: ISUArchiveIndexFileEntry
        :param archive: the directory archive instance
        :type archive: ISUArchive
        :return: the file's data (may be compressed)
        :rtype: bytes
        """
        if isinstance(entry, ISUArchiveIndexEntry):
            assert entry.type == IndexEntryType.File, "File entry required!"
            entry = entry.content

        # NOTE: The offset position is relative to the start of the archive header
        # without the magic bytes. So we have to remove the index size and additional
        # four bytes for the directory archive size field.
        offset = entry.offset - archive.index_size - 4
        size = entry.size
        if size != entry.is_compressed():
            # File is compressed
            size = entry.compressed_size

        return archive.data[offset : offset + size]

    # internal
    def _create(self, __class: t.Type[t._T], index=0) -> t._T:
        self.stream.seek(index, 0)
        return __class.parser.parse_stream(self.stream)
