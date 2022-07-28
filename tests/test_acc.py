import pytest
from datetime import datetime
from time import sleep
from src.accounts import Standard_account, Abstract_account


@pytest.fixture
def numbers():
    inp = 1
    exp_out = 1
    return [inp, exp_out]


class TestAcc:
    def test_create_standatd(self):
        sa = Standard_account()
        assert isinstance(sa, object)

    def test_fail_create_abstract(self):
        try:
            aa = Abstract_account()
            assert isinstance(aa, object)
        except (RuntimeError, TypeError, NameError, AssertionError):
            raise AssertionError("Abstract account should not be created")

    def test_zero_balance_on_start(self):
        sa = Standard_account()
        assert sa._balance == 0

    def test_deposition_works_int(self):
        sa = Standard_account()
        sa.deposit(1)
        assert sa._balance == 1

    def test_deposition_works_float(self):
        sa = Standard_account()
        sa.deposit(100.0)
        assert sa._balance == 100

    def test_deposition_works_str(self):
        sa = Standard_account()
        sa.deposit("555.31")
        assert sa._balance == 555.31

    def test_deposition_fails_str(self):
        sa = Standard_account()
        ret_val = sa.deposit("one million bucks")
        assert sa._balance == 0 and ret_val != 0

    def test_deposition_fails_negative(self):
        sa = Standard_account()
        ret_val_int = sa.deposit(-3)
        ret_val_float = sa.deposit(-3.0001)
        ret_val_str = sa.deposit("-3")
        assert (
            sa._balance == 0
            and ret_val_int != 0
            and ret_val_float != 0
            and ret_val_str != 0
        )

    def test_withdrawal_int_1(self):
        sa = Standard_account()
        sa._balance = 100.0
        ret_val = sa.withdraw(100)
        assert sa._balance == 0.0 and ret_val == 0

    def test_withdrawal_int_2(self):
        sa = Standard_account()
        sa._balance = 100.0
        ret_val = sa.withdraw(10)
        assert sa._balance == 90.0 and ret_val == 0

    def test_withdrawal_float(self):
        sa = Standard_account()
        sa._balance = 100.0
        ret_val = sa.withdraw(10.0)
        assert sa._balance == 90.0 and ret_val == 0

    def test_withdrawal_str(self):
        sa = Standard_account()
        sa._balance = 100.0
        ret_val = sa.withdraw("10.0")
        assert sa._balance == 90.0 and ret_val == 0

    def test_withdrawal_fails_str(self):
        sa = Standard_account()
        sa._balance = 100.0
        ret_val = sa.withdraw("blablabla")
        assert sa._balance == 100.0 and ret_val != 0

    def test_withdrawal_fails_negative(self):
        sa = Standard_account()
        sa._balance = 100.0
        ret_val = sa.withdraw(-1000)
        assert sa._balance == 100.0 and ret_val != 0

    def test_withdrawal_fails_limit_ext(self):
        sa = Standard_account()
        sa._balance = 100.0
        ret_val = sa.withdraw(1000)
        assert sa._balance == 100.0 and ret_val != 0

    def test_deposit_no_arg(self):
        sa = Standard_account()
        sa._balance = 100.0
        sa.deposit()
        assert sa._balance == 100.0

    def test_withdrawal_no_arg(self):
        sa = Standard_account()
        sa._balance = 100.0
        sa.withdraw()
        assert sa._balance == 100.0

    def test_integrational_1(self):
        sa = Standard_account()
        sa.deposit(1000)
        sa.withdraw(500.0)
        sa.withdraw("600.0")
        sa.deposit(1.0)
        assert sa._balance == 501.0

    def test_integrational_2(self):
        sa = Standard_account()
        sa.deposit(1000)
        sa.deposit(500.0)
        sa.withdraw("600.0")
        assert sa._balance == 900.0

    def test_display_1(self):
        def check(history: str, acc_lst: list, balance_lst: list):
            operations = history.split("\n")[:-2]
            for op, acc, balance in zip(operations, acc_lst, balance_lst):
                acc_in_op = float(op[21:41])
                balance_in_op = float(op[41:])
                assert acc_in_op == acc and balance_in_op == balance

        sa = Standard_account()
        sa.deposit(1000)
        sa.deposit(500.0)
        sa.withdraw("600.0")
        history = sa.get_history()
        acc_lst = [+1000, +500, -600]
        balance_lst = [1000, 1500, 900]
        check(history, acc_lst, balance_lst)
        assert sa._balance == 900.0

    def test_display_2(self):
        def check(history: str, acc_lst: list, balance_lst: list):
            operations = history.split("\n")[:-2]
            for op, acc, balance in zip(operations, acc_lst, balance_lst):
                acc_in_op = float(op[21:41])
                balance_in_op = float(op[41:])
                assert acc_in_op == acc and balance_in_op == balance

        sa = Standard_account()
        sa.deposit(-1)
        sa.deposit(500.0)
        sa.withdraw()
        sa.withdraw(100)
        sa.withdraw(400)
        sa.withdraw()
        history = sa.get_history()
        acc_lst = [+500, 0, -100, -400, 0]
        balance_lst = [500, 500, 400, 0, 0]
        check(history, acc_lst, balance_lst)
        assert sa._balance == 0.0

    def test_display_time_1(self):
        def check(history: str, acc_lst: list, balance_lst: list):
            operations = history.split("\n")[:-2]
            lst_times = []
            for op, acc, balance in zip(operations, acc_lst, balance_lst):
                time_op = datetime.strptime(op[:21], " %d.%m.%Y %H:%M:%S ")
                lst_times.append(time_op)
                acc_in_op = float(op[21:41])
                balance_in_op = float(op[41:])
                assert acc_in_op == acc and balance_in_op == balance
            assert (lst_times[-1] - lst_times[0]).total_seconds() < 2, "TIME"

        sa = Standard_account()
        sa.deposit(-1)
        sa.deposit(500.0)
        sa.withdraw()
        sa.withdraw(100)
        sa.withdraw(400)
        sa.withdraw()
        history = sa.get_history()
        acc_lst = [+500, 0, -100, -400, 0]
        balance_lst = [500, 500, 400, 0, 0]
        check(history, acc_lst, balance_lst)
        assert sa._balance == 0.0

    def test_display_time_2(self):
        TIME_SLEEP = 3

        def check(history: str, acc_lst: list, balance_lst: list):
            operations = history.split("\n")[:-2]
            lst_times = []
            for op, acc, balance in zip(operations, acc_lst, balance_lst):
                time_op = datetime.strptime(op[:21], " %d.%m.%Y %H:%M:%S ")
                lst_times.append(time_op)
                acc_in_op = float(op[21:41])
                balance_in_op = float(op[41:])
                assert acc_in_op == acc and balance_in_op == balance
            assert (lst_times[-1] - lst_times[0]).total_seconds() >= TIME_SLEEP

        sa = Standard_account()
        sa.deposit(-1)
        sa.deposit(500.0)
        sa.withdraw()
        sa.withdraw(100)
        sleep(TIME_SLEEP)
        sa.withdraw(400)
        sa.withdraw()
        history = sa.get_history()
        acc_lst = [+500, 0, -100, -400, 0]
        balance_lst = [500, 500, 400, 0, 0]
        check(history, acc_lst, balance_lst)
        assert sa._balance == 0.0
