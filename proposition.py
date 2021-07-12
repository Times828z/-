class proposition:
    def __init__(self, name, val):
        self.val = val
        self.name = name

    def __and__(self, other):
        if type(other) is proposition:
            return self.val and other.val
        elif type(other) is bool:
            return self.val and other
        elif type(self) is bool:
            return self and other.val

    def __or__(self, other):
        if type(other) is proposition:
            return self.val or other.val
        elif type(other) is bool:
            return self.val or other
        elif type(self) is bool:
            return self or other.val

    def __invert__(self):
        return not self.val

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if other is str:
            return False
        if self.val == other.val and self.name == other.name:
            return True
        else:
            return False

a = proposition("a", False)
b = proposition("b", True)
c = proposition("c", False)

D = (a.val&b.val)&c.val
a.__and__(b)