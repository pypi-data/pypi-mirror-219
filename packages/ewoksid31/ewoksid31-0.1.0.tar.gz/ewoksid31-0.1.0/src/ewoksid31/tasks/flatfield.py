import numpy
from scipy.io import loadmat
from ewokscore import Task


class FlatFieldFromEnergy(
    Task,
    input_names=["newflat", "oldflat", "energy"],
    output_names=["flatfield"],
):
    """Interpolate an energy-stack of flat-field images.

    The resulting flat-field image can be used as follows
    to correct diffraction patterns for flat field:

    .. code::

        Icor = I / flatfield
    """

    def run(self):
        energy = self.inputs.energy
        new_flat = _interpolated_flatfield(self.inputs.newflat, "E", "F", energy)
        old_flat = _interpolated_flatfield(self.inputs.oldflat, "Eold", "Fold", energy)
        flatfield = old_flat / new_flat
        flatfield[~numpy.isfinite(flatfield)] = 1
        self.outputs.flatfield = flatfield


def _interpolated_flatfield(
    matlab_filename: str, energy_key: str, flatfield_key: str, energy: float
) -> numpy.ndarray:
    """
    :param matlab_filename: matlab file from ID31 that contains an energy-stack of images
    :param energy_key:
    :param flatfield_key:
    :param energy:
    :return: interpolated image (nrow, ncol)
    """
    m = loadmat(matlab_filename)
    flatfields = m[flatfield_key]
    energies = numpy.squeeze(m[energy_key]).astype(float)
    return _interpolate_flatfields(energies, flatfields, energy)


def _interpolate_flatfields(
    energies: numpy.ndarray, flatfields: numpy.ndarray, energy: float
) -> numpy.ndarray:
    """
    :param energies: array of energies (nenergies,)
    :param flatfields: stack of images (nrow, ncol, nenergies)
    :param energy:
    :return: interpolated image (nrow, ncol)
    """
    j = numpy.argsort(abs(energies - energy))[0:2]
    j.sort()
    j_before, j_after = j
    e_before = energies[j_before]
    e_after = energies[j_after]
    w_before = (e_after - energy) / (e_after - e_before)
    w_after = (energy - e_before) / (e_after - e_before)
    f_before = flatfields[..., j_before]
    f_after = flatfields[..., j_after]
    return w_before * f_before + w_after * f_after
