import pytest
import os
from geovisio_cli import sequence, exception, model
from .conftest import FIXTURE_DIR, MOCK_API_URL
from pathlib import Path
from geopic_tag_reader import reader
import toml
import requests
from requests_mock import Adapter


@pytest.mark.parametrize(
    ("data", "method", "expected"),
    (
        (["1.jpg", "2.jpg", "3.jpg"], "filename-asc", ["1.jpg", "2.jpg", "3.jpg"]),
        (["3.jpg", "1.jpg", "2.jpg"], "filename-asc", ["1.jpg", "2.jpg", "3.jpg"]),
        (["3.jpg", "1.jpg", "2.jpeg"], "filename-asc", ["1.jpg", "2.jpeg", "3.jpg"]),
        (["10.jpg", "5.jpg", "1.jpg"], "filename-asc", ["1.jpg", "5.jpg", "10.jpg"]),
        (["C.jpg", "A.jpg", "B.jpg"], "filename-asc", ["A.jpg", "B.jpg", "C.jpg"]),
        (
            ["CAM1_001.jpg", "CAM2_002.jpg", "CAM1_002.jpg"],
            "filename-asc",
            ["CAM1_001.jpg", "CAM1_002.jpg", "CAM2_002.jpg"],
        ),
        (["1.jpg", "2.jpg", "3.jpg"], "filename-desc", ["3.jpg", "2.jpg", "1.jpg"]),
        (["3.jpg", "1.jpg", "2.jpg"], "filename-desc", ["3.jpg", "2.jpg", "1.jpg"]),
        (["3.jpg", "1.jpg", "2.jpeg"], "filename-desc", ["3.jpg", "2.jpeg", "1.jpg"]),
        (["10.jpg", "5.jpg", "1.jpg"], "filename-desc", ["10.jpg", "5.jpg", "1.jpg"]),
        (["C.jpg", "A.jpg", "B.jpg"], "filename-desc", ["C.jpg", "B.jpg", "A.jpg"]),
        (
            ["CAM1_001.jpg", "CAM2_002.jpg", "CAM1_002.jpg"],
            "filename-desc",
            ["CAM2_002.jpg", "CAM1_002.jpg", "CAM1_001.jpg"],
        ),
    ),
)
def test_sort_files_names(data, method, expected):
    dataPictures = [sequence.Picture(path=p) for p in data]
    resPictures = sequence._sort_files(dataPictures, method)
    assert expected == [pic.path for pic in resPictures]


@pytest.mark.parametrize(
    ("data", "method", "expected"),
    (
        (
            [["1.jpg", 1], ["2.jpg", 2], ["3.jpg", 3]],
            "time-asc",
            ["1.jpg", "2.jpg", "3.jpg"],
        ),
        (
            [["1.jpg", 2], ["2.jpg", 3], ["3.jpg", 1]],
            "time-asc",
            ["3.jpg", "1.jpg", "2.jpg"],
        ),
        (
            [["1.jpg", 1.01], ["2.jpg", 1.02], ["3.jpg", 1.03]],
            "time-asc",
            ["1.jpg", "2.jpg", "3.jpg"],
        ),
        (
            [["1.jpg", 1], ["2.jpg", 2], ["3.jpg", 3]],
            "time-desc",
            ["3.jpg", "2.jpg", "1.jpg"],
        ),
        (
            [["1.jpg", 2], ["2.jpg", 3], ["3.jpg", 1]],
            "time-desc",
            ["2.jpg", "1.jpg", "3.jpg"],
        ),
        (
            [["1.jpg", 1.01], ["2.jpg", 1.02], ["3.jpg", 1.03]],
            "time-desc",
            ["3.jpg", "2.jpg", "1.jpg"],
        ),
    ),
)
def test_sort_files_time(data, method, expected):
    dataPictures = []
    for p in data:
        name, ts = p
        m = reader.GeoPicTags(
            lon=47.7,
            lat=-1.78,
            ts=ts,
            heading=0,
            type="flat",
            make="Panoramax",
            model="180++",
            focal_length=4,
            crop=None,
        )
        dataPictures.append(sequence.Picture(path=name, metadata=m))

    resPictures = sequence._sort_files(dataPictures, method)
    assert expected == [pic.path for pic in resPictures]


def test_rw_sequence_toml(tmp_path):
    s = sequence.Sequence(
        title="SEQUENCE",
        id="blab-blabla-blablabla",
        path=str(tmp_path),
        pictures=[
            sequence.Picture(
                id="blou-bloublou-bloubloublou-1", path=str(tmp_path / "1.jpg")
            ),
            sequence.Picture(
                id="blou-bloublou-bloubloublou-2", path=str(tmp_path / "2.jpg")
            ),
            sequence.Picture(
                id="blou-bloublou-bloubloublou-3", path=str(tmp_path / "3.jpg")
            ),
        ],
        sort_method=sequence.SortMethod.time_desc,
    )
    res = sequence._write_sequence_toml(s)
    assert res == str(tmp_path / "_geovisio.toml")
    res2 = sequence._update_sequence_from_toml(sequence.Sequence(path=str(tmp_path)))
    assert s == res2
    assert res2.sort_method == sequence.SortMethod.time_desc


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
)
def test_read_sequence(datafiles):
    # First read : position is based on picture names
    seq = sequence._read_sequence(Path(datafiles))
    seqTomlPath = sequence._write_sequence_toml(seq)

    assert os.path.isfile(seqTomlPath)

    # Edit TOML file : position is inverted
    with open(seqTomlPath, "r+") as seqToml:
        editedSeqToml = seqToml.read()
        editedSeqToml = (
            editedSeqToml.replace("position = 1", "position = A")
            .replace("position = 2", "position = 1")
            .replace("position = A", "position = 2")
        )
        seqToml.seek(0)
        seqToml.write(editedSeqToml)
        seqToml.close()

        # Read sequence 2 : position should match edited TOML
        seq = sequence._read_sequence(Path(datafiles))
        assert seq.pictures[0].path.endswith("e2.jpg")
        assert seq.pictures[1].path.endswith("e1.jpg")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_read_sequence_invalid_file(datafiles):
    # Read sequence from files
    seq = sequence._read_sequence(Path(datafiles))
    seqTomlPath = sequence._write_sequence_toml(seq)

    assert os.path.isfile(seqTomlPath)

    # Check if invalid_pic is marked as broken
    with open(seqTomlPath, "r") as seqToml:
        seq2toml = seqToml.read()
        seq2 = sequence.Sequence()
        seq2.from_toml(toml.loads(seq2toml))
        assert len(seq2.pictures) == 4
        assert seq2.pictures[0].status == "broken-metadata"
        assert seq2.pictures[1].status is None
        assert seq2.pictures[2].status is None
        assert seq2.pictures[3].status is None


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
)
def test_read_sequence_sort_method_changed_set2unset(datafiles):
    # Write toml with sort method defined
    seq = sequence._read_sequence(
        Path(datafiles), sortMethod=sequence.SortMethod.time_desc
    )
    seqTomlPath = sequence._write_sequence_toml(seq)
    assert os.path.isfile(seqTomlPath)

    # Read sequence from toml without sort method = should reuse read one
    seq = sequence._read_sequence(Path(datafiles))
    assert seq.pictures[0].path.endswith("e2.jpg")
    assert seq.pictures[1].path.endswith("e1.jpg")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
)
def test_read_sequence_sort_method_changed_different(datafiles):
    # Write toml with sort method defined
    seq = sequence._read_sequence(
        Path(datafiles), sortMethod=sequence.SortMethod.time_desc
    )
    seqTomlPath = sequence._write_sequence_toml(seq)
    assert os.path.isfile(seqTomlPath)

    # Read sequence from toml without sort method = should reuse read one
    with pytest.raises(exception.CliException) as e:
        seq = sequence._read_sequence(
            Path(datafiles), sortMethod=sequence.SortMethod.filename_asc
        )

    assert e.match("Sort method passed as argument")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_no_valid_file(datafiles):
    with pytest.raises(exception.CliException) as e:
        seq = sequence._read_sequence(Path(datafiles))

    assert e.match("All read pictures have invalid metadata")


def mock_api_post_collection_fail(requests_mock):
    requests_mock.post(
        MOCK_API_URL + "/api/collections",
        exc=requests.exceptions.ConnectTimeout,
    )


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_collection_create_failure(requests_mock, datafiles):
    mock_api_post_collection_fail(requests_mock)

    with pytest.raises(exception.CliException) as e:
        sequence.upload(
            path=datafiles,
            geovisio=model.Geovisio(url=MOCK_API_URL),
            title="Test",
            alreadyBlurred=True,
        )

    assert str(e.value).startswith("Error while connecting to the API")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_upload_with_invalid_file(requests_mock, datafiles):
    # Put apart third picture
    os.rename(datafiles + "/e2.jpg", datafiles + "/e2.bak")
    os.rename(datafiles + "/e3.jpg", datafiles + "/e3.bak")

    # Mock collection creation
    gvsMock = model.Geovisio(url=MOCK_API_URL)
    seqId = "123456789"
    picId1 = "123"
    picId2 = "456"
    picId3 = "789"
    requests_mock.get(f"{MOCK_API_URL}/api", json={})
    requests_mock.get(f"{MOCK_API_URL}/api/configuration", json={})
    requests_mock.get(
        f"{MOCK_API_URL}/api/collections/{seqId}",
        json={"id": seqId, "title": "whatever"},
    )
    requests_mock.post(
        f"{MOCK_API_URL}/api/collections",
        json={"id": seqId},
        headers={"Location": f"{MOCK_API_URL}/api/collections/{seqId}"},
    )
    requests_mock.post(
        f"{MOCK_API_URL}/api/collections/{seqId}/items",
        json={"type": "Feature", "id": picId1},
        headers={"Location": f"{MOCK_API_URL}/api/collections/{seqId}/items/{picId1}"},
    )
    uploadReport = sequence.upload(path=Path(datafiles), geovisio=gvsMock, title=None)

    # Check previous pictures are OK
    assert len(uploadReport.uploaded_pictures) == 1
    assert len(uploadReport.errors) == 0

    # Make other pictures available
    os.rename(datafiles + "/e2.bak", datafiles + "/e2.jpg")
    os.rename(datafiles + "/e3.bak", datafiles + "/e3.jpg")
    with open(datafiles + "/_geovisio.toml") as f:
        seq = toml.loads(f.read())
        seq["pictures"]["e2.jpg"] = {"path": str(datafiles) + "/e2.jpg", "position": 2}
        seq["pictures"]["e3.jpg"] = {"path": str(datafiles) + "/e3.jpg", "position": 3}
        f.close()

    with open(datafiles + "/_geovisio.toml", "w") as f2:
        f2.write(toml.dumps(seq))
        f2.close()

        # Mock item call to fail
        requests_mock.post(
            f"{MOCK_API_URL}/api/collections/{seqId}/items",
            [
                {
                    "json": {"type": "Feature", "id": picId2},
                    "status_code": 202,
                    "headers": {
                        "Location": f"{MOCK_API_URL}/api/collections/{seqId}/items/{picId2}"
                    },
                },
                {"status_code": 500},
            ],
        )
        uploadReport2 = sequence.upload(
            path=Path(datafiles), geovisio=gvsMock, title=None
        )

        assert len(uploadReport2.uploaded_pictures) == 1
        assert len(uploadReport2.errors) == 1
