import io
import random
import sys


class RockPaperScissors:

    game_results_filename = 'rating.txt'

    def __init__(self):
        self.options = ['rock', 'paper', 'scissors']
        self.computer_option = None
        self.user_name = None
        self.results = {}

    def greet(self):
        print('Enter your name:', end=' ')
        self.user_name = input()
        print(f'Hello, {self.user_name}')

    def load_results(self):
        try:
            with open(RockPaperScissors.game_results_filename) as f:
                for line in f.readlines():
                    name, score = line.split()
                    self.results[name] = int(score)
        except FileNotFoundError:
            pass

    def load_options(self):
        options_str = input()
        if options_str:
            self.options = options_str.split(',')
        print("Okay, let's start")

    def store_results(self):
        with open(RockPaperScissors.game_results_filename, 'w') as f:
            f.write('\n'.join(f'{name} {score}' for name, score in self.results.items()))

    def get_result(self, user_option):

        res = None

        u_idx = self.options.index(user_option)
        c_idx = self.options.index(self.computer_option)

        u_cap_idx = (u_idx + len(self.options) // 2) % len(self.options)  # index of an option opposite to user option

        if u_idx == c_idx:
            res = 'Draw'
        elif u_idx < u_cap_idx:
                res = 'Lose' if u_idx < c_idx <= u_cap_idx else 'Win'
        elif u_idx > u_cap_idx:
                res = 'Win' if u_cap_idx < c_idx < u_idx else 'Lose'

        return res

    def print_result(self, result):
        print({
                  'Lose': f'Sorry, but computer chose {self.computer_option}',
                  'Draw': f'There is a draw ({self.computer_option})',
                  'Win': f'Well done. Computer chose {self.computer_option} and failed',
              }[result])

    def run(self):

        self.greet()
        self.load_results()
        self.load_options()

        while True:

            user_option = input().strip()

            if user_option == '!exit':
                print('Bye!')
                break
            if user_option == '!rating':
                print(f'Your rating: {self.results.get(self.user_name, 0)}')
                continue
            if user_option not in self.options:
                print('Invalid input')
                continue

            self.computer_option = random.choice(self.options)

            result = self.get_result(user_option)
            self.results[self.user_name] = (self.results.setdefault(self.user_name, 0)
                                            + {'Draw': 50, 'Lose': 0, 'Win': 100}[result])
            self.print_result(result)

        self.store_results()


if __name__ == '__main__':

    RockPaperScissors().run()
