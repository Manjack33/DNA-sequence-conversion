#!/usr/bin/env python3

import sys
from pathlib import Path


class DNA_Byte:
    dna_sequence: str
    quality_score: str


def main() -> None:
    file_path: str = sys.argv[1]
    fragment_length: int = int(sys.argv[2])
    data: list[bin] = load_data(file_path)

    check_length_equality(data, fragment_length)
    dna_fragments = split_to_fragments(data, fragment_length)
    write_report(dna_fragments)


def check_length_equality(data: list[bin], fragment_length) -> None:
    """Checks whether the fragment_length number would split the dna data into the equal sized fragments."""
    if len(data) % fragment_length != 0:
        print(f'Fragment length {fragment_length} is not valid in this case.\nSet number which splits {len(data)} bytes file into the equal fragments!')
        sys.exit(1)


def load_data(file_path) -> list[bin]:
    """Loads input binary file and returns list of data bytes."""
    return [bin(byte) for byte in Path(file_path).read_bytes()]


def split_to_fragments(data: list[bin], fragment_length: int) -> list[list[DNA_Byte]]:
    """Splits DNA data into the equal fragments."""
    index = 0
    dna_fragments = []

    while index != len(data):
        fragment = []
        for byte in data[index:index + fragment_length]:
            fragment.append(split_byte(byte=byte[2:]))
        dna_fragments.append(fragment)
        index = index + fragment_length

    return dna_fragments


def split_byte(byte: str):
    """Splits DNA byte into the DNA sequence marker and Quality score character."""
    dna_byte = DNA_Byte()
    dna_byte.dna_sequence = dna_convert(byte[:-6])
    dna_byte.quality_score = chr(int(byte[-6:], 2) + 33)
    return dna_byte


def dna_convert(dna: str) -> str:
    """Evaluate first 2 bits into the DNA markers."""
    try:
        dna_integer = int(dna, 2)
    except ValueError:
        dna_integer = 0

    match dna_integer:
        case 0: return 'A'
        case 1: return 'C'
        case 2: return 'G'
        case 3: return 'T'


def write_report(dna_fragments: list[list[DNA_Byte]]):
    """Prints the output of the DNA sequences."""
    for index, fragment in enumerate(dna_fragments):
        print(f'@READ_{index+1}\n{"".join([dna_byte.dna_sequence for dna_byte in fragment])}\n'
              f'+READ_{index+1}\n{"".join([dna_byte.quality_score for dna_byte in fragment])}')


if __name__ == '__main__':
    main()
