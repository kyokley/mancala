from src.utils import generate_sequence


class TestGenerateSequence:
    def test_short(self):
        expected = [
            'a',
            'b',
            'c',
            'd',
            'e',
        ]
        actual = generate_sequence(5)
        assert expected == actual

    def test_one_cycle(self):
        expected = [
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            'aa',
            'ab',
            'ac',
            'ad',
            'ae',
            'af',
        ]
        actual = generate_sequence(32)
        assert expected == actual
