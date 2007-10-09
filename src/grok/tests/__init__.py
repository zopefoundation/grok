# this is a package

from zope.configuration.config import ConfigurationMachine

import grok as grokpkg

def grok(module_name):
    config = ConfigurationMachine()
    grokpkg.grok(module_name, config=config)
    config.execute_actions()
    
