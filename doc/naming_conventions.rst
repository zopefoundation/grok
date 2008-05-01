Grok naming conventions
-----------------------

Zope 3 used to follow PEP 8, but then PEP 8 changed so that
methodNames() is deprecated in favor of method_names().

Grok aims to be mostly consistent with Zope 3, but does make some
changes in the direction of PEP 8.

modulenames - module and package names are all lower case, no
underscores
              
ClassNames - CamelCase (Zope 3 + PEP 8)

methodNames - camelCase: follow Zope 3 conventions. We work a lot with Zope 3
              classes and sometimes subclass.

attribute_names - Zope 3 + PEP 8

class_annotations - we break with Zope 3 tradition
                    (grok.local_utility() versus implementsOnly()). 
                    This makes class annotations stand out a bit
                    more and is more consistent with the use of
                    class-level attribute names for customization
                    as well (as in formlib).

top_level_functions - Zope 3 uses camel case (getUtility()).  Grok
                      uses underscores for top-level functions that
                      define class annotations. Grok internally has also
                      been using underscores for functions defined
                      internally. So far we have avoided exposing them
                      to the outside world. If you need to expose
                      one of these, bring it up on the grok-dev mailing list.
