import unittest
from pkg_resources import resource_listdir
from zope.testing import doctest
from zope.app.testing.functional import (HTTPCaller, getRootFolder,
                                         FunctionalTestSetup, sync, Functional)

# XXX bastardized from zope.app.testing.functional.FunctionalDocFileSuite :-(
def FunctionalDocTestSuite(*paths, **kw):
    globs = kw.setdefault('globs', {})
    globs['http'] = HTTPCaller()
    globs['getRootFolder'] = getRootFolder
    globs['sync'] = sync

    #kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        FunctionalTestSetup().setUp()

        if kwsetUp is not None:
            kwsetUp(test)
    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        if kwtearDown is not None:
            kwtearDown(test)
        FunctionalTestSetup().tearDown()
    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.REPORT_NDIFF
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocTestSuite(*paths, **kw)
    suite.layer = Functional
    return suite

def test_suite():
    suite = unittest.TestSuite()
    from adder.ftests import index_view
    test = FunctionalDocTestSuite(index_view)
    suite.addTest(test)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
