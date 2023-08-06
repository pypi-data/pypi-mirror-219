import pytest
from ewoksorange.tests.conftest import qtapp  # noqa F811
from est import resources
from est.core.types import Spectrum
from . import data


@pytest.fixture()
def example_pymca() -> str:
    return str(resources.resource_path("workflows/example_pymca.ows"))


@pytest.fixture()
def example_larch() -> str:
    return str(resources.resource_path("workflows/example_larch.ows"))


@pytest.fixture()
def example_bm23() -> str:
    return str(resources.resource_path("workflows/example_bm23.ows"))


@pytest.fixture()
def filename_cu_from_pymca() -> str:
    return str(resources.resource_path("exafs/EXAFS_Cu.dat"))


@pytest.fixture()
def filename_cu_from_larch() -> str:
    return str(resources.resource_path("exafs/cu_rt01.xmu"))


@pytest.fixture()
def spectrum_cu_from_pymca() -> Spectrum:
    energy, mu = data.example_spectrum("exafs/EXAFS_Cu.dat")
    return Spectrum(energy=energy, mu=mu)


@pytest.fixture()
def spectrum_cu_from_larch() -> Spectrum:
    energy, mu = data.example_spectrum("exafs/cu_rt01.xmu")
    return Spectrum(energy=energy, mu=mu)


@pytest.fixture()
def hdf5_filename_cu_from_pymca(tmpdir) -> str:
    return str(
        resources.generate_resource(
            resource="exafs/EXAFS_Cu.dat", word="L", output_directory=str(tmpdir)
        )
    )
