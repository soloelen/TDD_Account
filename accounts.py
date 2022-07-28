from abc import abstractmethod
from datetime import datetime


# Abstract Class
class Abstract_account(object):
    def __init__(self):
        self._balance = 0
        self._history = ""
        self.greeting_message()

    def greeting_message(self):
        print("Welcome to the Bank. The account is created.")

    @abstractmethod
    def deposit(self, amount: float):
        pass

    @abstractmethod
    def withdraw(self, amount: float):
        pass

    @abstractmethod
    def display(self):
        pass

    def get_balance(self):
        return self._balance

    def get_history(self):
        return self._history

    def set_balance(self, new_value: float):
        self._balance = new_value

    def set_history(self, new_value: float):
        self._history = new_value


# Child Class
class Standard_account(Abstract_account):
    def __init__(self):
        # conduct initialisation of the parent
        super().__init__()

    def _logging(self, operation_type: str, amount: float):
        """
        info:
            Log operation
        params:
            operation_type [str] - the type of logging operation:
                'deposit' or 'withdrawal'
            amount [float] - value of the operation
        returns:
            0 if operation is completed, -1 otherwise
        """
        try:
            if operation_type not in ["deposit", "withdrawal"]:
                raise TypeError("Wrong parameter in logging")
            amount = float(amount)
            assert amount >= 0
        except Exception as e:
            print("Operation aborted. Unsupported datatype or value.\n")
            del e
            return -1

        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y %H:%M:%S")
        sign_of_operation = "?"
        if operation_type == "deposit":
            sign_of_operation = "+"
        else:
            sign_of_operation = "-"
        amount_str = "{}{:.2f}".format(sign_of_operation, amount)
        balance_str = "{:.2f}".format(self.get_balance())
        event_to_add = "{: >20} {: >20} {: >20}\n".format(
            date_time, amount_str, balance_str
        )
        new_history = self.get_history() + event_to_add
        self.set_history(new_history)

        return 0

    def deposit(self, amount: float = 0):
        """
        info:
            Make a deposit
        params:
            amount [float] - value to be deposited.
        returns:
            0 if operation is completed, -1 otherwise
        """

        # test for argument validity
        try:
            amount = float(amount)
            assert amount >= 0
        except Exception as e:
            print("Operation aborted. Unsupported datatype or value.\n")
            del e
            return -1

        new_balance = self.get_balance() + amount

        # conduct operation
        self.set_balance(new_balance)

        # logging
        self._logging("deposit", amount)

        # finalizing message
        print(f"Operation completed successfully. You deposited {amount}.\n")

        return 0

    def withdraw(self, amount: float = 0):
        """
        info:
            Make a withdrawal
        params:
            amount [float] - value to be withdrew.
        returns:
            0 if operation is completed, -1 otherwise
        """

        # test for argument validity
        try:
            amount = float(amount)
            assert amount >= 0
        except Exception as e:
            print("Operation aborted. Unsupported datatype or value.\n")
            del e
            return -1

        # conduct operation
        if self.get_balance() >= amount:
            new_balance = self.get_balance() - amount
            self.set_balance(new_balance)

            # logging
            self._logging("withdrawal", amount)

            # finalizing message
            ms = f"Operation completed successfully. You withdrew {amount}.\n"
            print(ms)
            return 0
        else:
            # finalizing message
            print("Operation failed. Insufficient balance.\n")
            return -2

    def display(self):
        """
        info:
            Displays history
        params:
            No
        returns:
            history [str] - up to date history
        """

        print("{: >20} {: >20} {: >20}\n".format("Time", "Amount", "Balance"))
        history = self.get_history()
        print(history)
        return history
