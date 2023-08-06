"""Provides a convenient and standard way to represent frequency values.
The classes in this module are subclasses of float,
which means that you can use instances of them just like regular numbers, but they have some additional features.
Example usage:

foo = kHz(4)
foo += 1.2
print(foo) # prints 1.204 because if units aren't specified everything is done in MHz
print(foo.in_hz) # prints 1204000.0
foo += GHz('3')
print(foo.in_ghz) # prints 3.001204
"""

from functools import partial


__version__ = '1.0.0'

class Frequency(float):
    """Represents a generic frequency value.
    The constructor allows you to specify a unit, and you may access the value with convenience properties like in_khz.
    Directly accessing the value results in a megahertz value.
    """
    prefixes = {
        '': 1e-6, 'k': 1e-3, 'm': 1, 'g': 1e3, 'p': 1e6
    }

    def __new__(cls, scalar, units: str = 'MHz'):
        """
        :param scalar: something you could pass to float()
        :param units: a string like "G" or "kHz". "MHz" and "mHz" both result in megahertz and not millihertz.
        """
        scalar = float(scalar)

        units = units.lower().replace('hz', '').strip()
        if units not in cls.prefixes:
            raise ValueError(f'Invalid SI prefix given: "{units}"')

        scalar *= cls.prefixes[units]

        return super().__new__(cls, scalar)

    @property
    def in_hz(self) -> float:
        return float(self / self.prefixes[''])

    @property
    def in_khz(self) -> float:
        return float(self / self.prefixes['k'])

    @property
    def in_mhz(self) -> float:
        return float(self / self.prefixes['m'])

    @property
    def in_ghz(self) -> float:
        return float(self / self.prefixes['g'])

    def __str__(self):
        for prefix, divisor in sorted(self.prefixes.items(), key=lambda key_value: key_value[1], reverse=True):
            if abs(self / divisor) >= 1:
                return f'{self / divisor:.2f} {prefix.upper()}Hz'

        return f'{self / self.prefixes[""]:.3e} Hz'

    # The following methods are needed so that doing math operations on Frequency values
    # results in Frequency values and not floats
    def __add__(self, other):
        return Frequency(super().__add__(other), 'MHz')

    def __abs__(self):
        return Frequency(super().__abs__(), 'MHz')

    def __ceil__(self):
        return Frequency(super().__ceil__(), 'MHz')

    def __divmod__(self, other):
        return Frequency(super().__divmod__(other), 'MHz')

    def __floor__(self):
        return Frequency(super().__floor__(), 'MHz')

    def __floordiv__(self, other):
        return Frequency(super().__floordiv__(other), 'MHz')

    def __mul__(self, other):
        return Frequency(super().__mul__(other), 'MHz')

    def __pow__(self, power, modulo=None):
        return Frequency(super().__pow__(power, modulo), 'MHz')

    def __mod__(self, other):
        return Frequency(super().__mod__(other), 'MHz')

    def __neg__(self):
        return Frequency(super().__neg__(), 'MHz')

    def __sub__(self, other):
        return Frequency(super().__sub__(other), 'MHz')


'''Hz(5) is shorthand for Frequency(5, 'Hz')'''
Hz = partial(Frequency, units='Hz')
KHz = kHz = partial(Frequency, units='KHz')
MHz = partial(Frequency, units='MHz')
GHz = partial(Frequency, units='GHz')
PHz = partial(Frequency, units='PHz')
