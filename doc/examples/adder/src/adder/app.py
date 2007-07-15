import grok
from persistent.list import PersistentList

class Adder(grok.Application, grok.Model):
    """An adding machine with tape
    
    >>> adder = Adder()
    >>> adder.total
    0.0
    >>> adder.addTerm(0)
    0.0
    >>> '%.2f' % adder.addTerm(1.2)
    '1.20'
    >>> '%.2f' % adder.addTerm(-1)
    '0.20'
    
    Besides adding, Adder also contains a history of the added terms
    
    >>> ['%.2f' % term for term in adder.terms]
    ['0.00', '1.20', '-1.00']
    
    """
    def __init__(self):
        super(Adder, self).__init__()
        self.message = None
        self.clear()

    def clear(self):
        self.terms = PersistentList()
        self.total = 0.0

    def addTerm(self, term):
        self.terms.append(term)
        self.total += term
        return self.total

class Index(grok.View):
    message = None

    def update(self, term=None):
        if self.request.has_key('bt_clear'):
            self.context.clear()
        elif term:
            try:
                term = float(term)
            except ValueError:
                self.message = "Invalid number."
            else:
                self.context.addTerm(term)
