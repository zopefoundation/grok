"""
This should fail:
"""
import grok

class MultipleNames(grok.View):
    grok.name('mammoth')
    grok.name('bear')
