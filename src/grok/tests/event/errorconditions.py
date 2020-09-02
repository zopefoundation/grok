"""
@grok.subscribe can only be used on module level:

  >>> function_context()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: @grok.subscribe can only be used on module level.

  >>> class_context()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: @grok.subscribe can only be used on module level.


@grok.subscribe can not be called without arguments:

  >>> import grok.tests.event.errorconditions_fixture
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: @grok.subscribe requires at least one argument.

"""  # noqa: E501
import grok


def function_context():
    @grok.subscribe(grok.Model, grok.IObjectCreatedEvent)
    def subscriber():
        pass


def class_context():
    class Wrapper:
        @grok.subscribe(grok.Model, grok.IObjectCreatedEvent)
        def subscriber(self):
            pass
