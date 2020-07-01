# env.py

# Environment or Table of symbols.


class Env:
    def __init__(self, prev):
        self.table = {}
        self.prev = prev

    def put(self, s, symbol):
        self.table[s] = symbol

    def get(self, s):
        e = self
        while e is not None:
            found = e.table.get(s)
            if found is not None:
                return found
            e = e.prev
        return None


e0 = Env(None)
e0.put('x', 0)
e1 = Env(e0)

print(e1.get('x'))  # 0 - returns x = 0 from upper scope
print(e1.get('y'))  # None - as y is not defined
