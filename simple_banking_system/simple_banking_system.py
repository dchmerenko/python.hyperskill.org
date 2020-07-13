import random
import sqlite3


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
        r = sum(int(c) if i % 2 != 0 else
                            2 * int(c) if int(c) < 5 else
                            2 * int(c) - 9
                            for i, c in enumerate(number)) % 10
        return str((10 - r) % 10)

    @staticmethod
    def is_valid_card_number(number):
        return Card.get_check_sum(number[:-1]) == number[-1]



class DataBase:

    db_file = 'card.s3db'

    @staticmethod
    def create_db_connection(database):
        conn = None
        try:
            conn = sqlite3.connect(database)
            return conn
        except sqlite3.Error as e:
            print(repr(e))
        return conn

    @staticmethod
    def create_table(conn, sql_create_table_query):
        try:
            cur = conn.cursor()
            cur.execute(sql_create_table_query)
        except sqlite3.Error as e:
            print(repr(e))

    def __init__(self):
        sql = """ CREATE TABLE IF NOT EXISTS card (
                                            id INTEGER PRIMARY KEY,
                                            number TEXT,
                                            pin TEXT,
                                            balance INTEGER DEFAULT 0
                                        ); """
        self.conn = DataBase.create_db_connection(DataBase.db_file)
        if self.conn is not None:
            DataBase.create_table(self.conn, sql)
        else:
            print("Error! cannot create the database connection.")

    def create_card(self, card):
        sql = ''' INSERT INTO card(number, pin) VALUES (?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (card.number, card.pin))
        self.conn.commit()
        return cur.lastrowid

    def is_valid_card_pin(self, card_number, card_pin):
        sql = ''' SELECT pin FROM card WHERE number = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (card_number,))
        row = cur.fetchone()
        return False if row is None else row[0] == card_pin

    def is_valid_card_number(self, card_number):
        sql = ''' SELECT 1 FROM card WHERE number = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (card_number,))
        row = cur.fetchone()
        return row is not None

    def get_amount(self, card_number):
        sql = ''' SELECT balance FROM card WHERE number = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (card_number,))
        row = cur.fetchone()
        return row[0]

    def add_to_card_balance(self, card_number, income):
        sql = ''' UPDATE card SET balance = balance + ? WHERE number = ? '''
        cur = self.conn.cursor()
        cur.execute(sql, (income, card_number))
        self.conn.commit()

    def get_card_numbers(self):
        sql = ''' SELECT number FROM card; '''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def delete_card(self, card_number):
        sql = ''' DELETE FROM card WHERE number = card_number '''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()


class SBS:

    def __init__(self):
        self.db = DataBase()
        self.go_on = True
        self.active_card = None

    def run(self):
        while self.go_on:
            self.get_menu_option()()

    def get_menu_option(self):

        if self.active_card:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            while True:
                option = input().strip()
                if option in ('1', '2', '3', '4', '5', '0'):
                    break
                else:
                    print('No such option. Please try again.')

            return {'1': self.show_balance,
                    '2': self.add_income,
                    '3': self.do_transfer,
                    '4': self.close_account,
                    '5': self.log_out,
                    '0': self.exit,
                    }[option]
        else:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            while True:
                option = input().strip()
                if option in ('1', '2', '0'):
                    break
                else:
                    print('No such option. Please try again.')

            return {'1': self.create_account,
                    '2': self.log_into_account,
                    '0': self.exit,
                    }[option]

    def create_account(self):
        card = Card()
        self.db.create_card(card)
        print(f'\nYour card has been created\n'
              f'Your card number:\n{card.number}\n'
              f'Your card PIN:\n{card.pin}\n')

    def log_into_account(self):
        print('\nEnter your card number:')
        card_number = input().strip()
        print('Enter your PIN:')
        card_pin = input().strip()
        if self.db.is_valid_card_pin(card_number, card_pin):
            print('\nYou have successfully logged in!\n')
            self.active_card = card_number
        else:
            print('\nWrong card number or PIN!\n')

    def show_balance(self):
        print(f'\nBalance: {self.db.get_amount(self.active_card)}\n')

    def add_income(self):
        print('\nEnter income:')
        income = int(input().strip())
        self.db.add_to_card_balance(self.active_card, income)
        print('Income was added!\n')

    def do_transfer(self):
        print('\nTransfer')
        print('Enter card number:')
        card_number = input()
        if card_number == self.active_card:
            print("You can't transfer money to the same account!\n")
            return
        if not Card.is_valid_card_number(card_number):
            print('Probably you made a mistake in the card number. Please try again!\n')
            return
        if not self.db.is_valid_card_number(card_number):
            print('Such a card does not exist.\n')
            return
        print('Enter how much money you want to transfer:')
        money_to_transfer = int(input())
        if self.db.get_amount(self.active_card) < money_to_transfer:
            print('Not enough money!\n')
            return
        self.db.add_to_card_balance(self.active_card, (-1) * money_to_transfer)
        self.db.add_to_card_balance(card_number, money_to_transfer)
        print('Success!\n')

    def close_account(self):
        self.db.delete_card(self.active_card)
        print('The account has been closed!')

    def log_out(self):
        self.active_card = None
        print('\nYou have successfully logged out!\n')

    def exit(self):
        self.go_on = False
        print('\nBye!')


if __name__ == '__main__':

    atm = SBS()
    atm.run()
