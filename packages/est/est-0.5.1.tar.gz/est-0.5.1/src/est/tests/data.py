from typing import Union, Tuple
import numpy
from numpy.typing import ArrayLike
from est.resources import resource_path


def example_spectrum(
    spectrum: Union[Tuple, str] = "exafs/EXAFS_Ge.dat"
) -> Tuple[ArrayLike, ArrayLike]:
    if isinstance(spectrum, tuple):
        energy = numpy.linspace(*spectrum)  # eV
        mi, ma = energy.min(), energy.max()
        edge = mi + (ma - mi) * 0.08
        mu = numpy.linspace(0.6, 0.1, energy.size) + (energy > edge).astype(int)
    elif spectrum in ("exafs/EXAFS_Cu.dat", "exafs/EXAFS_Ge.dat", "exafs/cu_rt01.xmu"):
        energy, mu, *_ = numpy.loadtxt(resource_path(spectrum)).T
    else:
        energy, mu = example_spectrum((5000, 5500, 100))
    return energy, mu


def example_spectra(
    spectrum: Union[Tuple, str] = "exafs/EXAFS_Ge.dat",
    shape: Tuple[int] = (0, 1, 1),
    noise: bool = False,
) -> Tuple[ArrayLike, ArrayLike]:
    """Replicate a single spectrum to a nD dataset with optional noise addition."""
    energy, mu = example_spectrum(spectrum=spectrum)
    nenergy = shape[0]
    if shape[0]:
        assert nenergy <= len(energy)
        energy = energy[:nenergy]
        mu = mu[:nenergy]
    else:
        nenergy = len(energy)
    mu = mu.reshape((nenergy,) + (1,) * (len(shape) - 1))
    tile_repts = (1,) + shape[1:]
    mu = numpy.tile(mu, tile_repts)
    if noise:
        mu += numpy.random.normal(0.0, 0.05, shape)
    return energy, mu
