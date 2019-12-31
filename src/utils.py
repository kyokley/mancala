alphabet = 'abcdefghijklmnopqrstuvwxyz'


def generate_sequence(number_of_items):
    alphabet_length = len(alphabet)
    sequence = []

    count = 0
    while count < number_of_items:
        if count < alphabet_length:
            sequence.append(alphabet[count])
        else:
            cycle = count // alphabet_length
            prefix = sequence[cycle - 1]
            sequence.append(f'{prefix}{alphabet[count % alphabet_length]}')

        count += 1

    return sequence
