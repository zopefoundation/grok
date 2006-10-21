"""
A template directory may only contain recognized template files:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Unrecognized file 'invalid.txt' in template directory '...dirtemplatesonly_templates'.
"""
import grok

class Mammoth(grok.Model):
    pass
