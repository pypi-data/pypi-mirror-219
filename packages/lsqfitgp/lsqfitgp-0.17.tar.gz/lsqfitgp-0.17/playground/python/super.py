class cippa:
    
    def __init_subclass__(cls):
        cls.cippa = 'original cippa'
    
class lippa:
    
    def __init_subclass__(cls):
        cls.cippa = 'fake cippa'

class fagiolino(cippa, lippa):
    
    def __init_subclass__(cls):
        pass