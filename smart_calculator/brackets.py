from collections import deque


def bracket_check(expr):

    bracket = deque()

    for c in expr:
        if c == '(':
            bracket.append(c)
        elif c == ')':
            if len(bracket) > 0:
                bracket.pop()
            else:
                return False

    return len(bracket) == 0


def test_case_run(f, test_case):

    np = [0, 0]  # [False, True]

    for test, check in test_case.items():
        t = f(test) == check
        np[t] += 1
        print(test, t, sep='\t')

    if np[False] == 0:
        msg = f'\nAll {np[True]} tests is OK.'
    else:
        msg = f'\nTestcase failed. {np[True]} tests passed, {np[False]} tests failed.'
    print(msg)


if __name__ == '__main__':

    test_case = {
        '(a + b)*c': True,
        '((a + b)*c': False,
        ')5*).((': False,
        '())(()': False,
    }

    test_case_run(bracket_check, test_case)
