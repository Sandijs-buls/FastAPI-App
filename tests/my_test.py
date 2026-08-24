from app.calculations import add, subtract, multiply, divide, BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)
@pytest.mark.parametrize("num1, num2, expected", 
[   (5,2,7),
    (7,1,8),
    (12, 4, 16)           
]
                        )

def test_add(num1, num2, expected):
    print("Testing add function")
    result = add(num1, num2)
    assert result == expected

def test_subtract():
    print("Testing subtract function")
    result = subtract(5, 2)
    assert result == 3

def test_multiply():
    print("Testing multiply function")
    result = multiply(5, 2)
    assert result == 10

def test_divide():
    print("Testing divide function")
    result = divide(5, 2)
    assert result == 2.5


def test_bank_set_initial_amount(bank_account):
    
    assert bank_account.balance == 50

def test_bank_empty(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 5) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", 
[   (200,100,100),
    (50,50,0),
    (40, 4, 36)         
]
                        )

def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(1000)