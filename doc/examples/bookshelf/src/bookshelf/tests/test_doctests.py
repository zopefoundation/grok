import doctest
import unittest

def test_suite():
    modules = ['app', 'book', 'shelf']
    suite = unittest.TestSuite()
    for module in modules:
        module_name = 'bookshelf.%s' % module
        test = doctest.DocTestSuite(module_name)
        suite.addTest(test)
    return suite

if __name__ == '__main__':
      unittest.main(defaultTest='test_suite')
