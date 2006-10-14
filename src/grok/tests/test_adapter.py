import unittest
from zope.testing.doctest import DocFileSuite

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('adapter.txt',
                     package='grok'),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
