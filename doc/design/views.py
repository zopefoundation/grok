import grok

grok.templatedir('calc_templates')  # this is actually the default (from module name, calc.py)

class Calculator(grok.Model):
    pass

class Sum(grok.View):
    """Simple view for a model"""
    grok.context(Calculator)  # this is actually the default (from module)
    grok.template('sum')  # this is actually the default (from class name)
    grok.name('sum')  # this is actually the default (from class name)
    grok.require('zope.Public')  # this is actually the default

    def calculateSum(self):
        """you can pull this in the template through view/calculateSum"""

    def update(self):    
        """executed before the template is rendered"""
        self.sum = self.calculateSum()
        self.sendEmail()

    def sendEmail(self):
        """send an email here"""

class PDFSum(grok.View):

    def update(self):
        pass

    def render(self):
        return pdfdata

sum = grok.PageTemplate("""\
<p tal:content="view/calculateSum">...</p>
<p tal:content="view/precalculatedSum">...</p>
""")


from zope import schema

class Index(grok.Form):
    """a form

    this is the default view for the Calculator model (because it's
    called Index)
    """

    class fields:
        operand = schema.Int(title=u'Operand')
        operator = schema.Choice(...)
        operand2 = schema.Int(...)

    @grok.action('Calculate')
    def calculate(self, operand, operator, operand2):
        """it's possible to receive any number of form fields in any
        order, or just use **kw to receive them all in a dict"""
        self.result = operator(operand, operand2)

    # this will raise a helpful error message at startup time (encoded
    # strings)
    @grok.action('Bהההה')
    def whatever(self, **data):
        pass

index = grok.PageTemplate("""\
<form tal:attributes="action request/URL">
<p tal:condition="exists:view/result">
  The result is: <span tal:replace="view/result" />
</p>

XXX render fields
XXX render actions
</form>
""")

class CalculatorXMLRPC(grok.XMLRPC):

    @grok.require('zope.Public')  # this is actually the default
    def sum(self, operand, operator, operand2):
        return ...

    @grok.require('something.else')
    def whatever(self):
        return ...
