#!/usr/bin/env python3

import sys
from pathlib import Path


class DnaByte:
    dna_base: str
    quality_score: str


def load_data(file_path: str) -> bytes:
    """Loads input binary file and returns them as bytes."""
    return Path(file_path).read_bytes()


def check_length_equality(data: bytes, fragment_length: int) -> None:
    """Checks whether the length of possible fragments would be split into the equal sized fragments."""
    if len(data) % fragment_length != 0:
        print(f'Fragment length {fragment_length} is not valid in this case.\n'
              f'Set number which splits {len(data)} bytes file into the equal fragments!')
        sys.exit(1)


def elaborate_data(data: bytes) -> list[bin]:
    """Processes data bytes and returns them as list of 8-bits long binary numbers"""
    return [bin(byte)[2:].rjust(8, '0') for byte in data]


def split_to_fragments(data: list[bin], fragment_length: int) -> list[list[DnaByte]]:
    """Splits DNA data into the equal fragments."""
    index = 0
    dna_fragments = []

    while index != len(data):
        fragment = []
        for byte in data[index:index+fragment_length]:
            fragment.append(split_byte(byte))
        dna_fragments.append(fragment)
        index = index + fragment_length
    return dna_fragments


def split_byte(byte: str) -> DnaByte:
    """Splits DNA byte into the DNA base and quality score character as stores them as a DnaByte class object."""
    dna_byte = DnaByte()
    dna_byte.dna_base = dna_convert(dna_base=int(byte[:-6], 2))
    dna_byte.quality_score = chr(int(byte[-6:], 2) + 33)
    return dna_byte


def dna_convert(dna_base: int) -> str:
    """Converts number into the DNA base character."""
    match dna_base:
        case 0: return 'A'
        case 1: return 'C'
        case 2: return 'G'
        case 3: return 'T'
        case _: raise ValueError(f'Invalid value, number must be between 0-3, but {dna_base} was given!')


def write_report(dna_fragments: list[list[DnaByte]]) -> None:
    """Prints the output of the DNA sequences."""
    for index, fragment in enumerate(dna_fragments):
        print(f'@READ_{index+1}\n{"".join([dna_byte.dna_base for dna_byte in fragment])}\n'
              f'+READ_{index+1}\n{"".join([dna_byte.quality_score for dna_byte in fragment])}')


def main() -> None:
    file_path: str = sys.argv[1]
    fragment_length: int = int(sys.argv[2])
    data: bytes = load_data(file_path)

    check_length_equality(data, fragment_length)
    dna_fragments = split_to_fragments(data=elaborate_data(data), fragment_length=fragment_length)
    write_report(dna_fragments)


if __name__ == '__main__':
    main()
