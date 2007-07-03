"""
If there is a static/ directory inside of a grokked package, its
contents will be available as static resources under a URL:

Actually it won't be this megrok package because the resource is registered for
IDefaultBrowserLayer and layers in this package do not inherit from
IDefaultBrowserLayer.

Instead resources will be configured explicitly.

"""
