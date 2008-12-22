"""

The JSON grokker registers a view for each method of the JSON class. These
"method" views support layers and skins.

  >>> grok.testing.grok(__name__)
  >>> mammoth = Mammoth()
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> jsonlayer_request = TestRequest(skin=IMyJSONLayer)

The 'run' view on the default skin::

  >>> view = getMultiAdapter((mammoth, request), name='run')
  >>> view()
  '{"me": "grok"}'

The 'run' on the my_json skin::

  >>> view = getMultiAdapter((mammoth, jsonlayer_request), name='run')
  >>> view()
  '{"shadows": "run on the default layer"}'

The 'another' view on the default skin, not available on the my_json::

  >>> view = getMultiAdapter((mammoth, request), name='public')
  >>> view()
  '{"public": "only availble on the default layer"}'

  >>> view = getMultiAdapter((mammoth, jsonlayer_request), name='public')
  Traceback (most recent call last):
  ...
  ComponentLookupError: ((<grok.tests.json.json_layers.Mammoth object at ...>,
  <zope.publisher.browser.TestRequest instance URL=http://127.0.0.1>),
  <InterfaceClass zope.interface.Interface>, 'public')

The 'public' view not available on the default skin, available on
the my_json skin::

  >>> view = getMultiAdapter((mammoth, request), name='another')
  Traceback (most recent call last):
  ...
  ComponentLookupError: ((<grok.tests.json.json_layers.Mammoth object at ...>,
  <zope.publisher.browser.TestRequest instance URL=http://127.0.0.1>),
  <InterfaceClass zope.interface.Interface>, 'another')

  >>> view = getMultiAdapter((mammoth, jsonlayer_request), name='another')
  >>> view()
  '{"another": "only available on my json layer"}'

Like with "normal" view, layers can aggregate view "methods"::

  >>> second_jsonlayer_request = TestRequest(skin=IMySecondJSONLayer)
  >>> view = getMultiAdapter((mammoth, second_jsonlayer_request), name='run')
  >>> view()
  '{"shadows": "run on the IMyJSONLayer layer"}'

  >>> view = getMultiAdapter(
  ...     (mammoth, second_jsonlayer_request), name='another')
  >>> view()
  '{"another": "only available on my json layer"}'

  >>> view = getMultiAdapter(
  ...     (mammoth, second_jsonlayer_request), name='yetanother')
  >>> view()
  '{"another": "only available on my second json layer"}'

"""

import grok

class IMyJSONLayer(grok.IBrowserRequest):
    grok.skin('my_json')

class Mammoth(grok.Model):
    pass

class MammothView(grok.JSON):
    grok.context(Mammoth)

    def run(self):
        return {'me': 'grok'}

    def public(self):
        return {'public': 'only availble on the default layer'}

class AnotherMammothView(grok.JSON):
    grok.context(Mammoth)
    grok.layer(IMyJSONLayer)

    def run(self):
        return {'shadows': 'run on the default layer'}

    def another(self):
        return {'another': 'only available on my json layer'}

class IMySecondJSONLayer(IMyJSONLayer):
    # Aggregates views on the first layer and adds more.
    grok.skin('my_second_json')

class YetAnotherMammothView(grok.JSON):
    grok.context(Mammoth)
    grok.layer(IMySecondJSONLayer)

    def run(self):
        return {'shadows': 'run on the IMyJSONLayer layer'}

    def yetanother(self):
        return {'another': 'only available on my second json layer'}
