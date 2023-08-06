from est.io.utils.url import build_spec_data_url, split_spec_url_elmts
from silx.io.url import DataUrl


def test_spec_url():
    """simple test of the spec url function class"""
    file_path = "test.dat"
    scan_title = "1.1"
    col_name = "energy"
    data_slice = None
    url = build_spec_data_url(
        file_path=file_path,
        scan_title=scan_title,
        col_name=col_name,
        data_slice=data_slice,
    )
    assert isinstance(url, DataUrl)
    assert split_spec_url_elmts(url) == {
        "file_path": file_path,
        "scan_title": scan_title,
        "col_name": col_name,
        "data_slice": data_slice,
    }
