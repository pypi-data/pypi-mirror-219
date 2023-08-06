import numpy
import pytest
from silx.io.url import DataUrl

try:
    import larch
except ImportError:
    larch = None

from ewokscore.missing_data import MISSING_DATA
from est.io.utils.information import InputInformation
from est.io.utils.read import get_data
from est.io.utils import url as url_utils
from orangecontrib.est.widgets.utils.xas_input import XASInputOW


def test_xas_input_no_dataset(qtapp):
    "Check behavior if no settings exists"
    widget = XASInputOW()
    assert widget.buildXASObj() is None
    widget.loadSettings(input_information=MISSING_DATA)
    while qtapp.hasPendingEvents():
        qtapp.processEvents()
    assert widget.buildXASObj() is None


def test_xas_input_with_spec(qtapp, filename_cu_from_pymca, spectrum_cu_from_pymca):
    """Check behavior when a spec file is provided"""
    energy_url = url_utils.build_spec_data_url(
        file_path=str(filename_cu_from_pymca),
        col_name="Column 1",
    )
    spectra_url = url_utils.build_spec_data_url(
        file_path=str(filename_cu_from_pymca),
        col_name="Column 2",
    )
    input_information = InputInformation(
        spectra_url=spectra_url,
        channel_url=energy_url,
    )
    widget = XASInputOW()
    assert widget.buildXASObj() is None
    widget.loadSettings(input_information=input_information)
    while qtapp.hasPendingEvents():
        qtapp.processEvents()
    xas_obj = widget.buildXASObj()

    numpy.testing.assert_almost_equal(
        xas_obj.get_spectrum(0, 0).mu, spectrum_cu_from_pymca.mu
    )
    numpy.testing.assert_almost_equal(xas_obj.energy, spectrum_cu_from_pymca.energy)


@pytest.mark.skipif(larch is None, reason="larch is not installed")
def test_xas_input_xmu(qtapp, filename_cu_from_larch):
    input_information = InputInformation(
        spectra_url=DataUrl(
            file_path=str(filename_cu_from_larch),
            data_path=None,
            scheme="larch",
        )
    )
    widget = XASInputOW()
    assert widget.buildXASObj() is None
    widget.loadSettings(input_information=input_information)
    while qtapp.hasPendingEvents():
        qtapp.processEvents()
    xas_obj = widget.buildXASObj()
    assert xas_obj is not None


def test_xas_input_hdf5(qtapp, hdf5_filename_cu_from_pymca):
    """
    Check behavior if we provide to the widget some valid inputs
    """
    energy_url = DataUrl(
        file_path=str(hdf5_filename_cu_from_pymca),
        data_path="/1.1/instrument/energy/value",
        scheme="silx",
    )
    spectra_url = DataUrl(
        file_path=str(hdf5_filename_cu_from_pymca),
        data_path="/1.1/instrument/mu/data",
        scheme="silx",
    )
    input_information = InputInformation(
        spectra_url=spectra_url,
        channel_url=energy_url,
    )
    widget = XASInputOW()
    assert widget.buildXASObj() is None
    widget.loadSettings(input_information=input_information)
    while qtapp.hasPendingEvents():
        qtapp.processEvents()
    xas_obj = widget.buildXASObj()
    numpy.testing.assert_almost_equal(
        xas_obj.get_spectrum(0, 0).mu, get_data(spectra_url)
    )
    numpy.testing.assert_almost_equal(xas_obj.energy, get_data(energy_url))
