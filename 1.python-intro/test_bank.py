import csv
from pathlib import Path

import pytest

from bank import dispatch_customers

DIR = Path(__file__).parent

CASES = [f"input{i}" for i in range(1, 11)]


def read_customers(csv_path):
    with open(csv_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        return [(row[0].strip(), row[1].strip()) for row in reader]


def read_expected(expected_path):
    return expected_path.read_text().splitlines()


@pytest.mark.parametrize("case", CASES)
def test_dispatch_customers(case):
    input_csv = DIR / f"{case}.csv"
    expected_txt = DIR / f"{case.replace('input', 'expected')}.txt"

    customers = read_customers(input_csv)
    expected = read_expected(expected_txt)

    assert dispatch_customers(customers) == expected
