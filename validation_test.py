def validationrule(method):
    def decorate(*args):
        print "%s : %s" %(method.__doc__, method(*args))
    return decorate

class ProductOne:
    a = 12
    b = 15

    @validationrule
    def a_lt_b(cls):
        """a is less than b"""   
        return cls.a < cls.b

class ProductTwo:
    a = 7
    b = 18
    @validationrule
    def a_lt_b(cls):
        """a is less than b"""
        return cls.a < cls.b

class AggregateProduct(ProductOne, ProductTwo):

    @validationrule
    def a_ne_a(cls):
        """ProductOne.a is not equal to ProductTwo.a"""
        return ProductOne.a != ProductTwo.a

    @validationrule
    def b_ne_b(cls):
        """ProductOne.b is not equal to ProductTwo.b"""
        return ProductOne.b != ProductTwo.b

