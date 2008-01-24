import grok

class Appointment(grok.Model):
    pass

class Day(grok.Model):

    def getAppointment(self, number):
        if number in self.appointments:
            return Appointment(number)
        return None # try to look up views then

    def traverse(self, name):
        return self.getAppointment(int(number))
    
class Calendar(grok.Model):
    def getYear(self, year):
        return Year(year)

    def traverse(self, name):
        return self.getYear(int(number))

# interpretation of traverse:

# * do the traverse traversal first

# * if this raises an error, propagate exception, do not swallow it (test)

# * if this returns None, fall back on "normal" traversal for the
    object (i.e. container traversal)

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
