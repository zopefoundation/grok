import grok

class Appointment(grok.Model):
    pass

class Day(grok.Model):

    @grok.traverse
    def getAppointment(self, number):
        if number in self.appointments:
            return Appointment(number)
        return None # try to look up views then

class Calendar(grok.Model):

    @grok.traverse
    def getYear(self, year):
        return Year(year)


"""
http://.../calendar/2006/10/13/1/
           ^^^^^^^^ ^^^^ ^^ ^^ ^
            Cal.    Year  ...  A.
"""

#XXX routes (http://routes.groovie.org/) for advanced cases


# instead of traverser on the model, you can also write a separate
# traverser component:

class CalendarTraverser(grok.Traverser):
    grok.context(Calendar)  # this is actually the default
    grok.register(site=CalendarApp)  #...

    def traverse(self, name):
        now look up stuff on self.context with 'name'...
        return that
