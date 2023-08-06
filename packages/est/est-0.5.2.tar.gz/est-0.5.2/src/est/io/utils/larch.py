from larch.io.columnfile import read_ascii as larch_read_ascii
from est.units import ur


def read_ascii(xmu_file, energy_unit=ur.eV):
    """

    :param xmu_file: file containing the spectrum definition
    :return: (energy, mu)
    :rtype: tuple
    """
    larch_group = larch_read_ascii(xmu_file)
    energy = (larch_group.energy * energy_unit).m_as(ur.eV)
    return energy, larch_group.mu
