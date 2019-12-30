alphabet = 'abcdefghijklmnopqrstuvwxyz'


def generate_sequence(number_of_items):
    alphabet_length = len(alphabet)
    sequence = []

    count = 0
    while count < number_of_items:
        if count < alphabet_length:
            sequence.append(alphabet[count])

        count += 1

    return sequence
