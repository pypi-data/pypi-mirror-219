from mfire.utils.unit_converter import fromWWMFToW1


class TestConversion:
    def test_simple(self):
        assert set(fromWWMFToW1(98)) == {28, 29}
        assert set(fromWWMFToW1(61)) == {13}

    def test_list(self):
        assert set(fromWWMFToW1([98, 99])) == {26, 27, 28, 29}
        assert set(fromWWMFToW1([40, 53, 61, 99])) == {7, 11, 12, 13, 26, 27, 28, 29}
