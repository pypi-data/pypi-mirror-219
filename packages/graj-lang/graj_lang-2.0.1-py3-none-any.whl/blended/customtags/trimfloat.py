import math

class trimfloat(float):
    def __str__(self):
        """
        Format a float so it prints like PHP and JavaScript, with no trailing zeroes.
        """
        return ('%f' % self).rstrip('0').rstrip('.')
        #('%f' % self).rstrip('0').rstrip('.') 

    def __repr__(self):
        """
        Format a float so it prints like PHP and JavaScript, with no trailing zeroes.
        """
        
        return ('%f' % self).rstrip('0').rstrip('.')

    def __pos__(self):
        """
        Implements behavior for unary positive (e.g. +some_object)
        """
        
        return self.__class__(float.__pos__(self))

    def __neg__(self):
        """
        Implements behavior for negation (e.g. -some_object)
        """

        return self.__class__(float.__neg__(self))

    def __abs__(self):
        """
        Implements behavior for the built in abs() function.
        """

        return self.__class__(float.__abs__(self))

    def __round__(self, ndigits=0):
        """
        Implements behavior for the built in round() function. 
        n is the number of decimal places to round to.
        """
        
        cust_self = float(self)
        return round(cust_self, ndigits)

    def __floor__(self):
        """
        Implements behavior for math.floor(), i.e., rounding down to the nearest integer.
        """
        
        cust_self = float(self)
        return self.__class__(math.floor(cust_self))

    def __ceil__(self):
        """
        Implements behavior for math.ceil(), i.e., rounding up to the nearest integer.
        """
        
        cust_self = float(self)
        return self.__class__(math.ceil(cust_self))

    def __trunc__(self):
        """
        Implements behavior for math.trunc(), i.e., truncating to an integral.
        """
        
        return self.__class__(math.trunc(self))

    def __add__(self, other):
        """
        Implements addition.
        """
        
        return self.__class__(float.__add__(self, other))

    def __sub__(self, other):
        """
        Implements subtraction.
        """
        
        return self.__class__(float.__sub__(self, other))

    def __mul__(self, other):
        """
        Implements multiplication.
        """
        return self.__class__(float.__mul__(self, other))

    def __floordiv__(self, other):
        """
        Implements integer division using the // operator.
        """
       
        return self.__class__(float.__floordiv__(self, other))

    def __div__(self, other):
        """
        Implements division using the / operator.
        """
        return self.__class__(float.__div__(self, other))

    def __truediv__(self, other):
        """
        Implements true division. Note that this only works when 
        from __future__ #import division is in effect.
        """
        return self.__class__(float.__truediv__(self, other))

    def __mod__(self, other):
        """
        Implements modulo using the % operator.
        """
        return self.__class__(float.__mod__(self, other))

    def __divmod__(self, other):
        """
        Implements behavior for long division using the divmod() built in function.
        """
        div, mod = float.__divmod__(self, other)
        return self.__class__(div), self.__class__(mod)

    def __pow__(self, other):
        """
        Implements behavior for exponents using the ** operator.
        """
        return self.__class__(float.__pow__(self, other))

    def __radd__(self, other):
        """
        Implements reflected addition.
        """
        return self.__class__(float.__radd__(self, other))

    def __rsub__(self, other):
        """
        Implements reflected subtraction.
        """
        other = float(str(other))
        return self.__class__(float.__rsub__(self, other))

    def __rmul__(self, other):
        """
        Implements reflected multiplication.
        """
        try:
            other = float(str(other))
            return self.__class__(float.__rmul__(self, other))
        except ValueError:
            raise TypeError("can't multiply sequence by non-int of type 'float'")

    def __rfloordiv__(self, other):
        """
        Implements reflected integer division using the // operator.
        """
        return self.__class__(float.__rfloordiv__(self, other))

    def __rdiv__(self, other):
        """
        Implements reflected division using the / operator.
        """
        return self.__class__(float.__rdiv__(self, other))

    def __rtruediv__(self, other):
        """
        Implements reflected true division. Note that this only works when 
        from __future__ #import division is in effect.
        """
        return self.__class__(float.__rtruediv__(self, other))

    def __rmod__(self, other):
        """
        Implements reflected modulo using the % operator.
        """
        return self.__class__(float.__rmod__(self, other))

    def __rdivmod__(self, other):
        """
        Implements behavior for long division using the divmod() built in function, 
        when divmod(other, self) is called.
        """
        div, mod = float.__rdivmod__(self, other)
        return self.__class__(div), self.__class__(mod)

    def __rpow__(self, other):
        """
        Implements behavior for reflected exponents using the ** operator.
        """
        return self.__class__(float.__rpow__(self, other))

    def __index__(self):
        """
        When you are using a trimfloat as an index, it needs to act like an int.
        """
        return int(self)

'''
class trimint
'''

class trimint(int):
    def __str__(self):
        """
        Format a float so it prints like PHP and JavaScript, with no trailing zeroes.
        """
        return ('%f' % self).rstrip('0').rstrip('.')

    def __repr__(self):
        """
        Format a float so it prints like PHP and JavaScript, with no trailing zeroes.
        """
        return ('%f' % self).rstrip('0').rstrip('.')

    def __pos__(self):
        """
        Implements behavior for unary positive (e.g. +some_object)
        """

        return self.__class__(int.__pos__(self))

    def __neg__(self):
        """
        Implements behavior for negation (e.g. -some_object)
        """

        return self.__class__(int.__neg__(self))

    def __abs__(self):
        """
        Implements behavior for the built in abs() function.
        """

        return self.__class__(int.__abs__(self))

    def __add__(self, other):
        """
        Implements addition.
        """

        result = int.__add__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __sub__(self, other):
        """
        Implements subtraction.
        """

        result = int.__sub__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __mul__(self, other):
        """
        Implements multiplication.
        """
        result = int.__mul__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __floordiv__(self, other):
        """
        Implements integer division using the // operator.
        """

        return trimfloat.__floordiv__(trimfloat(self), other)

    def __div__(self, other):
        """
        Implements division using the / operator.
        """
        return trimfloat.__div__(trimfloat(self), other)

    def __truediv__(self, other):
        """
        Implements true division. Note that this only works when
        from __future__ #import division is in effect.
        """
        return trimfloat.__truediv__(trimfloat(self), other)

    def __mod__(self, other):
        """
        Implements modulo using the % operator.
        """
        result = int.__mod__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __divmod__(self, other):
        """
        Implements behavior for long division using the divmod() built in function.
        """
        return trimfloat.__divmod__(trimfloat(self), other)

    def __pow__(self, other):
        """
        Implements behavior for exponents using the ** operator.
        """
        result = int.__pow__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __radd__(self, other):
        """
        Implements reflected addition.
        """
        result = int.__radd__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __rsub__(self, other):
        """
        Implements reflected subtraction.
        """
        result = int.__rsub__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __rmul__(self, other):
        """
        Implements reflected multiplication.
        """
        #return trimfloat.__rmul__(trimfloat(self), other)
        try:
            other = int(str(other))
            return self.__class__(int.__rmul__(self, other))
        except ValueError:
            return super(trimint, self).__rmul__(other)

    def __rfloordiv__(self, other):
        """
        Implements reflected integer division using the // operator.
        """
        return trimfloat.__rfloordiv__(trimfloat(self), other)

    def __rdiv__(self, other):
        """
        Implements reflected division using the / operator.
        """
        return trimfloat.__rdiv__(trimfloat(self), other)

    def __rtruediv__(self, other):
        """
        Implements reflected true division. Note that this only works when
        from __future__ #import division is in effect.
        """
        return trimfloat.__rtruediv__(trimfloat(self), other)

    def __rmod__(self, other):
        """
        Implements reflected modulo using the % operator.
        """
        result = int.__rmod__(self, other)
        return result if result is NotImplemented else self.__class__(result)

    def __rdivmod__(self, other):
        """
        Implements behavior for long division using the divmod() built in function,
        when divmod(other, self) is called.
        """
        return trimfloat.__rdivmod__(trimfloat(self), other)

    def __rpow__(self, other):
        """
        Implements behavior for reflected exponents using the ** operator.
        """
        result = int.__rpow__(self, other)
        return result if result is NotImplemented else self.__class__(result)

