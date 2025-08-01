from numbers import Number


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree())
            # subtract the overlapping coefficients
            coefs = tuple(a - b for a, b in zip(self.coefficients,
                                                other.coefficients))
            # add the remaining coefficients
            coefs += self.coefficients[common+1:]  # leftover from self
            coefs += tuple(-c for c in other.coefficients[common+1:])
            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,)
                              + self.coefficients[1:])
        else:
            return NotImplemented

    def __rsub__(self, other):
        new_coefs = (
            (self.coefficients[0] * -1 + other,) +
            tuple(-c for c in self.coefficients[1:])
        )
        return Polynomial(new_coefs)

    def __mul__(self, other):
        if isinstance(other, Number):
            coefs = tuple(other * c for c in self.coefficients)
            return Polynomial(coefs)
        elif isinstance(other, Polynomial):
            coefs = [0] * (self.degree() + other.degree() + 1)
            for i, a in enumerate(self.coefficients):
                for j, b in enumerate(other.coefficients):
                    coefs[i+j] += a*b
            return Polynomial(tuple(coefs))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        from numbers import Integral
        if isinstance(other, Integral) and other > 0:
            start = self
            for i in range(other-1):
                start *= self
            return start
        else:
            NotImplemented

    def __call__(self, other):
        if isinstance(other, Number):
            sum = 0
            for i in range(self.degree() + 1):
                sum += self.coefficients[i]*other**i
            return sum
        else:
            return NotImplemented

    def dx(self):
        coefs = tuple((n+1)*c for n, c in enumerate(self.coefficients[1:]))
        if self.degree() == 0:
            coefs = (0,)
        return Polynomial(coefs)


def derivative(x):
    if isinstance(x, Polynomial):
        return x.dx()
