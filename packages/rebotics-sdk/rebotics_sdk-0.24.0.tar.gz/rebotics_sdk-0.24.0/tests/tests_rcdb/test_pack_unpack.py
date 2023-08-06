import hashlib
import pathlib
import uuid

import numpy as np
import pytest

from rebotics_sdk.rcdb.entries import BaseEntry
from rebotics_sdk.rcdb.fields import StringField, FeatureVectorField, UUIDField, RemoteImageField, ImageField
from rebotics_sdk.rcdb.service import Packer, Unpacker


class RawEntry(BaseEntry):
    id = StringField()
    label = StringField(column_name='labels')
    feature_vector = FeatureVectorField()


class RawEntryWithNonsenseFields(BaseEntry):
    id = StringField()
    uuid = UUIDField()
    label = StringField(column_name='labels')
    feature_vector = FeatureVectorField()
    image_url = RemoteImageField()


def test_basic_packing(tmp_path):
    """Basic packing on the items that are provided"""
    test_data = {
        'id': '1',
        'label': 'test',
        'feature_vector': [1, 2, 3],
    }

    with Packer(tmp_path / 'test_file.rcdb', entry_type=RawEntry) as packer:
        packer.add_entry(RawEntry(**test_data))

    assert len(packer.metadata.files) == 1, 'Only one batch should be present'
    files = packer.metadata.files[0]
    assert files['id'] == 'id.txt', 'name should be set as a name of the field'
    assert files['label'] == 'labels.txt', 'filename is set in the field'
    assert files['feature_vector'] == 'features.txt', 'filename is set ' \
                                                      'because FeatureVectorField has a default column name'

    with Unpacker(tmp_path / 'test_file.rcdb', entry_type=RawEntry) as unpacker:
        for i, entry in enumerate(unpacker.entries()):
            assert entry.id == test_data['id'], entry.dict()
            assert entry.label == test_data['label']
            assert entry.feature_vector.tolist() == test_data['feature_vector']

    assert i == 0, "there should be only one entry"

    # test to autodetect what entry it is and what fields it may have
    with Unpacker(tmp_path / 'test_file.rcdb') as unpacker:
        for i, entry in enumerate(unpacker.entries()):
            assert entry.id == test_data['id'], entry.dict()
            assert entry.label == test_data['label']
            assert entry.feature_vector.tolist() == test_data['feature_vector']
    assert i == 0, "there should be only one entry"

    # test unpacker with nonsense fields
    with Unpacker(tmp_path / 'test_file.rcdb', entry_type=RawEntryWithNonsenseFields) as unpacker:
        i = 0
        for entry in unpacker.entries():
            i += 1
            assert entry.uuid is None
            assert entry.image_url is None

            # everything else should be setup properly
            assert entry.id == test_data['id'], entry.dict()
            assert entry.label == test_data['label']
            assert entry.feature_vector.tolist() == test_data['feature_vector']

            with pytest.raises(AttributeError):
                entry.vasya_pupkin  # noqa

        assert i == 1, "there should be only one entry"


def test_attributes_set():
    entry = RawEntry(id=123, label=123123, feature_vector=[1, 2, 3])
    assert entry.id == '123', 'transformation to_python should be called'
    assert entry.label == '123123'
    assert entry.feature_vector.tolist() == np.array([1, 2, 3], dtype=np.float32).tolist()  # noqa

    assert RawEntry.id.to_python(123) == '123'
    assert RawEntry.label.to_python(123) == '123'

    data = entry.dict()
    assert data['id'] == '123'
    assert data['label'] == '123123'
    assert data['feature_vector'].tolist() == np.array([1, 2, 3], dtype=np.float32).tolist()


def test_emtpy_entry():
    entry = RawEntry(id=None, label=None, feature_vector=None)
    assert entry.is_empty(), "this entry should be empty"
    entry = RawEntry(id=123, label=None, feature_vector=None)
    assert not entry.is_empty(), "this entry should not be empty"

    entry = RawEntry(id='', label='', feature_vector='')
    assert entry.is_empty(), "this entry should be empty because it is string empty"


def test_do_not_populate_all_fields_in_unpack(tmp_path):
    """Test if we don't populate one of the fields, it should be None"""
    with Packer(tmp_path / 'test_file_not_all_fields.rcdb', entry_type=RawEntry) as packer:
        packer.add_entry(RawEntry(id=123, label=123123, feature_vector=None))

    with Unpacker(tmp_path / 'test_file_not_all_fields.rcdb', entry_type=RawEntry) as unpacker:
        for entry in unpacker.entries():
            assert entry.id == '123'
            assert entry.label == '123123'
            assert entry.feature_vector is None


def test_unknown_field_attributes():
    with pytest.raises(AttributeError):
        _ = RawEntry.id.vasya_pupkin  # noqa


def test_known_field_attributes():
    assert RawEntry.id.column_name == 'id'
    assert RawEntry.label.column_name == 'labels'
    assert RawEntry.feature_vector.column_name == 'features'
    assert RawEntry.id.extension == 'txt'
    assert RawEntry.label.extension == 'txt'
    assert RawEntry.feature_vector.extension == 'txt'
    assert RawEntry.id.text_wrap
    assert RawEntry.id.text_wrap
    assert RawEntry.id.text_wrap


def test_unpack_mjhd_960(script_cwd: pathlib.Path):
    """Try to read an existing rcdb file generated by CORE on mjhd_960 example from r3us-admin"""
    rcdb_file = script_cwd / 'mjhd_960.rcdb'
    assert rcdb_file.exists()
    with Unpacker(rcdb_file) as unpacker:
        metadata = unpacker.get_metadata()
        assert metadata.packer_version == 1
        assert metadata.count == 254, 'There are 254 feature vectors with images'

        assert unpacker.entry_type is not None, "After reading metadata, entry type should be populated"
        assert unpacker.entry_type.options.fields

        assert 'image' in unpacker.entry_type.options.fields, 'There should be an image field in the entry type'

        for i, entry in enumerate(unpacker.entries()):
            if i == 0:
                # do assert statements only for the first entry
                assert len(entry.feature_vector.tolist()) == 512, \
                    "Check that there is at least a feature vector with correct number of features"
                assert entry.image is not None, "The image can be read automatically " \
                                                "without specifying in the entry type"

        assert i == 254 - 1, "After reading all entries, the total count should be 254, starting from 0"


class ImageEntry(BaseEntry):
    label = StringField(column_name='labels')
    feature_vector = FeatureVectorField(column_name='features')
    image = ImageField(column_name='images')


def test_unpack_mjhd_960_with_image(script_cwd: pathlib.Path):
    rcdb_file = script_cwd / 'mjhd_960.rcdb'
    assert rcdb_file.exists()

    with Unpacker(rcdb_file, entry_type=ImageEntry) as unpacker:
        metadata = unpacker.get_metadata()
        assert metadata.packer_version == 1
        for entry in unpacker.entries():
            assert entry.label is not None
            assert entry.feature_vector is not None
            assert entry.image is not None
            break


def test_pack_with_images_image(tmp_path, script_cwd):
    image_path = script_cwd / '..' / 'db' / 'custom_folder' / 'image_1.png'
    with Packer(tmp_path / 'test_file.rcdb', entry_type=ImageEntry) as packer:
        packer.add_entry(ImageEntry(label="123123", feature_vector=[1, 2, 3], image=image_path))

    with open(image_path, 'rb') as fio:
        image_hash = hashlib.md5(fio.read()).hexdigest()

    with Unpacker(tmp_path / 'test_file.rcdb', entry_type=ImageEntry) as unpacker:
        for entry in unpacker.entries():
            assert entry.label == "123123"
            assert entry.feature_vector.tolist() == [1, 2, 3]
            assert entry.image is not None
            image_hash_2 = hashlib.md5(entry.image.read()).hexdigest()
            assert image_hash == image_hash_2, "Two images in archive and out archive should have the same hash"


def test_batching(tmp_path):
    batch_size = 10
    with Packer(tmp_path / 'test_file.rcdb', entry_type=RawEntry, batch_size=batch_size) as packer:
        for i in range(100):
            packer.add_entry(RawEntry(id=i, label=i, feature_vector=[i, i, i]))

    assert packer.entries_count == 100, 'There should be 100 entries'
    assert packer.batch_counter == 11, 'There should be 10 batches'
    assert len(packer.metadata.files) == 10, 'There should be 10 batches'

    with Unpacker(tmp_path / 'test_file.rcdb', entry_type=RawEntry) as unpacker:
        i = 0
        for i, entry in enumerate(unpacker.entries()):
            if i == 0:
                assert entry.id == str(i), entry.dict()
                assert entry.label == str(i)
                assert entry.feature_vector.tolist() == [i, i, i]

        assert i == 100 - 1, "there should be only 100 entries"


def test_pack_and_unpack_vrcdb_file(tmp_path):
    class VRCDBEntry(BaseEntry):
        label = StringField(column_name='labels')
        feature_vector = FeatureVectorField()
        uuid = UUIDField()
        image_url = RemoteImageField()

    packer = Packer(
        tmp_path / 'test_file.rcdb', entry_type=VRCDBEntry,
    )
    packer.metadata.packer_version = 2  # force overwrite of the version

    with packer:
        packer.add_entry(VRCDBEntry(
            label='123',
            feature_vector=[1, 2, 3],
            uuid='123e4567-e89b-12d3-a456-426655440000',
            image_url='https://example.com/image.jpg',
        ))

    unpacker = Unpacker(tmp_path / 'test_file.rcdb')  # open without entry type
    with unpacker:
        i = 0
        for entry in unpacker.entries():
            i += 1
            assert entry.label == '123'
            assert entry.feature_vector.tolist() == [1, 2, 3]
            assert entry.uuid == uuid.UUID('123e4567-e89b-12d3-a456-426655440000'), "Should automatically detect UUID"
            assert entry.image_url == 'https://example.com/image.jpg'

            with pytest.raises(AttributeError):
                # id is never populated
                _ = entry.id  # noqa

        assert i == 1, "there should be only one entry"
        assert unpacker.metadata.packer_version == 2, "version should be 2 as it is set in packer"
        assert sorted(unpacker.fields.keys()) == sorted(['label', 'feature_vector', 'uuid', 'image_url'])

    unpacker = Unpacker(tmp_path / 'test_file.rcdb', entry_type=VRCDBEntry)  # open with entry type
    with unpacker:
        i = 0
        for entry in unpacker.entries():
            i += 1
            assert entry.label == '123'
            assert entry.feature_vector.tolist() == [1, 2, 3]
            assert entry.uuid == uuid.UUID('123e4567-e89b-12d3-a456-426655440000'), \
                "Because there is a formatting to UUID field"
            assert entry.image_url == 'https://example.com/image.jpg'

            with pytest.raises(AttributeError):
                _ = entry.roga_kopyta  # noqa

        assert i == 1, "there should be only one entry"
        assert sorted(unpacker.fields.keys()) == sorted(['label', 'feature_vector', 'uuid', 'image_url'])
