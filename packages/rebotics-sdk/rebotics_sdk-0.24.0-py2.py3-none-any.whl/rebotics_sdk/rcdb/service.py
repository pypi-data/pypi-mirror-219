import json
import pathlib
import tempfile
import typing

from pydantic import BaseModel

import rebotics_sdk
from rebotics_sdk.constants import RCDBBaseFileNames
from rebotics_sdk.rcdb.archivers import BaseArchiver, detect_archiver, ArchiveFacade, ZipArchiver
from rebotics_sdk.rcdb.entries import BaseEntry, EntryBuilder
from rebotics_sdk.rcdb.fields import detect_field_class_by_name, StringField, FeatureVectorField, RemoteImageField, \
    UUIDField, BaseField, ImageField

ETV = typing.TypeVar('ETV', bound=BaseEntry)


class Metadata(BaseModel):
    packed: typing.Optional[str] = None  # datetime of packing in %c format
    model_type: typing.Optional[str] = None
    model_codename: typing.Optional[str] = None
    sdk_version: typing.Optional[str] = rebotics_sdk.__version__
    core_version: typing.Optional[str] = None
    fvm_version: typing.Optional[str] = None
    packer_version: typing.Optional[int] = 0
    count: int = 0
    images_links_expiration: typing.Optional[str] = None  # iso data format

    additional_files: typing.Optional[typing.List[str]] = None  # additional files in archive
    images: typing.Optional[typing.List[str]] = None  # images in archive

    # new field for metadata
    files: typing.List[dict] = []


class BasePackerInterface:
    @property
    def fields(self):
        return self.entry_type.options.fields


class Packer(BasePackerInterface):
    """
    new packer method to add files to a RCDB archive via generator.

    usage example:

    >>> class RawEntry(BaseEntry):
    >>>     id = StringField()
    >>>     label = StringField(column_name='labels')
    >>>     feature_vector = FeatureVectorField()
    >>>
    >>> archiver = ZipArchiver(compression=zipfile.ZIP_STORED)  # no compression
    >>> with Packer('test_file.rcdb', entry_type=RawEntry, archiver=archiver) as packer:
    >>>     packer.add_entry(RawEntry(**test_data))
    """
    version = 4
    extension = 'rcdb'
    archive: typing.Optional[ArchiveFacade]

    tmp_folder_path: typing.Optional[pathlib.Path]

    def __init__(self, output_file: typing.Union[pathlib.PurePath, str],
                 entry_type: typing.Type[BaseEntry],
                 archiver: BaseArchiver = None,
                 batch_size: int = None,
                 **metadata):

        self.output_file = pathlib.Path(output_file)

        if self.output_file.suffix[1:] != self.extension:
            # or change the output_file extension to .rcdb
            raise ValueError(f"Output file must have {self.extension} extension")

        self.entry_type = entry_type

        self.metadata = Metadata(**metadata)
        self.metadata.packer_version = self.version

        self.batch_size = batch_size  # default behavior is to write all entries at once
        self.batch_counter = 0

        if not archiver:
            # use default archiver to be zipfile
            archiver = ZipArchiver()

        if self.batch_size is not None and not archiver.supports_batching:
            raise ValueError(f"Archiver {archiver.__class__.__name__} does not support batching")

        self.archiver = archiver
        self.archive = None
        self.temporary_folder = None
        self.tmp_folder_path = None

        self.column_descriptors = {}
        self.entries_count = 0
        self.per_batch_counter = 0

    def add_entry(self, entry: BaseEntry):
        # Check that entry is of the type that user requested
        # Convert entry to the format that is required by
        fields = self.entry_type.options.fields

        for field_name, field in fields.items():
            value = getattr(entry, field_name)
            field.write_to_rcdb(value,
                                index=self.entries_count,
                                descriptor=self.column_descriptors[field_name],
                                packer=self)
            self.per_batch_counter += 1

        self.entries_count += 1

        if self.batch_size is not None:
            if self.entries_count % self.batch_size == 0:
                self._flush_into_archive()
                self.per_batch_counter = 0

    def __enter__(self):
        self.archive = self.archiver.open_for_write(self.output_file)
        # open a temporary descriptors to store column entities for each field from the entry_type
        self.temporary_folder = tempfile.TemporaryDirectory()
        self.tmp_folder_path = pathlib.Path(self.temporary_folder.name)
        self._create_file_descriptors()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Fill meta.json with
        #  - User-provided data
        #  - entries count
        #  - fields that are available in entries and their types
        # Close files, pack archive

        if exc_type is None:
            self.metadata.count = self.entries_count
            self._flush_into_archive(recreate_descriptors=False)

            # we can read additionally size of the archive and populate the metadata as well

            # flush metadata file
            with open(self.tmp_folder_path / 'meta.json', 'w') as fio:
                json.dump(self.metadata.dict(), fio)
            self.archive.write(self.tmp_folder_path / 'meta.json', RCDBBaseFileNames.META)

        self.archive.close()
        self.temporary_folder.cleanup()

    def _create_file_descriptors(self):
        for field_name, field in self.fields.items():
            self.column_descriptors[field_name] = open(self.tmp_folder_path / field.column_name, 'w')

    def _flush_into_archive(self, recreate_descriptors=True):
        """with given column descriptors, write down """
        for field_name, descriptor in self.column_descriptors.items():
            descriptor.close()

        if self.batch_size is not None:
            self.batch_counter += 1
        else:
            self.batch_counter = None

        batched_files = {}

        if self.per_batch_counter > 0:
            # Do not write empty files into an archive
            for field_name, field in self.fields.items():
                archive_name = field.get_filename(self.batch_counter)
                self.archive.write(
                    self.tmp_folder_path / field.column_name,
                    archive_name
                )
                batched_files[field_name] = archive_name
            self.metadata.files.append(batched_files)

        if recreate_descriptors:
            # recreate descriptors for the next batch
            self._create_file_descriptors()


class Unpacker(BasePackerInterface):
    """
    New type of unpackers that can support older versions of RCDB
    When entry_type is not defined, it is automatically detected from the metadata.json.
    The only exception being is for the ImageField, which is ambiguous and cannot be detected

    Example of usage:
    >>> with Unpacker('test_file.rcdb') as unpacker:
    >>>     for entry in unpacker.entries():
    >>>         print(entry)
    """
    version = 4
    archive: typing.Optional[ArchiveFacade]

    def __init__(self, input_file: typing.Union[str, pathlib.PurePath],
                 entry_type: typing.Optional[typing.Type[BaseEntry]] = None,
                 archiver: BaseArchiver = None,
                 ):
        """
        :param entry_type: defines the field set that user requests for extraction.
          If it's None, only RCDB meta could read.
        """
        self.input_file = pathlib.Path(input_file)

        # when entry_type is None, we might just unpack all fields that are available in RCDB
        # in terms of string format first
        self.entry_type = entry_type
        if archiver is None:
            archiver_class = detect_archiver(input_file)
            archiver = archiver_class()
        self.archiver = archiver
        self.archive = None
        self.metadata = None
        self.column_descriptors = {}

        self.batch_counter = 0

    def get_metadata(self) -> Metadata:
        """
        Get meta without opening the archive to check it or get fields format.
        """
        if self.archive is None:
            raise ValueError("Archive is not opened. Use 'with' statement to open it first")
        self.metadata = Metadata(**json.load(
            self.archive.read(RCDBBaseFileNames.META)
        ))

        if self.entry_type is None:
            self._resolve_fields_for_packer_version()

        return self.metadata

    def _resolve_fields_for_packer_version(self):
        # create a class with fields that are available in metadata
        # check if we have files in metadata
        # if yes, then we need to read them to get the format of the fields
        entry_builder = EntryBuilder()

        if self.metadata.packer_version == self.version:
            for field_name, filename in self.metadata.files[0].items():
                # read the first file and try to detect the format
                column_name, ext = filename.split('.')
                field_cls = detect_field_class_by_name(field_name)

                entry_builder.add_field(field_name, field_cls(extension=ext, column_name=column_name))

            self.entry_type = entry_builder.build()
            return self.entry_type

        # need to list all files in archive and try to initialize entry_type
        # or try to read predefined files that we can actually find and read
        # default available fields across all versions
        entry_builder.add_field('label', StringField(extension='txt', column_name='labels'))
        entry_builder.add_field('feature_vector', FeatureVectorField(extension='txt', column_name='features'))

        if self.metadata.packer_version == 1:
            if self.metadata.images:
                # need to read arcnames for images and create ImageField
                entry_builder.add_field('image', ImageField())

        if self.metadata.packer_version == 2:
            # this means it is an archive with RemoteImageField
            entry_builder.add_field('image_url', RemoteImageField())
            entry_builder.add_field('uuid', UUIDField())

        if self.metadata.packer_version == 3:
            # read additional files from meta to find known usages
            for arcname, _ in self.metadata.additional_files:
                if 'features_uuid' in arcname:
                    # found in CORE at common.classification.actions
                    entry_builder.add_field('uuid', UUIDField(column_name='features_uuid'))

        # single batch with multiple files
        self.entry_type = entry_builder.build()
        self.metadata.files = [self.entry_type.get_field_to_filename_map()]
        return self.entry_type

    def entries(self) -> typing.Iterable[ETV]:
        """
        Iterate over entries in RCDB. Required archive to be opened
        """
        if self.archive is None:
            raise ValueError("Archive is not opened. Use 'with' statement to open it first")

        if self.metadata is None:
            self.get_metadata()

        entry_index = 0

        if len(self.metadata.files) == 0:
            # read with available fields
            return

        if not self.archiver.supports_batching and len(self.metadata.files) > 1:
            raise ValueError(f"Archive {self.archiver} does not support batching.")

        # there are batches to be read
        for batch in self.metadata.files:
            self.batch_counter += 1

            files = batch.values()
            self._close_column_descriptors()

            file_descriptors = self.archive.read_batch(files)  # filename: IO

            for field_name, archive_name in batch.items():
                # open descriptors for each file
                field: 'BaseField' = self.fields[field_name]
                self.column_descriptors[field_name] = field.wrap_descriptor(file_descriptors[archive_name])

            entry_kwargs = {}

            while True:
                # for lines in files...
                for field_name, field in self.fields.items():
                    descriptor = self.column_descriptors.get(field_name)
                    entry_kwargs[field_name] = field.read_from_rcdb(index=entry_index,
                                                                    descriptor=descriptor,
                                                                    unpacker=self)

                entry = self.entry_type(**entry_kwargs)
                if entry.is_empty():
                    # we reached full empty row
                    break
                yield entry
                entry_index += 1
        return

    def _close_column_descriptors(self):
        if self.column_descriptors:
            for descriptor in self.column_descriptors.values():
                if descriptor is not None:
                    descriptor.close()

    def __enter__(self):
        """
        Open an archive. Get meta first to get a field set with the typings.
        If packed RCDB contains more fields that are not defined in entry_type -
        they would be ignored and not extracted.
        If packed RCDB misses some fields, or they have a different type than requested, raise an error.
        """
        if self.archive is None:
            self.archive = self.archiver.open_for_read(self.input_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close_column_descriptors()
        self.archive.close()
