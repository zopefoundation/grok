"""
Forms cannot define a render method. Here we show the case where the
EditForm has no explicit template associated with it:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
  ...
  GrokError: It is not allowed to specify a custom 'render' method for
  form <class 'grok.tests.form.norender2.Edit'>. Forms either use the default
  template or a custom-supplied one.
  
"""

import grok

class Mammoth(grok.Model):
    pass

class Edit(grok.EditForm):
    # not allowed to have a render method
    def render(self):
        return "this cannot be"
