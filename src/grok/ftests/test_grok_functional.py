import doctest
import importlib.resources
import importlib.util
import pathlib
import unittest

import zope.app.wsgi.testlayer
import zope.testbrowser.wsgi

import grok
import grok.testing


class Layer(
        zope.testbrowser.wsgi.TestBrowserLayer,
        zope.app.wsgi.testlayer.BrowserLayer):
    pass


layer = Layer(grok)


def http_call(method, path, data=None, **kw):
    """Function to help make RESTful calls.

    method - HTTP method to use
    path - testbrowser style path
    data - (body) data to submit
    kw - any request parameters
    """

    if path.startswith('http://localhost'):
        path = path[len('http://localhost'):]
    request_string = f'{method} {path} HTTP/1.1\n'
    for key, value in kw.items():
        request_string += f'{key}: {value}\n'
    if data is not None:
        request_string += '\r\n'
        request_string += data
    return zope.app.wsgi.testlayer.http(request_string, handle_errors=False)


def suiteFromPackage(name):
    try:
        with importlib.resources.as_file(
                importlib.resources.files(__name__).joinpath(name)) as path:
            filenames = [f.name for f in pathlib.Path(path).iterdir()]
    except (AttributeError, TypeError):  # PY3.11 and below
        spec = importlib.util.find_spec(__name__)
        package_path = pathlib.Path(spec.origin).parent / name
        filenames = [f.name for f in package_path.iterdir()]
    suite = unittest.TestSuite()
    for filename in filenames:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        dottedname = f'grok.ftests.{name}.{filename[:-3]}'
        test = doctest.DocTestSuite(
            dottedname,
            extraglobs=dict(
                getRootFolder=layer.getRootFolder,
                http=zope.app.wsgi.testlayer.http,
                http_call=http_call,
                wsgi_app=layer.make_wsgi_app,
            ),
            optionflags=(
                doctest.ELLIPSIS +
                doctest.NORMALIZE_WHITESPACE +
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
