import io
import random
import sys


class RockPaperScissors:

    game_results_filename = 'rating.txt'

    def __init__(self):
        self.rock = 'rock'
        self.paper = 'paper'
        self.scissors = 'scissors'
        self.options = [self.rock, self.paper, self.scissors]
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
                    self.results[name] = score
        except FileNotFoundError:
            pass

    def store_results(self):
        with open(RockPaperScissors.game_results_filename, 'w') as f:
            f.write('\n'.join(f'{name} {score}' for name, score in self.results.items()))

    def get_result(self, user_option):
        """ Return 0, 1, 2 for users Lose, Draw, Win """
        res = (self.options.index(self.computer_option) - self.options.index(user_option) + 3) % 3
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
            # print(f'My choice: {user_option}')  # for testing
            # print(f'Computer choice: {self.computer_option}')  # for testing
            result = ('Draw', 'Lose', 'Win')[self.get_result(user_option)]
            self.results[self.user_name] = (
                self.results.setdefault(self.user_name, 0) + {'Draw': 50, 'Lose': 0, 'Win': 100}[result]
                )
            self.print_result(result)

        self.store_results()

    def test_run(self):
        tmp_stdin = sys.stdin
        input_str = '\n'.join(random.sample(self.options * 4, 10))
        sys.stdin = io.StringIO(input_str)
        while sys.stdin:
            try:
                self.run()
            except EOFError:
                break
        sys.stdin = tmp_stdin


if __name__ == '__main__':

    RockPaperScissors().run()
