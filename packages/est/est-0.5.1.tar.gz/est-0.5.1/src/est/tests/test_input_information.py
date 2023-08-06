from est.io.utils.information import InputInformation
from est.app.utils.xasobj import get_xas_obj
from est.io.utils import url as url_utils
from est.io.utils.url import build_spec_data_url, split_spec_url_elmts
from silx.io.url import DataUrl

try:
    import PyMca5
except ImportError:
    PyMca5 = None

import pytest


@pytest.mark.skipif(PyMca5 is None, reason="PyMca5 is not installed")
def test_input_information(filename_cu_from_pymca):
    """Test providing urls to spec files"""
    input_information = InputInformation(
        channel_url=url_utils.build_spec_data_url(
            file_path=filename_cu_from_pymca,
            scan_title=None,
            col_name="Column 1",
            data_slice=None,
        ),
        spectra_url=url_utils.build_spec_data_url(
            file_path=filename_cu_from_pymca,
            scan_title=None,
            col_name="Column 2",
            data_slice=None,
        ),
    )
    xas_obj = get_xas_obj(input_information)
    assert xas_obj.energy is not None
    assert xas_obj.spectra.data.flat[0] is not None


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
