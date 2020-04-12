import pytest
from flaskr.lib.description_comparer import DescriptionComparer

class TestDescriptionComparer:
    def setup(self):
        self.comparer = DescriptionComparer()


    def test_compare(self):
        desc1 = 'Set Intersection — Returns a new array containing unique elements common to the two arrays. The order is preserved from the original array. It compares elements using their hash and eql? methods for efficiency. See also'
        desc2 = 'The Array.of() method creates a new Array instance from a variable number of arguments, regardless of number or type of the arguments.'

        assert self.comparer.compare(desc1, desc2) == 0.9098949965688894

    def test_break_camelcase(self):
        text = 'isArray'

        assert self.comparer.break_camelcase(text) == 'is Array'
