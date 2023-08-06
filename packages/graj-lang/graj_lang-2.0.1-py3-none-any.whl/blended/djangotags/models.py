"""
In all versions of Django, models.py loads at system startup.  So, this is the place
to put any monkey-patching that may be required to bootstrap a system.

Blended does a coupld of things that might be considered "monkey patching".  First, it 
appends the blended_tags library to the template tag builtins.  This way, the Blended
versions of the template tags will override the template tags and filters natively provided
by Django, without users having to add {% load blended_tags %} to every template.  

This automatic loading can be turned off by setting the 'override_builtins' option of the TEMPLATES 
setting to False, or by setting the OVERRIDE_BUILTINS setting itself to False (in case of a 
conflict where one of the two settings is set to True, the TEMPLATES option will take precidence).

Second, in order to provide global control over autoescape functionality, it wraps the constructors
of the django.template.context.Context and django.template.context.RequestContext classes with
decorators that apply the AUTOESCAPE_DEFAULT setting at the time of object instantiation.

By default (i.e. if it is unspecified), the AUTOESCAPE_DEFAULT is False, but it can be overridden
in the settings.  If the original default Django functionality is required, set AUTOESCAPE_DEFAULT
to True.
"""

from django.conf import settings
from blended.djangotags.templatetags.blended_tags import register
from django.template.context import Context, RequestContext

TEMPLATES = getattr(settings, 'TEMPLATES', None)

if TEMPLATES and ('OPTIONS' in TEMPLATES) and ('override_builtins' in TEMPLATES['OPTIONS']):
    OVERRIDE_BUILTINS = TEMPLATES['OPTIONS']['override_builtins']
elif getattr(settings, 'OVERRIDE_BUILTINS', None):
    OVERRIDE_BUILTINS = settings.OVERRIDE_BUILTINS
else:
    OVERRIDE_BUILTINS = True

try:
    from django.template.base import builtins
    if OVERRIDE_BUILTINS:
        builtins.append(register)
except ImportError:
    from django.template.engine import Engine
    if OVERRIDE_BUILTINS:
        Engine.default_builtins.append('blended.djangotags.templatetags.blended_tags')

'''
Engine.default_builtins = 
                        ['django.template.defaulttags', 'django.template.defaultfilters', 
                        'django.template.loader_tags', 'blended.djangotags.templatetags.blended_tags']
'''   
# breakpoint()

def wrap_context_init(__init__):
    def __wrapinit__(self, dict_=None, autoescape=None, **kwargs):
        if autoescape is None:
            autoescape = getattr(settings, 'AUTOESCAPE_DEFAULT', False)
        return __init__(self, dict_, autoescape=autoescape, **kwargs) 
    return __wrapinit__


def wrap_request_context_init(__init__):
    def __wrapinit__(self, request, dict_=None, processors=None, **kwargs):
        autoescape_default = getattr(settings, 'AUTOESCAPE_DEFAULT', False)
        autoescape = kwargs.pop('autoescape', autoescape_default)
        try:
            return __init__(self, request, dict_, processors, autoescape=autoescape, **kwargs) 
        except TypeError:
            return __init__(self, request, dict_, processors, **kwargs)
    return __wrapinit__


Context.__init__ = wrap_context_init(Context.__init__)
RequestContext.__init__ = wrap_request_context_init(RequestContext.__init__)


