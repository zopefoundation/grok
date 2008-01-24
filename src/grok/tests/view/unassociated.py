"""
Templates that are not associated with a view class will provoke an
error:

  >>> from zope.deprecation.tests import warn
  >>> import warnings
  >>> saved_warn = warnings.warn
  >>> warnings.warn = warn

  >>> grok.testing.grok(__name__)
  From tests.py's showwarning():
  ...UserWarning: Found the following unassociated template(s) when grokking
  'grok.tests.view.unassociated': index.  Define view classes inheriting from
  grok.View to enable the template(s).

  >>> warnings.warn = saved_warn

"""
import grok

class Mammoth(grok.Model):
    pass
