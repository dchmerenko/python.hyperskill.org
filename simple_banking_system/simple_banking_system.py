import random


class Card:

    IIN = '400000'  # Issuer Identification Number

    def __init__(self):
        number = Card.IIN + Card.generate_account_number()
        number += Card.get_check_sum(number)
        pin = Card.generate_pin()
        self.number = number
        self.pin = pin
        self.amount = 0

    def get_amount(self):
        return self.amount

    @staticmethod
    def generate_account_number():
        return str(random.randint(0, 999999999)).rjust(9, '0')

    @staticmethod
    def generate_pin():
        return str(random.randint(0, 9999)).rjust(4, '0')

    @staticmethod
    def get_check_sum(number):
        return str(10 - sum(int(c) if i % 2 != 0 else
                            2 * int(c) if int(c) < 5 else
                            2 * int(c) - 9
                            for i, c in enumerate(number)) % 10)


class SBS:

    def __init__(self):
        self.cards = {}
        self.go_on = True
        self.active_card = None

    def run(self):
        while self.go_on:
            self.get_menu_option()()

    def get_menu_option(self):

        if self.active_card:
            print('1. Balance')
            print('2. Log out')
            print('0. Exit')
            option = input().strip()

            return {'1': self.show_balance,
                    '2': self.log_out,
                    '0': self.exit,
                    }[option]
        else:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            option = input().strip()

            return {'1': self.create_account,
                    '2': self.log_into_account,
                    '0': self.exit,
                    }[option]

    def create_account(self):
        card = Card()
        self.cards[card.number] = card
        print(f'\nYour card has been created\n'
              f'Your card number:\n{card.number}\n'
              f'Your card PIN:\n{card.pin}\n')

    def log_into_account(self):
        print('\nEnter your card number:')
        card_number = input().strip()
        print('Enter your PIN:')
        card_pin = input().strip()
        if card_number in self.cards and card_pin == self.cards[card_number].pin:
            print('\nYou have successfully logged in!\n')
            self.cards[card_number].is_logged = True
            self.active_card = card_number
        else:
            print('\nWrong card number or PIN!\n')

    def show_balance(self):
        print(f'\nBalance: {self.cards[self.active_card].get_amount()}\n')

    def log_out(self):
        self.cards[self.active_card].is_logged = False
        self.active_card = None
        print('\nYou have successfully logged out!\n')

    def exit(self):
        self.go_on = False
        print('\nBye!')


if __name__ == '__main__':

    atm = SBS()
    atm.run()
