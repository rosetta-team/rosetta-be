import conftest

class TestDescriptionComparer:
    def setup():
        self.comparer = DescriptionComparer()
        self.desc1 = 'Set Intersection — Returns a new array containing unique elements common to the two arrays. The order is preserved from the original array. It compares elements using their hash and eql? methods for efficiency. See also'
        self.desc2 = 'The Array.of() method creates a new Array instance from a variable number of arguments, regardless of number or type of the arguments.'
