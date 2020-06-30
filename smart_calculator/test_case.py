def function_to_test(*args):
    """Mockup function for test."""
    return str(*args)


def test_case_run(f, test_case):

    np = [0, 0]  # [False, True]
    w0 = w1 = w2 = 0

    for test, check in test_case.items():
        t = str(f(test))
        np[t == check] += 1
        w0 = len(str(test)) if w0 < len(str(test)) else w0
        w1 = len(str(t)) if w1 < len(str(t)) else w1
        w2 = len(str(check)) if w2 < len(str(check)) else w2
        print(f'Check: {test:{w0}}'
              f'\tResult: {t:{w1}}'
              f'\tExpected: {check:{w2}}'
              f'\tTest: {"Ok" if t == check else "Fail"}'
        )

    msg = (
        f'\nTesting "{f.__name__}(...)" failed. {np[True]} tests passed, {np[False]} tests failed.',
        f'\nTesting "{f.__name__}(...)" complete. All {np[True]} tests is OK.',
    )[np[False] == 0]

    print(msg)


if __name__ == '__main__':

    test_case = {
        '1': '1',
        'a': 'a',
        'Test string': 'Test string',
    }

    test_case_run(function_to_test, test_case)