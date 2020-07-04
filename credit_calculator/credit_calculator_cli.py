import argparse
import math
import sys


class Parameter:
    '''Store calculation parameter.'''
    def __init__(self, value, type_, prompt):
        self.value = value
        self.type_ = type_
        self.prompt = prompt


class CreditCalculatorCLI:
    '''Credit calculator is able to work with different types of payment and to work with command-line arguments.'''

    def __init__(self):

        parser = argparse.ArgumentParser()

        parser.add_argument('--type', help='type of payments [annuity | diff]')
        parser.add_argument('--principal', type=int, help='credit principal')
        parser.add_argument('--periods', type=int, help='count of months to pay')
        parser.add_argument('--interest', type=float, help='interest rate (in percents)')
        parser.add_argument('--payment', type=float, help='monthly payment')

        args = parser.parse_args()

        if any((
            self.count_args(args) < 4,
            args.type not in ('annuity', 'diff'),
            args.type == 'diff' and args.payment is not None,
            any(v < 0 for v in vars(args).values() if isinstance(v, int) or isinstance(v, float)),
            args.interest is None,
        )):
            print('Incorrect parameters')
            sys.exit()

        # 'credit_principal', 'monthly_payment', 'credit_interest', 'count_of_month'
        self.parameters = {
            'type_of_payments': Parameter(args.type, str, None),
            'credit_principal': Parameter(args.principal, int, 'Enter credit principal'),
            'monthly_payment': Parameter(args.payment, float, 'Enter monthly payment'),
            'credit_interest': Parameter(args.interest, float, 'Enter credit interest'),
            'count_of_month': Parameter(args.periods, int, 'Enter count of periods'),
        }

    def run(self):
        if self.parameters['type_of_payments'].value == 'diff':
            self.process_diff()
        else:
            self.process_annual()

    def process_diff(self):
        monthly_payment = self.calculate_diff_payment()
        self.print_monthly_payment(monthly_payment)
        print(f"Overpayment = {sum(monthly_payment) - self.parameters['credit_principal'].value}")

    def calculate_diff_payment(self):
        p = self.parameters
        monthly_payment = []

        interest_rate = p['credit_interest'].value / (12 * 100)
        cm = p['count_of_month'].value
        cp = p['credit_principal'].value

        for month in range(1, cm + 1):
            monthly_payment.append(math.ceil(cp / cm + interest_rate * (cp - cp * (month - 1) / cm)))

        return monthly_payment

    @staticmethod
    def print_monthly_payment(monthly_payment):
        for i, p in enumerate(monthly_payment):
            print(f'Month {i + 1}: paid out {p}')
        print()

    def process_annual(self):
        '''Calculate annual payment.'''
        option = self.get_option()

        if option == 'n':  # count of month
            self.get_parameters('credit_principal', 'monthly_payment', 'credit_interest')
            count_of_month = self.calculate_count_of_month()
            self.print_count_of_month(count_of_month)
            overpayment = (count_of_month * self.parameters['monthly_payment'].value
                           - self.parameters['credit_principal'].value)
            print(f"Overpayment = {math.ceil(overpayment)}")

        elif option == 'a':  # annuity monthly payment
            self.get_parameters('credit_principal', 'count_of_month', 'credit_interest')
            monthly_payment = self.calculate_monthly_payment()
            print(f'Your annuity payment = {monthly_payment}!')
            overpayment = (monthly_payment * self.parameters['count_of_month'].value
                           - self.parameters['credit_principal'].value)
            print(f"Overpayment = {math.ceil(overpayment)}")

        elif option == 'p':  # credit principal
            self.get_parameters('monthly_payment', 'count_of_month', 'credit_interest')
            credit_principal = self.calculate_credit_principal()
            print(f'Your credit principal = {credit_principal}!')
            overpayment = (self.parameters['monthly_payment'].value * self.parameters['count_of_month'].value
                           - credit_principal)
            print(f"Overpayment = {math.ceil(overpayment)}")

        else:
            print(f'You enter wrong option: "{option}"')

    def get_option(self):
        '''Get option to calculate'''
        if (all(
                    self.parameters[p].value >= 0
                    for p in ('credit_principal', 'monthly_payment', 'credit_interest')
                    if self.parameters[p].value is not None
                )
            and self.parameters['count_of_month'].value is None):
            return 'n'
        elif (all(
                    self.parameters[p].value >= 0
                    for p in ('credit_principal', 'count_of_month', 'credit_interest')
                    if self.parameters[p].value is not None
                 )
            and self.parameters['monthly_payment'].value is None):
            return 'a'
        elif (all(
                    self.parameters[p].value >= 0
                    for p in ('monthly_payment', 'count_of_month', 'credit_interest')
                    if self.parameters[p].value is not None
                 )
            and self.parameters['credit_principal'].value is None):
            return 'p'
        else:
            print('Wrong arguments set.')

    def get_parameters(self, *parameter_names):
        '''Get calculation parameters by theirs names.'''
        for p_name in parameter_names:
            p = self.parameters[p_name]
            p.value = p.type_(p.value)

    def calculate_count_of_month(self):
        '''Calculate count of month to return a credit with annuity payments.'''
        p = self.parameters
        interest_rate = p['credit_interest'].value / (12 * 100)
        count_of_month = math.log(
            (
                p['monthly_payment'].value
                /  # -----------------------divide the top by the bottom-----------------
                (p['monthly_payment'].value - interest_rate * p['credit_principal'].value)
            ),
            1 + interest_rate
        )
        return math.ceil(count_of_month)  # count_of_month

    def calculate_monthly_payment(self):
        '''Calculate monthly payment to return a credit with annuity payments.'''
        p = self.parameters
        interest_rate = p['credit_interest'].value / (12 * 100)
        monthly_payment = p['credit_principal'].value * interest_rate * (1 + interest_rate) ** p['count_of_month'].value
        monthly_payment /= (1 + interest_rate) ** p['count_of_month'].value - 1

        return math.ceil(monthly_payment)

    def calculate_credit_principal(self):
        '''Calculate credit principal to return a credit with annuity payments.'''
        p = self.parameters
        interest_rate = p['credit_interest'].value / (12 * 100)
        credit_principal = p['monthly_payment'].value * ((1 + interest_rate) ** p['count_of_month'].value - 1)
        credit_principal /= interest_rate * (interest_rate + 1) ** p['count_of_month'].value

        return math.floor(credit_principal)

    @staticmethod
    def print_count_of_month(count_of_month):
        '''Convert number of month to years, months form and print it.'''
        years, months = int(count_of_month // 12), math.ceil(count_of_month % 12)
        msg = f'You need'
        msg += '' if years == 0 else ' 1 year' if years == 1 else f' {years} years'
        msg += '' if months == 0 else ' and 1 month' if months == 1 else f' {months} months'
        msg += ' to repay this credit!'
        print(msg)

    @staticmethod
    def count_args(args):
        '''Calculate number of arguments.'''
        return sum(v is not None for v in vars(args).values())

if __name__ == '__main__':

    calc = CreditCalculatorCLI()
    calc.run()

