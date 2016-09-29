import re
import unittest, doctest
import grok

from pkg_resources import resource_listdir
from zope.testing import renormalizing

import zope.testbrowser.wsgi
import zope.app.wsgi.testlayer


layer = zope.app.wsgi.testlayer.BrowserLayer(grok)

checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    (re.compile(
        r'^WrongType: '),
        'zope.schema._bootstrapinterfaces.WrongType: '),
    (re.compile(
        r'^ComponentLookupError: '),
        'zope.interface.interfaces.ComponentLookupError: '),
    (re.compile(
        r'^HTTPError: '),
        'urllib.error.HTTPError: '),
    (re.compile(
        r'^ForbiddenAttribute: '),
        'zope.security.interfaces.ForbiddenAttribute: '),
    (re.compile(
        r'^NotFound: '),
        'zope.publisher.interfaces.NotFound: '),
    ])

def http_call(method, path, data=None, **kw):
    """Function to help make RESTful calls.

    method - HTTP method to use
    path - testbrowser style path
    data - (body) data to submit
    kw - any request parameters
    """

    if path.startswith('http://localhost'):
        path = path[len('http://localhost'):]
    request_string = '%s %s HTTP/1.1\n' % (method, path)
    for key, value in kw.items():
        request_string += '%s: %s\n' % (key, value)
    if data is not None:
        request_string += '\r\n'
        request_string += data
    return zope.app.wsgi.testlayer.http(request_string, handle_errors=False)


def bprint(data):
    """Python 2 and 3 doctest compatible print.

    http://python3porting.com/problems.html#string-representation
    """
    if not isinstance(data, str):
        data = data.decode()
    print(data.strip())


def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        dottedname = 'grok.ftests.%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            checker=checker,
            extraglobs=dict(
                http_call=http_call,
                wsgi_app=layer.make_wsgi_app,
                http=zope.app.wsgi.testlayer.http,
                print=bprint,
                getRootFolder=layer.getRootFolder),
            optionflags=(
                doctest.ELLIPSIS+
                doctest.NORMALIZE_WHITESPACE+
                doctest.REPORT_NDIFF)
                )
        test.layer = layer
        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in [
        'catalog',
        'chameleon',
        'errorviews',
        'form',
        'forms',
        'lifecycle',
        'security',
        'site',
        'traversal',
        'url',
        'viewlet',
        ]:
        suite.addTest(suiteFromPackage(name))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
