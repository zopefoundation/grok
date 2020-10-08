"""
Since grok.global_utility is a MultipleTimesDirective, there is a list of
GlobalUtilityInfo objects annotated on the module.

  >>> from grok.tests.directive import multipletimes
  >>> guis = grok.global_utility.bind().get(multipletimes)
  >>> len(guis)
  2

  >>> factory, provides, name, direct = guis[0]
  >>> factory
  <class 'grok.tests.directive.multipletimes.Club'>

  >>> provides
  <InterfaceClass grok.tests.directive.multipletimes.IClub>

  >>> name
  'foo'

  >>> factory, provides, name, direct = guis[1]
  >>> factory
  <class 'grok.tests.directive.multipletimes.Cave'>

  >>> provides is None
  True

  >>> print(name)

"""
import grok
from zope import interface


class IClub(interface.Interface):
    pass


class ICave(interface.Interface):
    pass


@grok.implementer(IClub)
class Club(object):
    pass


@grok.implementer(ICave)
class Cave(object):
    pass


grok.global_utility(Club, provides=IClub, name='foo')
grok.global_utility(Cave)
