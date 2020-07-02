import math


def calculate_count_of_month(credit_principal, monthly_payment, credit_interest):
    '''Calculate count of month for return a credit with annuity payments.'''

    interest_rate = credit_interest / (12 * 100)
    count_of_month = math.log(
        monthly_payment / (monthly_payment - interest_rate * credit_principal),
        1 + interest_rate
    )
    count_of_month = math.ceil(count_of_month)
    years, months = int(count_of_month // 12), math.ceil(count_of_month % 12)

    return years, months


def calculate_monthly_payment(credit_principal, count_of_month, credit_interest):
    '''Calculate monthly payment for return a credit with annuity payments.'''

    interest_rate = credit_interest / (12 * 100)
    monthly_payment = credit_principal * interest_rate * (1 + interest_rate) ** count_of_month
    monthly_payment /= (1 + interest_rate) ** count_of_month - 1

    return math.ceil(monthly_payment)


def calculate_credit_principal(monthly_payment, count_of_month, credit_interest):
    '''Calculate credit principal for return a credit with annuity payments.'''

    interest_rate = credit_interest / (12 * 100)
    credit_principal = monthly_payment * ((1 + interest_rate) ** count_of_month - 1)
    credit_principal /= interest_rate * (interest_rate + 1) ** count_of_month

    return math.ceil(credit_principal)


main_prompt = 'What do you want to calculate?'
parameter_prompt = (
    'type "n" - for count of months,\n'
    'type "a" - for annuity monthly payment,\n'
    'type "p" - for credit principal:\n'
)

print(main_prompt)
parameter = input(parameter_prompt)

if parameter == 'n':  # count of month
    credit_principal = int(input('Enter credit principal:\n'))
    monthly_payment = int(input('Enter monthly payment:\n'))
    credit_interest = float(input('Enter credit interest:\n'))
    years, months = calculate_count_of_month(credit_principal, monthly_payment, credit_interest)
    msg = f'You need'
    msg += '' if years == 0 else ' 1 year' if years == 1 else f' {years} years'
    msg += '' if months == 0 else ' and 1 month' if months == 1 else f' {months} months'
    msg += ' to repay this credit!'
    print(msg)

elif parameter == 'a':  # annuity monthly payment
    credit_principal = int(input('Enter credit principal:\n'))
    count_of_month = int(input('Enter count of periods:\n'))
    credit_interest = float(input('Enter credit interest:\n'))
    monthly_payment = calculate_monthly_payment(credit_principal, count_of_month, credit_interest)
    print(f'Your annuity payment = {monthly_payment}!')

elif parameter == 'p':  # credit principal
    monthly_payment = float(input('Enter monthly payment:\n'))
    count_of_month = int(input('Enter count of periods:\n'))
    credit_interest = float(input('Enter credit interest:\n'))
    credit_principal = calculate_credit_principal(monthly_payment, count_of_month, credit_interest)
    print(f'Your credit principal = {credit_principal}!')

else:
    print(f'You enter wrong parameter: "{parameter}"')
