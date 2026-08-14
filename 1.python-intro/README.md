# Bank Teller Window

A bank has a teller window to serve its customers. Customers arrive and must wait their turn to be served. However, the bank manages different priority levels to organize service.

There are three types of customers:

1. **General public:** customers with no special priority.
2. **VIP customers:** customers with preferential service.
3. **Special attention:** people with disabilities, seniors, or pregnant women.

The teller window must always serve customers with higher priority first. Within the same priority level, customers should be served in the order they arrived.

The priority order is as follows:

1. Special attention.
2. VIP customers.
3. General public.

For example, if the following customers arrive:

* Ana, general public
* Luis, VIP
* Maria, general public
* Carlos, special attention

The order of service should be:

**Carlos -> Luis -> Ana -> Maria**

### Problem

Complete the implementation of `bank.py` so that the simulation of this process works properly.

The program will receive the path to a CSV format file, with the first column representing the customer's name and the second representing the customer type (`General`, `VIP`, `Special`):

```
Ana, General
Luis, VIP
Maria, General
Carlos, Special
```

The order in which customers arrive is defined by the order they appear in the input; that is, in the example above, the arrival order was `Ana -> Luis -> Maria -> Carlos`.

Internally, the business logic is implemented in the `dispatch_customers` function, which receives a list of customers and their type in the order they arrived at the bank. The output of this function is a list with the names of customers in the order they were served.

Input validation is not necessary, assume it will always be correct and there will be at least 1 customer.

### Test Cases

The `inputs/` directory includes 10 example input files (`input1.csv` to `input10.csv`), and the `outputs/` directory contains their corresponding expected output (`expected1.txt` to `expected10.txt`).

To verify your implementation of `bank.py` against a single case (for example `input1.csv`), run from this directory:

```bash
diff <(python bank.py inputs/input1.csv) outputs/expected1.txt && echo OK || echo FAIL
```

If nothing is printed except `OK`, your program's output matches the expected output exactly.

### Tests with pytest

Also included is `test_bank.py`, which directly tests the `dispatch_customers` function from `bank.py` (by importing it) against the same 10 input/expected output cases.

To run the tests using `pytest`:

```bash
pytest -v
```