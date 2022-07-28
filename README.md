# TDD_Account

## The task
Implement an Account abstract data type that represents a model of a bank checking account. The account is kept in arbitrary units and does not allow reaching a negative balance. Account must support the following operations:

- Deposit funds to the account.

- Withdraw funds from the account.

- Generate an account statement.

An example of an account statement format:

|   Time   | Amount | Balance |
| ----------------- | -- | -- |
|28.09.2021 13:37:00| +500| 500 |
|28.09.2021 13:37:01| -100| 400 |


## Necessary information

Classes implementation can be found in `src/accounts.py`

Tests can be found in `tests/test_acc.py`

To check example usage, please run `python main.py`

To start testing, please run `pytest -v` or `pytest -vs`
