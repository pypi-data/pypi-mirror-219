class SingletonMeta(type):
    
    def __repr__(cls):
        return cls.__name__

class Singleton(metaclass=SingletonMeta):
    
    def __new__(cls):
        raise NotImplementedError(f"{cls.__name__} can not be instantiated")

class Cippa(Singleton):
    """cippa"""
    pass
