import pytest
import kappa

EPSILON = 0.0001

def test_calculation_on_minimal_example():
    assert abs(kappa.main({'--filename': 'test/fixtures/minimal_example.txt', '--weighted': 'test/fixtures/customweights/weights_matrix_2x2.txt'}) - 0.4) < EPSILON


def test_assymmetric_weights():
    with pytest.raises(RuntimeError, match="Weights matrix has to be symmetric"):
        kappa.main({'--filename': 'test/fixtures/minimal_example.txt', '--weighted': 'test/fixtures/customweights/asymmetric_weights.txt'})


def test_invalid_weights():
    with pytest.raises(ValueError, match="numbers required"):
        kappa.main({'--filename': 'test/fixtures/minimal_example.txt', '--weighted': 'test/fixtures/customweights/invalid_weights.txt'})


def test_missing_weights_value():
    with pytest.raises(ValueError, match="same number of elements required in each row"):
        kappa.main({'--filename': 'test/fixtures/minimal_example.txt', '--weighted': 'test/fixtures/customweights/missing_weights.txt'})

    with pytest.warns(UserWarning, match="Empty input file"):
        with pytest.raises(ValueError, match="numbers required"):
            kappa.main({'--filename': 'test/fixtures/minimal_example.txt', '--weighted': 'test/fixtures/customweights/empty.txt'})


def test_bad_filename_for_weights_exit():
    with pytest.raises(OSError, match="not found"):
        kappa.main({'--filename': 'test/fixtures/minimal_example.txt', '--weighted': 'test/fixtures/customweights/does_not_exist.txt'})
