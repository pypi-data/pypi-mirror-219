import numpy
from .resources import resource_filename
from ..tasks.flatfield import FlatFieldFromEnergy


def test_flatfield():
    inputs = {
        "newflat": resource_filename("flats.mat"),
        "oldflat": resource_filename("flats_old.mat"),
        "energy": 90.0,
    }
    task = FlatFieldFromEnergy(inputs=inputs)
    task.execute()
    # Flat-field correction:
    #  Icor = I * 0.8115191925457376 = I / flatfield
    numpy.testing.assert_allclose(1 / task.outputs.flatfield[0, 0], 0.8115191925457376)
