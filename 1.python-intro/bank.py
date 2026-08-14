import csv
import sys
from typing import List, Tuple


def dispatch_customers(customers: List[Tuple[str, str]]) -> List[str]:
    pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bank.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    customers = []

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            customers.append((row[0], row[1])) 

    dispatched_customers = dispatch_customers(customers)
    for c in dispatched_customers:
        print(c)
