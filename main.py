from src.accounts import Standard_account


if __name__ == "__main__":
    sa = Standard_account()
    sa.deposit(1000)
    sa.withdraw(500)
    sa.display()
    del sa
