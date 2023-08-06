
import unittest
import re

from django.test import TestCase #, modify_settings
from django.template import Template, Context, RequestContext
from django.template.base import TemplateSyntaxError
from django.template.engine import Engine
from django.template.loaders.app_directories import Loader
from django.conf import settings

from blended.djangotags.loader import template_from_string, preprocess, Loader as BaseLoader
from blended.jinjaenv import BlendedEnvironment, number_filter, BlendedImmutableEnvironment
from blended.functions import builtins, hexcolor, rgbcolor, blendedround

from jinja2 import Environment, UndefinedError, contextfunction,DictLoader,\
          make_logging_undefined, TemplateSyntaxError as JinjaTemplateSyntaxError
from jinja2._compat import text_type


class BlendedTestCase(TestCase):

    @classmethod
    def setUpClass(klass):
        klass.TEMPLATES = getattr(settings, 'TEMPLATES', None)
        settings.TEMPLATES = [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            #'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'blended.functions.builtins',
                ],
                'loaders': [
                    'blended.djangotags.loader.Loader'
                ]
            }
        }]

    @classmethod
    def tearDownClass(klass):
        settings.TEMPLATES = klass.TEMPLATES


    def test_01_parent(self):
        parent = "{% block test %}Parent{% endblock %}"
        child  = "{% extends parent %}{% block test %}{% parent %} Child{% endblock %}"

        result = Template(child).render(Context({"parent":Template(parent)}))
        self.assertEquals(result, "Parent Child")

        template = \
            "{% extends (block_test ~ 'Parent' ~ endblock)|template %}" \
            "{% block test %}{% parent %} Child{% endblock %}"

        result = Template(template).render(Context(
            {'block_test' : '{% block test %}', 'endblock' : '{% endblock %}'}))
        self.assertEquals(result, "Parent Child")

        context = {
            'templates' : {
                'one' : '{% block test %}Base One{% endblock %}',
                'two' : '{% block test %}Base Two{% endblock %}'
            },
            'page' : {
                'content' : 'Page Content',
                'template' : 'one'
            }
        }
        template = \
            "{% extends templates[page.template]|template %}" \
            "{% block test %}{% parent %} {{ page.content }}{% endblock %}"

        result = Template(template).render(Context(context))
        self.assertEquals(result, 'Base One Page Content')

        context['page']['template'] = 'two'
        result = Template(template).render(Context(context))
        self.assertEquals(result, 'Base Two Page Content')

        ## Not sure if we should have a workarround for Django's lexer limitations
        template = \
            "{% extends '{% print 1 + 2 %/}'|template %}"

    def test_02_print(self):
        template = "{% print 'a' ~ 'b' %}"
        result = Template(template).render(Context({}))

        self.assertEquals(result, "ab")

        template = "{% print 1 ~ 2 %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "12")

    def test_03_set(self):
        template = "{% set a = 22 %}{% print a * 2 %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "44")

    def test_04_include(self):
        template = "{% include '{{a}}'|template with {'a':1} %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "1")

        template = "{% include '{{a + 1}}'|template with {'a':1} %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "2")

    @unittest.skip("This won't work because of tokenizer limitations of Django")
    def test_05_include_template_string(self):
        template = """{% include '{% include "hello"|template %}'|template %}"""
        template = Template(template)
        result = template.render(Context({}))
        self.assertEquals(result, "hello")

        template = """{% include '{% include "{{ 1 + 1 }}"|template %}'|template %}"""
        result = Template(template).render(Context({}))
        self.assertEquals(result, "1")

    def test_06_for(self):
        template = "{% for x in [3,2,1] %}{{ x }}{% if not loop.last %}, {% endif %}{% endfor %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "3, 2, 1")

        template = "{% for x,y in {'a':1,'b':2}|items %}{{x}}:{{y}},{% endfor %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "a:1,b:2,")

        template = "{% for x in [] %}Not empty.{% empty %}Empty.{% endfor %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "Empty.")

        template = "{% for x in [] %}Not empty.{% else %}Empty.{% endfor %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "Empty.")

    def test_07_autoescape(self):
        no_AE_attr = False
        try:
            old_default = settings.AUTOESCAPE_DEFAULT
        except AttributeError:
            no_AE_attr = True

        settings.AUTOESCAPE_DEFAULT = False
        context = Context({"html": "<h1>Title</h1>"})

        template = "{{ html }}|{{ html|safe }}|{{ html|escape }}|{{ html|e }}"
        result = Template(template).render(context)
        expected = "<h1>Title</h1>|<h1>Title</h1>|&lt;h1&gt;Title&lt;/h1&gt;|&lt;h1&gt;Title&lt;/h1&gt;"
        self.assertEquals(result, expected)

        template = "{{ html|safe|escape }}|{{ html|escape|safe }}"
        result = Template(template).render(context)
        expected = "<h1>Title</h1>|<h1>Title</h1>"
        self.assertEquals(result, expected)

        template = "{{ html|escape|escape }}|{{ html|safe|safe }}"
        result = Template(template).render(context)
        expected = "&lt;h1&gt;Title&lt;/h1&gt;|<h1>Title</h1>"
        self.assertEquals(result, expected)

        settings.AUTOESCAPE_DEFAULT = True
        context = Context({"html": "<h1>Title</h1>"})

        template = "{{ html }}|{{ html|safe }}|{{ html|escape }}|{{ html|e }}"
        result = Template(template).render(context)
        expected = "&lt;h1&gt;Title&lt;/h1&gt;|<h1>Title</h1>|" \
                   "&lt;h1&gt;Title&lt;/h1&gt;|&lt;h1&gt;Title&lt;/h1&gt;"
        self.assertEquals(result, expected)

        template = "{{ html|safe|escape }}|{{ html|escape|safe }}"
        result = Template(template).render(context)
        expected = "<h1>Title</h1>|<h1>Title</h1>"
        self.assertEquals(result, expected)

        template = "{{ html|escape|escape }}|{{ html|safe|safe }}"
        result = Template(template).render(context)
        expected = "&lt;h1&gt;Title&lt;/h1&gt;|<h1>Title</h1>"
        self.assertEquals(result, expected)

        if no_AE_attr:
            delattr(settings, 'AUTOESCAPE_DEFAULT')
        else:
            settings.AUTOESCAPE_DEFAULT = old_default

    def test_08_load(self):
        template = "{% load blended_tags %}{% print 1 + 1 %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "2")

    def test_10_strings_in_print(self):
        template = "{% print '1,2,3' %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "1,2,3")

        template = "{% print '{{ var }}' %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "{{ var }}")

        template = '{% print "{{ var }}" %}'
        result = Template(template).render(Context({}))
        self.assertEquals(result, "{{ var }}")

        template = preprocess("{{ '{{ var }}' }}")
        result = Template(template).render(Context({}))
        self.assertEquals(result, "{{ var }}")

        template_obj = template_from_string("{{ '{{ var }}' }}")
        result = template_obj.render(Context({}))
        self.assertEquals(result, "{{ var }}")

    def test_11_float_printing(self):
        template = "{% print 4 / 2 %}|{% print 4.0 / 2 %}|{% print 5 / 2 %}|{% print 5.0 / 2 %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "2|2|2.5|2.5")

        template = "{% print 5.0 + 1 %}|{% print 1 + 2 %}|{% print 4.0 - 1 %}|{% print 5.2 - 1 %}"
        result = Template(template).render(Context({}))
        self.assertEquals(result, "6|3|3|4.2")

    def test_12_escape(self):
        template = "<html><body>{{ hello|escape }}</body></html>"
        context = Context({ "hello" : "<p>hello</p>" })
        expected = "<html><body>&lt;p&gt;hello&lt;/p&gt;</body></html>"
        result = Template(template).render(context)
        self.assertEquals(result, expected)

        template = "<html><body>{% print hello|escape %}</body></html>"
        context = Context({ "hello" : "<p>hello</p>" })
        expected = "<html><body>&lt;p&gt;hello&lt;/p&gt;</body></html>"
        result = Template(template).render(context)
        self.assertEquals(result, expected)

        template = \
            "{% print html|escape %}|" \
            "{% set var='<h1>hello</h1>'|escape %}" \
            "{{ var }}|" \
            "{% print var %}"
        context = Context({ "html" : "<h1>Title</h1>" })
        expected = "&lt;h1&gt;Title&lt;/h1&gt;|&lt;h1&gt;hello&lt;/h1&gt;|&lt;h1&gt;hello&lt;/h1&gt;"
        result = Template(template).render(context)
        self.assertEquals(result, expected)

        template = \
            "{% print nullvar|escape %}" \
            "{{ nullvar|escape }}" \
            "{% set var=nullvar|escape %}" \
            "{{ nullvar }}" \
            "{% print nullvar %}"
        expected = ""
        result = Template(template).render(Context({}))
        self.assertEquals(result, expected)

    def test_13_render_filter(self):
        template = \
            """{% include '{{ "{{ a + b }}"|template|render({ "a":1, "b":2 }) }}'|template %}"""

        result = template_from_string(template).render(Context({}))
        self.assertEqual(result, "3")

        template = \
            """{% set rendered = "{{a}},{{b}}"|template|render({"a":1, "b":2 }) %}{{ rendered }}"""

        result = template_from_string(template).render(Context({}))
        self.assertEqual(result, "1,2")

    def test_14_color_functions(self):
        #from django.test import Client
        #req = Client()
        color1, color2 = '#56789A', '#123456'
        template_str = \
            "{% import 'colormacros.html' as colormacros %}" \
            "{{ colormacros.avgcolor(color1, color2) }}"
        result = template_from_string(template_str).render(Context({'color1':color1,'color2':color2}))
        expected = rgb_avg(rgbcolor(color1), rgbcolor(color2))
        self.assertEquals(result, expected)

        color, fraction = '#888', 0.5
        template_str = \
            "{% from 'colormacros.html' import lighten, darken as darker %}" \
            "{{ lighten(color, fraction) }},{{ darker(color, fraction) }}"
        result = template_from_string(template_str).render(Context({'color':color, 'fraction':fraction}))
        expected = "%s,%s" % (lighten(color, fraction), darken(color, fraction))
        self.assertEquals(result, expected)

       # on replacing "Context" with "RequestContext" in test_14_color_functions
       # Error which we are facing in blended-lang-test will raised :
       # NameError: Function name 'rgbcolor' is not defined.

    def test_15_kitchen_sink(self):
        template_str = \
            "{% extends base|template %}{% block content %}{% parent %}" \
            "{% set message = '<br/>Nice to meet you!' %}{{- message -}}{% endblock %}"
        context = {
            "base": "{% macro hello(name) %}Hello {{ name|default('World') }}!{% endmacro %}" \
                    "<html>{% block content %}{% print hello() %}{% endblock %}</html>"
        }
        expected = "<html>Hello World!<br/>Nice to meet you!</html>"
        from django.test import Client
        req = Client()
        result = template_from_string(template_str).render(RequestContext(req, context))
        self.assertEquals(result, expected)

    def test_16_print_numbers(self):
        from django.test import Client
        req = Client()

        context = { "two" : 2.0, "dict": { 'num' : 3.0 }, "list" : [4.0], "six" : 6 , "ten" : 10}

        template = \
            "{% print 1.0 %},{% print two %},{% print dict.num %},{% print list[0] %}," \
            "{% print '5.0'|number %},{% print six|number %},{% print round(7.2) %}," \
            "{% print six + two %},{% print 4.5 * 2 %},{{ ten }},{% print ten + 1 %}"

        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "1,2,3,4,5,6,7,8,9,10,11")

        template = \
            "{{ 1.0 }},{{ two }},{{ dict.num }},{{ list[0] }},{{ '5.0'|number }}," \
            "{{ six|number }},{{ round(7.2) }},{{ six + two }},{{ 4.5 * 2 }},{{ ten }}," \
            "{{ ten + 1 }}"

        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "1,2,3,4,5,6,7,8,9,10,11")

        template = "{{ 1.0 }}"
        context = {}
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "1")

    def test_17_dict_attributes(self):
        from django.test import Client
        req = Client()

        template = "{{ dict.items }}"
        context = { 'dict' : { 'items': [1,2,3] } }
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "[1, 2, 3]")

        template = "{% print dict.items %}"
        context = { 'dict' : { 'list': [1,2,3] } }
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "")

        template = "{{ dict.items }}"
        context = { 'dict' : { 'list': [1,2,3] } }
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "")

    def test_18_autoescape_tag(self):

        from django.test import Client
        req = Client()
        context = { 'html': '<html>' }

        no_AE_attr = False
        try:
            old_default = settings.AUTOESCAPE_DEFAULT
        except AttributeError:
            no_AE_attr = True
        settings.AUTOESCAPE_DEFAULT = False

        template = "{% autoescape true %}{{ '<html>' }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        #self.assertEqual(result, "<html>")

        template = "{% autoescape true %}{{ '<html>'|safe }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        template = "{% autoescape true %}{{ '<html>'|e }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape true %}{{ html }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape true %}{{ html|safe }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        template = "{% autoescape true %}{{ html|e }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape on %}{{ html }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        settings.AUTOESCAPE_DEFAULT = True

        template = "{{ '<html>' }}" + '{{ "</html>" }}'
        result = template_from_string(template).render(RequestContext(req,context))
        #self.assertEqual(result, "<html></html>")

        template = "{{ html }}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape false %}{{ '<html>' }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ '<html>'|safe }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ '<html>'|e }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape false %}{{ html }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ html|safe }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ html|e }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape off %}{{ html }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        template = "{{ '{{ html }}'|template|render({'html':'<html>'}) }}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape false %}" \
                   "{{ '{{ html }}'|template|render({'html':'<html>'}) }}" \
                   "{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "<html>")

        settings.AUTOESCAPE_DEFAULT = False

        template = "{% autoescape true %}" \
                   "{{ '{{ html }}'|template|render({'html':'<html>'}) }}" \
                   "{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,context))
        self.assertEqual(result, "&lt;html&gt;")

        if no_AE_attr:
            delattr(settings, 'AUTOESCAPE_DEFAULT')
        else:
            settings.AUTOESCAPE_DEFAULT = old_default

    def test_19_escape_macro(self):
        from django.test import Client
        req = Client()

        template = "{% macro m() %}<html>{% endmacro %}" \
                   "{% autoescape true %}{{ m() }}{% endautoescape %}"
        result = template_from_string(template).render(RequestContext(req,{}))
        self.assertEqual(result, "<html>")

    def test_20_functions(self):
        from django.test import Client
        req = Client()

        template = "{% for i in range(0,5) %}" \
                   "{{ cycle(['cold','hot'], i) }}{% if not loop.last %},{% endif %}" \
                   "{% endfor %}"
        result = template_from_string(template).render(RequestContext(req,{}))
        expected = "cold,hot,cold,hot,cold"
        self.assertEqual(result, expected)


def rgb_avg(rgb1, rgb2):
    """
    Takes 2 rgb values represented in list form and
    returns the rgb value that is an average of the 2 values passed in.
    """
    data = [rgb1,rgb2]
    return hexcolor([int(sum(e)/len(e)) for e in zip(*data)])

def lighten(hex_val, fraction):
    """Decreases the hex value passed in by the percent argument passed in"""
    list_rgb = rgbcolor(hex_val)
    col_r, col_g, col_b = list_rgb[0], list_rgb[1], list_rgb[2]
    white_col_per = 255 * fraction
    new_r = col_r + white_col_per
    new_g = col_g + white_col_per
    new_b = col_b + white_col_per
    if new_r > 255: new_r = 255
    if new_g > 255: new_g = 255
    if new_b > 255: new_b = 255
    return hexcolor([new_r,new_g,new_b])

def darken(hex_val, fraction):
    """Increases the hex value passed in by the percent argument passed in"""
    list_rgb = rgbcolor(hex_val)
    col_r, col_g, col_b = list_rgb[0],list_rgb[1],list_rgb[2]
    new_r = col_r - col_r * fraction
    new_g = col_g - col_g * fraction
    new_b = col_b - col_b * fraction
    return hexcolor([new_r,new_g,new_b])


class PreprocessTest(TestCase):

    def test_01_expr(self):
        template = preprocess("{{ '{{ var }}' }}")
        self.assertEquals(template, "{% print '{{ var }}' %}")

        template = preprocess('{{ "{{ var }}" }}')
        self.assertEquals(template, '{% print "{{ var }}" %}')

    def test_02_func_filter(self):
        template = preprocess("{{ func(var) }}")
        self.assertEquals(template, "{% print func(var) %}")

        template = preprocess("{{ var|filter(arg, arg) }}")
        self.assertEquals(template, "{% print var|filter(arg, arg) %}")

    def test_03_remove_whitespace_expr(self):
        template = preprocess("  {{- var -}}  ")
        self.assertEquals(template, "{% print var %}")

        template = preprocess("XX\n   {{- var|filter(arg) -}}   XX")
        self.assertEquals(template, "XX{% print var|filter(arg) %}XX")

    def test_04_newlines_after_tags(self):
        "needs to be implemented"

    def test_05_strings_inside_tags(self):
        ## In order to avoid pre-processing being performed on the underlying strings twice,
        ## once by the loader and once by the template filter, templates inside strings
        ## inside tags and expressions should not be converted.
        original = """{% set var = "{{ '{{ 1 + 1 }}' }}" %}"""
        self.assertEquals(preprocess(original), original)

        original = """{% include '{% include "{{ 1 + 1 }}"|template %}'|template %}"""
        self.assertEquals(preprocess(original), original)

        original = """{% include '{% include "hello"|template %}\n'|template %}\n"""
        ## Not sure if this is actually the expected value
        expected = """{% include '{% include "hello"|template %}'|template %}"""
        self.assertEquals(preprocess(original), expected)


    def test_99_complex_templates(self):
        "needs to be implemented"


class HelperLoader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        out_source, path = \
            super(HelperLoader, self).load_template_source(template_name, template_dirs=None)
        self.out_source = out_source
        return out_source, path


class CustomLoaderTest(TestCase):

    def test_remove_white_space_for_hyphne_modulo_tag(self):
        """will be Pass on Removing whitespaces before {%- and after -%}
        and replace them by '{%' and '%}'.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/whitespace.html')

        self.assertEqual(out.out_source, "{% for i in list %}{% print i %}{% endfor %}")

    def test_remove_new_line_after_module_close_tag(self):
        """
        will be Pass on Removing new line i.e '\n' after every '%}'.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/newline.html')

        expected = '{% for i in list %}      {% print i %}\n{% print a*c/d-b %}\n\n\n{% endfor %}'
        self.assertEqual(out.out_source, expected)

    def test_allow_multiline_comments(self):
        """
        will be Pass on Allowing multiline comments in template.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/multilinecomment.html')

        self.assertEqual(out.out_source,"{# this is a multiline comment #}\n{% print func() %}")

    def test_allow_multiline_tags1(self):
        """
        will be Pass on Allowing multiline tag in template.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/multilinetag.html')

        self.assertEqual(out.out_source,'{% with var="yash" %}{% print var %}{% print a+b %}{% endwith %}')

    def test_allow_multiline_tags2(self):
        """
        will be Pass on Allowing multiline variable in template.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/multilinevariable.html')

        self.assertEqual(out.out_source,'{% print var %}')

    def test_replace_by_echo_tags(self):
        """
        will be Pass on replacing {{ expression }} with {% echo expression %}.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/echotag.html')

        expected = \
              '{% load blended_tags %}{% with var=list %}{% print "Ipsum" %}' \
              '\n   \n   \n{% endwith %}'
        self.assertEqual(out.out_source, expected)

    def test_remove_white_space_for_hyphne_modulo_tag2(self):
        """
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/whitespace2.html')

        expected = "{% with name=list %}{% for i in name %}{% print i %}{% endfor %}{% endwith %}"
        self.assertEqual(out.out_source, expected)

    def test_remove_white_space_for_hyphne_modulo_tag_fail(self):
        """
        will fails on not Removing whitespaces before {%- and after -%}
        and replace them by '{%' and '%}'.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/whitespace.html')

        self.assertNotEqual(out.out_source, '{% for i in list -%}          {{i}} {%- endfor %}')

    def test_remove_new_line_after_module_close_tag_fail(self):
        """
        will fails on not Removing new line i.e '\n' after every '%}'.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/newline.html')

        self.assertNotEqual(out.out_source,'{% for i in list %}\n{{ i }}\n{% endfor %}\n')

    def test_allow_multiline_comments_fail(self):
        """
        will fails on not Allowing multiline comments in template.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/multilinecomment.html')

        self.assertNotEqual(out.out_source,'{# this is\na multiline\ncomment #}\n{{ func() }}\n')

    def test_allow_multiline_tags_fail(self):
        """
        will fails on not Allowing multiline tags in template.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/multilinetag.html')

        expected = '{% with\nvar="yash"\n %}{{\n var\n }}{{ a+b }}\n{% endwith\n%}'
        self.assertNotEqual(out.out_source, expected)

    def test_replace_by_echo_tags_fail(self):
        """
        will fails on not replacing {{ expression }} with {% echo expression %}.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = HelperLoader(engine)
        template = out.load_template('temp/echotag.html')

        expected = '{%load blended_tags %}{% with var=list %}{{ "Ipsum" }}\n   \n   \n{% endwith %}'
        self.assertNotEqual(out.out_source, expected)

    def test_remove_white_space_for_hyphne_modulo_tag_default_loader(self):
        """
        will be fail if blended djangoloader is used.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = Loader(engine)

        self.assertRaises(TemplateSyntaxError, out.load_template, 'temp/whitespace.html')

    def test_remove_new_line_after_module_close_tag_default_loader(self):
        """
        will be fail if blended djangoloader is used.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = Loader(engine)

        self.assertRaises(TemplateSyntaxError, out.load_template, 'temp/newline.html')

    def test_allow_multiline_comments_default_loader(self):
        """
        will be fail if blended djangoloader is used.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = Loader(engine)

        self.assertRaises(TemplateSyntaxError, out.load_template, 'temp/multilinecomment.html')

    def test_allow_multiline_tags_default_loader(self):
        """
        will be fail if blended djangoloader is used.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = Loader(engine)

        self.assertRaises(TemplateSyntaxError, out.load_template, 'temp/multilinetag.html')

    def test_replace_by_echo_tags_default_loader(self):
        """
        will be fail if blended djangoloader is used.
        """
        engine = Engine()
        engine.dirs = settings.TEMPLATE_DIRS
        out = Loader(engine)

        self.assertRaises(TemplateSyntaxError, out.load_template, 'temp/echotag.html')


class JinjaTestCase(TestCase):

    def test_01_print_numbers(self):
        template = \
            "{{ 1.0 }},{{ two }},{{ dict.num }},{{ list[0] }},{{ '5.0'|number }}," \
            "{{ six|number }},{{ round(7.2) }},{{ six + two }},{{ 4.5 * 2 }},{{ ten }},{{ ten + 1 }}"

        context = { "two" : 2.0, "dict": { 'num' : 3.0 }, "list" : [4.0], "six" : 6 , "ten" : 10}

        env = BlendedEnvironment()
        result = env.from_string(template).render(context)
        self.assertEqual(result, "1,2,3,4,5,6,7,8,9,10,11")

        env = Environment()
        env.filters['number'] = number_filter
        env.globals['round'] = builtins()['round']
        result = env.from_string(template).render(context)
        # This one is getting failed in python 3
        self.assertEqual(result, "1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10,11")

        env = BlendedEnvironment(trim_floats=False)
        result = env.from_string(template).render(context)
        self.assertEqual(result, "1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10,11")

    def test_02_include_tag(self):
        template = "{% include template_str|template with local_context %}"
        context = {
            "template_str" : "{{one}}, {{two}}, {{three}}",
            "local_context" : { "one" : 1.0, "two" : 2.0, "three" : 3.0 }
        }

        env = BlendedEnvironment()
        result = env.from_string(template).render(context)
        self.assertEqual(result, "1, 2, 3")

        env = Environment()
        self.assertRaises(JinjaTemplateSyntaxError, env.from_string, template)

    def test_03_render_filter(self):
        env = BlendedEnvironment()

        template = "{% print '{{ test }}'|template|render({ 'test' : 'This is a test.' }) %}"
        result = env.from_string(template).render({})
        self.assertEqual(result, "This is a test.")

        template = \
            """{% include '{{ "{{ a + b }}"|template|render({ "a":1, "b":2 }) }}'|template %}"""
        result = env.from_string(template).render({})
        self.assertEqual(result, "3")

        template = \
            """{% set rendered = "{{a}},{{b}}"|template|render({"a":1, "b":2 }) %}{{ rendered }}"""
        result = env.from_string(template).render({})
        self.assertEqual(result, "1,2")

    def test_04_slice_operation(self):
        env = BlendedEnvironment()

        template = "{{ 'abcd'[1:3] }}"
        result = env.from_string(template).render({})
        self.assertEqual(result, "bc")

        template = "{{ [1,2,3,4][1:2]|string }}"
        result = env.from_string(template).render({})
        self.assertEqual(result, "[2]")

        template = "{{ list[1:3]|string }}"
        result = env.from_string(template).render({ "list": [1,2,3,4]})
        self.assertEqual(result, "[2, 3]")

    def test_05_dict_attributes(self):
        env = BlendedEnvironment()

        template = "{{ dict.items }}"
        result = env.from_string(template).render({ 'dict' : { 'items': [1,2,3] } })
        self.assertEqual(result, "[1, 2, 3]")

        result = env.from_string(template).render({ 'dict' : { 'list': [1,2,3] } })
        self.assertEqual(result, "")

    def test_06_autoescape(self):
        env = BlendedEnvironment()

        template = "{% autoescape true %}{{ '<html>' }}{% endautoescape %}"
        result = env.from_string(template).render();
        #self.assertEqual(result, "<html>")

        template = "{% autoescape true %}{{ '<html>'|safe }}{% endautoescape %}"
        result = env.from_string(template).render();
        self.assertEqual(result, "<html>")

        template = "{% autoescape true %}{{ '<html>'|e }}{% endautoescape %}"
        result = env.from_string(template).render();
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape true %}{{ html }}{% endautoescape %}"
        result = env.from_string(template).render({ "html" : "<html>" });
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape true %}{{ html|safe }}{% endautoescape %}"
        result = env.from_string(template).render({ "html" : "<html>" });
        self.assertEqual(result, "<html>")

        template = "{% autoescape true %}{{ html|e }}{% endautoescape %}"
        result = env.from_string(template).render({ "html" : "<html>" });
        self.assertEqual(result, "&lt;html&gt;")

        env = BlendedEnvironment(autoescape=True)
        template = "{{ '<html>' }}" + '{{ "</html>" }}'
        result = env.from_string(template).render();
        #self.assertEqual(result, "<html></html>")

        template = "{{ html }}"
        result = env.from_string(template).render({ "html" : "<html>" });
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape false %}{{ '<html>' }}{% endautoescape %}"
        result = env.from_string(template).render();
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ '<html>'|safe }}{% endautoescape %}"
        result = env.from_string(template).render();
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ '<html>'|e }}{% endautoescape %}"
        result = env.from_string(template).render();
        self.assertEqual(result, "&lt;html&gt;")

        template = "{% autoescape false %}{{ html }}{% endautoescape %}"
        result = env.from_string(template).render({ "html" : "<html>" });
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ html|safe }}{% endautoescape %}"
        result = env.from_string(template).render({ "html" : "<html>" });
        self.assertEqual(result, "<html>")

        template = "{% autoescape false %}{{ html|e }}{% endautoescape %}"
        result = env.from_string(template).render({ "html" : "<html>" });
        self.assertEqual(result, "&lt;html&gt;")


    def test_07_escape_macro(self):
        env = BlendedEnvironment()
        template = "{% macro m() %}<html>{% endmacro %}" \
                   "{% autoescape true %}{{ m() }}{% endautoescape %}"
        result = env.from_string(template).render({});
        self.assertEqual(result, "<html>")


    def test_08_functions(self):
        env = BlendedEnvironment()
        template = "{% for i in range(0,5) %}" \
                   "{{ cycle(['cold','hot'], i) }}{% if not loop.last %},{% endif %}" \
                   "{% endfor %}"
        result = env.from_string(template).render({});
        expected = "cold,hot,cold,hot,cold"
        self.assertEqual(result, expected)


    def test_09_ifblock(self):
        env = BlendedEnvironment()

        base1 = "{% ifblock heading %}<h1>" \
                "{% block heading %}{{ heading }}{% endblock %}" \
                "</h1>{% endifblock %}"

        base2 = "<h1>{% ifblock heading %}" \
                "{% block heading %}{% endblock %}" \
                "{% else %}Default Heading" \
                "{% endifblock %}</h1>"

        template = "{% extends base|template %}" \
                   "{% block heading %} {{ heading }} {% endblock %}"

        result = env.from_string(template).render({ "base":base1, "heading":"Heading" })
        self.assertEqual(result, "<h1> Heading </h1>")

        result = env.from_string(template).render({ "base":base2, "heading":"Heading" })
        self.assertEqual(result, "<h1> Heading </h1>")

        result = env.from_string(template).render({ "base":base1 })
        self.assertEqual(result, "")

        result = env.from_string(template).render({ "base":base2 })
        self.assertEqual(result, "<h1>Default Heading</h1>")


    def test_10_round(self):
        jinjaenv = Environment()

        jinjaenv.globals.update({'round': blendedround})

        blendedenv = BlendedEnvironment()

        template = jinjaenv.from_string('{{ 2.646442|round(precision=8) }}')

        result = template.render({})
        self.assertEqual(result, u'2.646442')

        template = jinjaenv.from_string('{{ var|round }}')

        result = template.render({"var" : 50.6295472})
        self.assertEqual(result, u'51.0')

        template = blendedenv.from_string('{{ 2.646442|round(precision=8) }}')

        result = template.render({})
        self.assertEqual(result, u'2.646442')

        template = blendedenv.from_string('{{ var|round }}')

        result = template.render({"var" : 50.6295472})
        self.assertEqual(result, u'51')

        template = jinjaenv.from_string('{{ round(100.122220004455, 12) }}')

        result = template.render({})
        self.assertEqual(result, u'100.122220004')

        template = jinjaenv.from_string('{{ round(var,12) }}')

        result = template.render({"var" : 100.122220004455})
        self.assertEqual(result, u'100.122220004')

        #template = blendedenv.from_string('{{ round(100.122220004455, 12) }}')

        #result = template.render({})
        #self.assertEqual(result,  u'100.122220004')

        template = blendedenv.from_string('{{ round(var,12) }}')

        result = template.render({"var" : 100.122220004455})
        self.assertEqual(result, u'100.122220004')


class JinjaTrimFloatBug(TestCase):

    def test_item_and_attribute(self):
        from jinja2.sandbox import SandboxedEnvironment

        Environment = BlendedEnvironment
        SandboxedEnvironment = BlendedEnvironment
        for env in Environment(dict_attrs=True), SandboxedEnvironment(dict_attrs=True):
            # the |list is necessary for python3
            tmpl = env.from_string('{{ foo.items()|list }}')
            assert tmpl.render(foo={'items': 42}) == "[('items', 42)]"
            tmpl = env.from_string('{{ foo|attr("items")()|list }}')
            assert tmpl.render(foo={'items': 42}) == "[('items', 42)]"
            tmpl = env.from_string('{{ foo["items"] }}')
            assert tmpl.render(foo={'items': 42}) == '42'

    def test_logging_undefined(self):
        _messages = []
        Environment = BlendedEnvironment

        class DebugLogger(object):
            def warning(self, msg, *args):
                _messages.append('W:' + msg % args)

            def error(self, msg, *args):
                _messages.append('E:' + msg % args)

        logging_undefined = make_logging_undefined(DebugLogger())
        env = Environment(undefined=logging_undefined)
        assert env.from_string('{{ missing }}').render() == u''
        import pytest
        with pytest.raises(UndefinedError):
            env.from_string('{{ missing.attribute }}').render()
        assert env.from_string('{{ missing|list }}').render() == '[]'
        assert env.from_string('{{ missing is not defined }}').render() \
            == 'True'
        assert env.from_string('{{ foo.missing }}').render(foo=42) == ''
        assert env.from_string('{{ not missing }}').render() == 'True'
        assert _messages == [
            'W:Template variable warning: missing is undefined',
            "E:Template variable error: 'missing' is undefined",
            'W:Template variable warning: missing is undefined',
            'W:Template variable warning: customtags.trimfloat.trimint object has no attribute missing',
            'W:Template variable warning: missing is undefined',
        ]

    def test_center(self):
        env = BlendedEnvironment()
        tmpl = env.from_string('{{ "foo"|center(9) }}')
        assert tmpl.render() == '   foo   '

    def test_batch(self):
        env = BlendedEnvironment()
        tmpl = env.from_string("{{ foo|batch(3)|list }}|"
                               "{{ foo|batch(3, 'X')|list }}")
        out = tmpl.render(foo=list(range(10)))
        assert out == ("[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]|"
                       "[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 'X', 'X']]")

    def test_indent(self):
        env = BlendedEnvironment()
        tmpl = env.from_string('{{ foo|indent(2) }}|{{ foo|indent(2, true) }}')
        text = '\n'.join([' '.join(['foo', 'bar'] * 2)] * 2)
        out = tmpl.render(foo=text)
        assert out == ('foo bar foo bar\n  foo bar foo bar|  '
                       'foo bar foo bar\n  foo bar foo bar')

    def test_sort1(self):
        env = BlendedEnvironment()
        tmpl = env.from_string(
            '{{ [2, 3, 1]|sort }}|{{ [2, 3, 1]|sort(true) }}')
        assert tmpl.render() == '[1, 2, 3]|[3, 2, 1]'

    def test_typechecks(self):
        env = BlendedEnvironment()
        tmpl = env.from_string('''
            {{ complex is number }}
        ''')

        class MyDict(dict):
            pass

        assert tmpl.render(mydict=MyDict(), complex=complex(1, 2)).split() == [
                 'True'
                ]

class JinjaTrueFlaseBoolean(TestCase):

    def test_context_vars(self):
        env = BlendedEnvironment()
        slist = [42, 24]
        for seq in [slist, iter(slist), reversed(slist), (_ for _ in slist)]:
            tmpl = env.from_string('''{% for item in seq -%}
            {{ loop.index }}|{{ loop.index0 }}|{{ loop.revindex }}|{{
                loop.revindex0 }}|{{ loop.first }}|{{ loop.last }}|{{
               loop.length }}###{% endfor %}''')
            one, two, _ = tmpl.render(seq=seq).split('###')
            (one_index, one_index0, one_revindex, one_revindex0, one_first,
             one_last, one_length) = one.split('|')
            (two_index, two_index0, two_revindex, two_revindex0, two_first,
             two_last, two_length) = two.split('|')

            assert int(one_index) == 1 and int(two_index) == 2
            assert int(one_index0) == 0 and int(two_index0) == 1
            assert int(one_revindex) == 2 and int(two_revindex) == 1
            assert int(one_revindex0) == 1 and int(two_revindex0) == 0
            assert one_first == 'True' and two_first == 'False'
            assert one_last == 'False' and two_last == 'True'
            assert one_length == two_length == '2'

    def test_scoped_special_var(self):
        env = BlendedEnvironment()
        t = env.from_string(
            '{% for s in seq %}[{{ loop.first }}{% for c in s %}'
            '|{{ loop.first }}{% endfor %}]{% endfor %}')
        assert t.render(seq=('ab', 'cd')) \
            == '[True|True|False][False|True|False]'

    def test_default_true(self):
        env = BlendedEnvironment()
        tmpl = env.from_string(
            "{{ missing|default('no') }}|{{ false|default('no') }}|"
            "{{ false|default('no', true) }}|{{ given|default('no') }}"
        )
        assert tmpl.render(given='yes') == 'no|False|no|yes'

    def test_bool_reject(self):
        env = BlendedEnvironment()
        tmpl = env.from_string(
            '{{ [none, false, 0, 1, 2, 3, 4, 5]|reject|join("|") }}'
        )
        assert tmpl.render() == 'None|False|0'

    def test_bool(self):
        env = BlendedEnvironment()
        tmpl = env.from_string('{{ true and false }}|{{ false '
                               'or true }}|{{ not false }}')
        assert tmpl.render() == 'False|True|True'

    def test_grouping(self):
        env = BlendedEnvironment()
        tmpl = env.from_string(
            '{{ (true and false) or (false and true) and not false }}')
        assert tmpl.render() == 'False'

    def test_constant_casing(self):
        env = BlendedEnvironment()
        for const in True, False, None:
            tmpl = env.from_string('{{ %s }}|{{ %s }}|{{ %s }}' % (
                str(const), str(const).lower(), str(const).upper()
            ))
            assert tmpl.render() == '%s|%s|' % (const, const)

    def test_const(self):
        env = BlendedEnvironment()
        tmpl = env.from_string(
            '{{ true }}|{{ false }}|{{ none }}|'
            '{{ none is defined }}|{{ missing is defined }}')
        assert tmpl.render() == 'True|False|None|True|False'

    def test_sameas(self):
        env = BlendedEnvironment()
        tmpl = env.from_string('{{ foo is sameas false }}|'
                               '{{ 0 is sameas false }}')
        assert tmpl.render(foo=False) == 'True|False'

class JinjaNewStylei18nEnvironmentBug(TestCase):

    def test_num_called_num(self):

        @contextfunction
        def gettext(context, string):
            language = context.get('LANGUAGE', 'en')
            return languages.get(language, {}).get(string, string)


        @contextfunction
        def ngettext(context, s, p, n):
            language = context.get('LANGUAGE', 'en')
            if n != 1:
                return languages.get(language, {}).get(p, p)
            return languages.get(language, {}).get(s, s)

        newstyle_i18n_templates = {
           'master.html': '<title>{{ page_title|default(_("missing")) }}</title>'
                   '{% block body %}{% endblock %}',
           'child.html': '{% extends "master.html" %}{% block body %}'
                  '{% trans %}watch out{% endtrans %}{% endblock %}',
           'plural.html': '{% trans user_count %}One user online{% pluralize %}'
                   '{{ user_count }} users online{% endtrans %}',
           'stringformat.html': '{{ _("User: %(num)s", num=user_count) }}',
           'ngettext.html': '{{ ngettext("%(num)s apple", "%(num)s apples", apples) }}',
           'ngettext_long.html': '{% trans num=apples %}{{ num }} apple{% pluralize %}'
                          '{{ num }} apples{% endtrans %}',
           'transvars1.html': '{% trans %}User: {{ num }}{% endtrans %}',
           'transvars2.html': '{% trans num=count %}User: {{ num }}{% endtrans %}',
           'transvars3.html': '{% trans count=num %}User: {{ count }}{% endtrans %}',
           'novars.html': '{% trans %}%(hello)s{% endtrans %}',
           'vars.html': '{% trans %}{{ foo }}%(foo)s{% endtrans %}',
           'explicitvars.html': '{% trans foo="42" %}%(foo)s{% endtrans %}'
           }

        newstyle_i18n_env = BlendedEnvironment(
                    loader=DictLoader(newstyle_i18n_templates),
                    extensions=['jinja2.ext.i18n']
                    )

        newstyle_i18n_env.install_gettext_callables(gettext, ngettext, newstyle=True)

        source = newstyle_i18n_env.compile('''
            {% trans num=3 %}{{ num }} apple{% pluralize
            %}{{ num }} apples{% endtrans %}
        ''', raw=True)
        # quite hacky, but the only way to properly test that.  The idea is
        # that the generated code does not pass num twice (although that
        # would work) for better performance.  This only works on the
        # newstyle gettext of course
        assert re.search(r"l_ngettext, u?'\%\(num\)s apple', u?'\%\(num\)s "
                         r"apples', 3", source) is not None

class JinjaSliceBug(TestCase):

    def test_slice(self):
        env = BlendedEnvironment()
        tmpl = env.from_string('{{ foo|slice(3)|list }}|'
                               '{{ foo|slice(3, "X")|list }}')
        out = tmpl.render(foo=list(range(10)))
        assert out == ("[[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]|"
                       "[[0, 1, 2, 3], [4, 5, 6, 'X'], [7, 8, 9, 'X']]")

class JinjaParsingHexDecimalBug(TestCase):

    def test_int(self):
        env = BlendedEnvironment()
        tmpl = env.from_string('{{ "42"|int }}|{{ "ajsghasjgd"|int }}|'
                               '{{ "32.32"|int }}|{{ "0x4d32"|int(0, 16) }}|'
                               '{{ "011"|int(0, 8)}}|{{ "0x33FU"|int(0, 16) }}')
        out = tmpl.render()
        assert out == '42|0|32|19762|9|0'

class JinjaImmutableSandBoxEnvironmentBug(TestCase):

    def test_immutable_environment(self):

        import jinja2
        import pytest
        from jinja2.sandbox import SandboxedEnvironment, \
             ImmutableSandboxedEnvironment
        from jinja2.exceptions import SecurityError

        jinja2.sandbox.SandboxedEnvironment = BlendedEnvironment
        SandboxedEnvironment = BlendedEnvironment
        ImmutableSandboxedEnvironment = BlendedImmutableEnvironment
        env = ImmutableSandboxedEnvironment(dict_attrs=True)
        with pytest.raises(SecurityError):
            env.from_string('{{ [].append(23) }}').render()
        with pytest.raises(SecurityError):
            env.from_string('{{ {1:2}.clear() }}').render()


class JinjaCustomCodeGeneratorBug(TestCase):

    def test_custom_code_generator(self):

        from blended.jinjaenv import BlendedEnvironment as Environment
        from blended.jinjaenv import BlendedCodeGenerator as CodeGenerator
        #from jinja2.compiler import CodeGenerator

        class CustomCodeGenerator(CodeGenerator):
            def visit_Const(self, node, frame=None):
                # This method is pure nonsense, but works fine for testing...
                if node.value == 'foo':
                    self.write(repr('bar'))
                else:
                    super(CustomCodeGenerator, self).visit_Const(node, frame)

        class CustomEnvironment(Environment):
            code_generator_class = CustomCodeGenerator

        env = CustomEnvironment()
        tmpl = env.from_string('{% set foo = "foo" %}{{ foo }}')
        assert tmpl.render() == 'bar'

class JinjaTestAutoEscapeTestVolatileScopingBug(TestCase):

    def test_volatile_scoping(self):

        from blended.jinjaenv import BlendedEnvironment as Environment

        env = Environment(extensions=['jinja2.ext.autoescape'], sandboxed_access=False)
        tmplsource = '''
        {% autoescape val %}
            {% macro foo(x) %}
                [{{ x }}]
            {% endmacro %}
            {{ foo().__class__.__name__ }}
        {% endautoescape %}
        {{ '<testing>' }}
        '''
        tmpl = env.from_string(tmplsource)
        assert tmpl.render(val=True).split()[0] == 'Markup'
        assert tmpl.render(val=False).split()[0] == text_type.__name__

        # looking at the source we should see <testing> there in raw
        # (and then escaped as well)
        env = Environment(extensions=['jinja2.ext.autoescape'])
        pysource = env.compile(tmplsource, raw=True)
        assert '<testing>\\n' in pysource

        env = Environment(extensions=['jinja2.ext.autoescape'],
                          autoescape=True)
        pysource = env.compile(tmplsource, raw=True)
        assert '&lt;testing&gt;\\n' in pysource

