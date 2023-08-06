import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

loan = {
    'price': 20_000_000,
    'year_rate': 0.02,
    'month_payment': 150_000
}


def set_loan():
    global loan
    loan['price'] = 20_000_000


def calculate_month_to_pay_loan(loan: dict[str]) -> int:
    months = 0
    rates = 0
    while True:
        month_rate_price = loan['price'] * loan['year_rate'] / 12
        monthly_payed = loan['month_payment'] - month_rate_price
        rates += month_rate_price
        loan['price'] -= monthly_payed
        months += 1
        if loan['price'] <= 0: break
    return months, rates


def calculate_year_to_pay_loan(loan: dict[str]) -> int:
    years = 1
    rates = 0
    while True:
        year_rate_price = loan['price'] * loan['year_rate']
        yearly_payed = loan['month_payment'] * 12 - year_rate_price
        rates += year_rate_price
        loan['price'] -= yearly_payed
        years += 1
        if loan['price'] <= 0: break
    return years, rates


set_loan()
MONTHS, RATES = calculate_month_to_pay_loan(loan)
YEARS = MONTHS // 12
print("Monthly loan decrease")
print(f"months: {MONTHS}")
print(f"years: {YEARS}")
print(f"rates: {RATES}")
print()

set_loan()
YEARS, RATES = calculate_year_to_pay_loan(loan)
print("Yearly loan decrease")
print(f"years: {YEARS}")
print(f"rates: {RATES}")
