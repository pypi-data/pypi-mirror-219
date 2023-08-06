class cippa: pass
class lippa: pass
class fagiolino(cippa): pass

fagiolino.__bases__ = (cippa, lippa)
