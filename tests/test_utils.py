from src.utils import generate_sequence


class TestGenerateSequence:
    def test_short(self):
        expected = ['a',
                    'b',
                    'c',
                    'd',
                    'e',
                    ]
        actual = generate_sequence(5)
        assert expected == actual
