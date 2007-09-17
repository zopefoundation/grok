"""
Templates that are not associated with a view class will provoke an
error:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
  ...
  GrokError: Found the following unassociated template(s) when grokking
  'grok.tests.view.unassociated': index.  Define view classes inheriting
  from grok.View to enable the template(s).


"""
import grok

class Mammoth(grok.Model):
    pass
