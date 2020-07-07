import sys


class Coffee:

    def __init__(self, water=0, milk=0, beans=0, price=0):
        self.water = water
        self.milk = milk
        self.beans = beans
        self.price = price


class CoffeeMachine:
    '''Simulating coffee machine.'''

    ESPRESSO = Coffee(water=250, beans=16, price=4)
    LATTER = Coffee(water=350, milk=75, beans=20, price=7)
    CAPPUCCINO = Coffee(water=200, milk=100, beans=12, price=6)

    def __init__(self):
        self.money_stock = 550
        self.water_stock = 400
        self.milk_stock = 540
        self.beans_stock = 120
        self.disposable_caps_stock = 9
        self.action = None
        self.coffee_type = None

    def show_state(self):
        print('\nThe coffee machine has:')
        print(f'{self.water_stock} of water')
        print(f'{self.milk_stock} of milk')
        print(f'{self.beans_stock} of coffee beans')
        print(f'{self.disposable_caps_stock} of of disposable cups')
        print(f'${self.money_stock} of money')
        print()

    def get_action(self):
        self.action = input('Write action (buy, fill, take, remaining, exit):\n')

    def dispatch(self):
        if self.action == 'buy':
            self.make_coffee()
        elif self.action == 'fill':
            self.fill_supplies()
        elif self.action == 'take':
            self.take_money()
        elif self.action == 'remaining':
            self.show_state()
        elif self.action == 'exit':
            sys.exit()
        else:
            raise NameError('Wrong action')

    def make_coffee(self):
        self.coffee_type = input('\nWhat do you want to buy? '
                                     '1 - espresso, '
                                     '2 - latte, '
                                     '3 - cappuccino'
                                     'back - to main menu:\n')
        if self.coffee_type == '1':
            coffee = CoffeeMachine.ESPRESSO
        elif self.coffee_type == '2':
            coffee = CoffeeMachine.LATTER
        elif self.coffee_type == '3':
            coffee = CoffeeMachine.CAPPUCCINO
        elif self.coffee_type == 'back':
            return
        else:
            raise NameError('Wrong coffee type')

        failure = []
        if self.water_stock < coffee.water:
            failure.append('water')
        elif self.milk_stock < coffee.milk:
            failure.append('milk')
        elif self.beans_stock < coffee.beans:
            failure.append('coffee beans')
        elif self.disposable_caps_stock < 1:
            failure.append('disposable cap')

        if failure:
            print('Sorry, not enough ' + ' and '.join(failure) + '!\n')
        else:
            print('I have enough resources, making you a coffee!\n')
            self.water_stock -= coffee.water
            self.milk_stock -= coffee.milk
            self.beans_stock -= coffee.beans
            self.disposable_caps_stock -= 1
            self.money_stock += coffee.price

    def fill_supplies(self):
        print()
        self.water_stock += int(input('Write how many ml of water do you want to add:\n'))
        self.milk_stock += int(input('Write how many ml of milk do you want to add:\n'))
        self.beans_stock += int(input('Write how many grams of coffee beans do you want to add:\n'))
        self.disposable_caps_stock += int(input('Write how many disposable cups of coffee do you want to add:\n'))
        print()

    def take_money(self):
        print()
        print(f'I gave you ${self.money_stock}\n')
        self.money_stock = 0

    def run(self):

        while True:
            self.get_action()
            self.dispatch()


if __name__ == '__main__':

    CoffeeMachine().run()
