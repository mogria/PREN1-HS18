import pytest
import numpy
from mollyvision.digit_finder import DigitFinder

@pytest.fixture
def template():
    return numpy.zeros((40, 40, 3))

@pytest.fixture
def digit_finder(template):
    return DigitFinder(template)

def test_mask(template, digit_finder):
    assert digit_finder.mask[template.shape.width / 2: template.shape.height / 2]
