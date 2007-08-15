"""Initialize grok admin application.

The grok admin application provides a session based login, which
eventually must be enabled using Pluggable Authentication
Utilities. This is done here.
"""

from zope.component import adapter, provideHandler
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent


def getPrincipalCredentialsFromZCML():
    """Read all principals' attributes from site.zcml.
    """
    import xml.sax
    from zope.app.appsetup.appsetup import getConfigSource

    class SAXPrincipalFinder(xml.sax.ContentHandler):
        """Parse an XML file and get attributes of ``principal`` tags.

        The principal tags of site.xml contain the credentials of
        principals as attributes. The attributes usually are 'id',
        'login', 'password', 'title' and other more. And usually only
        one pricipal is defined: the manager.
        """
        result = []

        def startElement(self, name, attrs):
            if name != 'principal':
                return
            self.result.append(dict(attrs.copy()))

    site_zcml_file = getConfigSource()
    principal_finder = SAXPrincipalFinder()
    xml.sax.parse(site_zcml_file, principal_finder)
    return principal_finder.result


def setupSessionAuthentication(root_folder=None,
                               principal_credentials=[{u'id': u'zope.manager',
                                                      u'login': u'grok',
                                                      u'password': u'grok',
                                                      u'title': u'Manager'
                                                      }],
                               auth_foldername=u'authentication',
                               userfolder_name=u'Users',
                               userfolder_prefix=u'grokadmin'
                               ):
    """Add session authentication PAU to root_folder.

    Add a PluggableAuthentication in site manager of
    root_folder. ``auth_foldername`` gives the name of the PAU to
    install, userfolder_prefix the prefix of the authenticator plugin
    (a simple ``PrincipalFolder``), which will be created in the PAU
    and gets name ``userfolder_name``. ``principal_credentials`` is a
    list of dicts with, well, principal_credentials. The keys ``id``,
    ``login``, ``password`` and ``title`` are required for each
    element of this list.
    """
    from zope.component import getUtilitiesFor
    from zope.security.proxy import removeSecurityProxy
    from zope.app.security.interfaces import IAuthentication
    from zope.app.securitypolicy.interfaces import IPrincipalRoleManager
    from zope.app.securitypolicy.interfaces import IRole
    from zope.app.authentication import PluggableAuthentication
    from zope.app.authentication.interfaces import IAuthenticatorPlugin
    from zope.app.authentication.principalfolder import PrincipalFolder
    from zope.app.authentication.principalfolder import InternalPrincipal

    sm = root_folder.getSiteManager()
    if auth_foldername in sm.keys():
        # There is already a folder of this name.
        return

    pau = PluggableAuthentication()
    users = PrincipalFolder(userfolder_prefix)

    # Add users into principals folder to enable login...
    for user in principal_credentials:
        # XXX make sure, the keys exist...
        user['id'] = user['id'].rsplit('.',1)[-1]
        user_title = user['title']
        principal = InternalPrincipal(user['login'],
                                      user['password'],
                                      user['title'])
        users[user['id']] = principal

    # Configure the PAU...
    pau.authenticatorPlugins = (userfolder_name,)
    pau.credentialsPlugins = ("No Challenge if Authenticated",
                              "Session Credentials")

    # Add the pau and its plugin to the root_folder...
    sm[auth_foldername] = pau
    sm[auth_foldername][userfolder_name] = users
    pau.authenticatorPlugins = (users.__name__,)

    # Register the PAU with the site...
    sm.registerUtility(pau, IAuthentication)
    sm.registerUtility(users, IAuthenticatorPlugin, name=userfolder_name)

    # Add manager roles to new users...
    # XXX the real roles could be obtained from site.zcml.
    role_ids = [name for name, util in getUtilitiesFor(IRole, root_folder)]
    user_ids = [users.prefix + p['id'] for p in principal_credentials]
    role_manager = IPrincipalRoleManager(root_folder)
    role_manager = removeSecurityProxy(role_manager)
    for role in role_ids:
        for user_id in user_ids:
            role_manager.assignRoleToPrincipal(role,user_id)



# If a new database is created, initialize a session based
# authentication.
#
# First create an eventhandler `adminSetup`, that is
# called, whenever a database is opened...
@adapter(IDatabaseOpenedWithRootEvent)
def adminSetup(event):
    from zope.app.appsetup.bootstrap import getInformationFromEvent
    
    db, connection, root, root_folder = getInformationFromEvent(event)
    principal_credentials = getPrincipalCredentialsFromZCML()
    setupSessionAuthentication(root_folder = root_folder,
                               principal_credentials = principal_credentials)


# ...then install the event handler:
provideHandler(adminSetup)

