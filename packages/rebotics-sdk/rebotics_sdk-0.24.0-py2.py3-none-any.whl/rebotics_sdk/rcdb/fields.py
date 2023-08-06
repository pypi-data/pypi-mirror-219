import io
import pathlib
import typing
import uuid

import numpy as np

if typing.TYPE_CHECKING:
    from rebotics_sdk.rcdb.entries import BaseEntry
    from rebotics_sdk.rcdb.service import Unpacker, Packer


class DeferredAttribute:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        data = instance.__dict__
        field_name = self.field.name
        if field_name not in data:
            # something wrong happened here and BaseEntry.init gone wrong
            raise ValueError(f'Field {field_name} is not initialized.')
        return data[field_name]

    def __getattr__(self, item):
        if hasattr(self.field, item):
            return getattr(self.field, item)
        raise AttributeError(f'Field {self.field.name} has no attribute {item}')

    def __set__(self, instance, value):
        data = instance.__dict__
        field_name = self.field.name

        if value is EMPTY_FIELD:
            data[field_name] = None
            return

        data[field_name] = self.field.to_python(value)


class BaseField:
    descriptor_class = DeferredAttribute
    column_name: str = None
    name: typing.Optional[str] = None
    extension: str = 'txt'
    text_wrap = True

    def __init__(self, *, column_name=None, extension=None):
        self.name = None
        self.base_entry = None

        if extension is not None:
            self.extension = extension

        if column_name is not None:
            self.column_name = column_name

    def contribute_to_class(self, cls: typing.Type['BaseEntry'], name):
        self.name = name
        self.base_entry = cls

        if self.column_name is None:
            # if the column name is still None, use the name attribute
            self.column_name = name

        # here is the magic shenanigans that we need to do
        cls.options.add_field(name, self)  # noqa
        setattr(cls, self.name, self.descriptor_class(self))

    def read_from_rcdb(self, *, index: int, descriptor: io.IOBase, unpacker: 'Unpacker'):
        if descriptor is None:
            return None
        return self.to_python(descriptor.readline())

    def write_to_rcdb(self, value, *, index, descriptor, packer: 'Packer'):
        descriptor.write(self.to_rcdb(value))

    def to_python(self, value):
        return value

    def to_rcdb(self, value):
        return f'{value}\n'

    def get_filename(self, batch_number=None):
        if batch_number is None:
            return f'{self.column_name}.{self.extension}'
        return f'{self.column_name}_{batch_number}.{self.extension}'

    def wrap_descriptor(self, descriptor):
        if self.text_wrap:
            return io.TextIOWrapper(descriptor)
        else:
            return descriptor


class EmptyField(BaseField):
    def contribute_to_class(self, cls: typing.Type['BaseEntry'], name):
        pass


EMPTY_FIELD = EmptyField()


class StringField(BaseField):
    # no changes
    def to_rcdb(self, value):
        return f"{value}\n"

    def to_python(self, value):
        if isinstance(value, bytes):
            value = value.decode()
            value.strip()
        return str(value).strip()


class FeatureVectorField(BaseField):
    column_name = 'features'

    def __init__(self, dtype=np.float32, length=512, **kwargs):
        super().__init__(**kwargs)
        self.dtype = dtype
        self.length = length

    def to_python(self, value):
        # convert from str or binary to List[float]
        # assume that internal representation of the field is a List[float]
        if isinstance(value, (str, bytes)):
            if isinstance(value, bytes):
                value = value.decode()

            value = value.strip().strip('[]')
            if value == '':
                return None
            return np.fromstring(value, dtype=self.dtype, sep=',')
        return np.array(value, dtype=self.dtype)

    def to_rcdb(self, value):
        if value is None:
            return ''

        # convert from List[float] to str or binary
        rendered_string = ','.join(map(str, value))
        # maybe code it to ascii??
        # or better to binary later on
        return f"{rendered_string}\n"


class RemoteImageField(StringField):
    """A file with image urls in the same order as the entries."""
    column_name = 'images'


class ImageField(StringField):
    column_name = 'images'
    text_wrap = True

    def read_from_rcdb(self, index: int, descriptor: io.IOBase, unpacker: 'Unpacker'):
        if descriptor is None:
            if not unpacker.metadata.images:
                return None
            # assume it is a proper index and string
            # surely support images that we have in the metadata
            # in other words support packer version 1
            try:
                image_name = unpacker.metadata.images[index]
                image_name = f'images/{image_name}'
            except IndexError:
                return None  # we reached the end of the file
        else:
            image_name = self.to_python(descriptor.readline())  # load string properly

        if not image_name:
            return None
        return unpacker.archive.read(image_name)

    def write_to_rcdb(self, value: typing.Union[str, pathlib.Path],
                      *, index, descriptor, packer: 'Packer'):
        arcname = f"images/{pathlib.Path(value).name}"
        if descriptor is None:
            if not packer.metadata.images:
                return
            packer.metadata.images[index] = arcname
        else:
            super().write_to_rcdb(arcname, index=index, descriptor=descriptor, packer=packer)
        packer.archive.write(value, arcname)

    def to_python(self, value):
        if hasattr(value, 'read'):
            return value
        return super().to_python(value)

    def wrap_descriptor(self, descriptor):
        if descriptor is None:
            return None
        return super().wrap_descriptor(descriptor)


class UUIDField(StringField):
    column_name = 'uuid'

    def to_python(self, value):
        value = super().to_python(value)
        return uuid.UUID(value) if value else None

    def to_rcdb(self, value):
        value = super().to_rcdb(value)
        if value is None:
            return ''
        if isinstance(value, uuid.UUID):
            value = value.hex
        return value


def detect_field_class_by_name(name: str) -> typing.Type[BaseField]:
    if name in ('feature_vector', 'features', 'fv'):
        return FeatureVectorField
    if name in ('image', 'images'):
        return RemoteImageField
    if name in ('uuid', 'uuids'):
        return UUIDField
    return StringField
