##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.

$Id: bootstrap.py 85041 2008-03-31 15:57:30Z andreasjung $
"""

import os, shutil, sys, tempfile, urllib2, logging

def remove_old_logger_handlers():
    # zc.buildout installs a new log stream on every call of
    # main(). We remove any leftover handlers to avoid multiple output
    # of same content (doubled lines etc.)
    root_logger = logging.getLogger()
    if 'zc.buildout' in root_logger.manager.loggerDict.keys():
        logger = logging.getLogger('zc.buildout')
        for handler in logger.handlers:
            logger.removeHandler(handler)
    return


tmpeggs = tempfile.mkdtemp()

try:
    import pkg_resources
except ImportError:
    ez = {}
    exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py'
                         ).read() in ez
    ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)

    import pkg_resources

if sys.platform == 'win32':
    def quote(c):
        if ' ' in c:
            return '"%s"' % c # work around spawn lamosity on windows
        else:
            return c
else:
    def quote (c):
        return c

cmd = 'from setuptools.command.easy_install import main; main()'
ws  = pkg_resources.working_set
assert os.spawnle(
    os.P_WAIT, sys.executable, quote (sys.executable),
    '-c', quote (cmd), '-mqNxd', quote (tmpeggs), 'zc.buildout',
    dict(os.environ,
         PYTHONPATH=
         ws.find(pkg_resources.Requirement.parse('setuptools')).location
         ),
    ) == 0

ws.add_entry(tmpeggs)
ws.require('zc.buildout')
import zc.buildout.buildout
zc.buildout.buildout.main(sys.argv[1:] + ['bootstrap'])
remove_old_logger_handlers()
shutil.rmtree(tmpeggs)

# grokproject specific addition to standard bootstrap.py:
# Install eggbasket too.  This should be verbose to give the user
# information about what is happening, since this can take a while.
zc.buildout.buildout.main(sys.argv[1:] + ['-v', 'install', 'eggbasket'])
if sys.platform == 'win32':
    print "Now you can run 'bin\buildout.exe'"
else:
    print "Now you can run 'bin/buildout'"
