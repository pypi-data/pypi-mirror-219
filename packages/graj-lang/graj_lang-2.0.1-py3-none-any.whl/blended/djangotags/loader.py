"""
Wrapper for loading templates from the filesystem.
"""
import os
import io
import re

from django.conf import settings
from django.template import Template, TemplateDoesNotExist, Origin
from django.utils._os import safe_join
from django.core.exceptions import SuspiciousOperation

try:
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:
    from django.template.loader import BaseLoader
try:
    from django.template.utils import get_app_template_dirs
except ImportError:
    from django.template.loaders.app_directories import app_template_dirs
    lambda get_app_template_dirs: app_template_dirs

# By default, trim blocks is turned off
BLENDED_TRIM_BLOCKS = getattr(settings, 'BLENDED_TRIM_BLOCKS', False)

'''
def substitute(val):
    #import pdb;pdb.set_trace()
    if (val.group(1)==None) and (val.group(2)==None) and (val.group(3)==None) and (val.group(4)==None):
         if re.match('^\s*[\w\.]+\s*$', val.group(6)):
              return "{{%s}}" % val.group(6)
         else:
              return "{%% print %s %%}" % val.group(6).strip()
    else:
        if val.group(1):
           return val.group(1)
        elif val.group(2):
           return val.group(2)
        elif val.group(3):
           return val.group(3)
        else:
           return val.group(4)
'''

# def substitute(val):
#     #import pdb;pdb.set_trace()
#     if ((val.group(1)==None) and (val.group(2)==None) and 
#           (val.group(3)==None) and (val.group(4)==None) and 
#           (val.group(6)==None) and (val.group(7)==None)):
#         if val.group(8) is None:
#             return "{%% print %s %%}" % ''
#         else:
#             return "{%% print %s %%}" % val.group(8).strip()
#          # if re.match('^\s*[\w\.]+\s*$', val.group(8)):
#          #      return "{{%s}}" % val.group(8)
#          # else:
#          #      return "{%% print %s %%}" % val.group(8).strip()
#     else:
#         if isinstance(val.group(1), str) or val.group(1):
#            return val.group(1)
#         elif isinstance(val.group(2), str) or val.group(2):
#            return val.group(2)
#         elif isinstance(val.group(3), str) or val.group(3):
#            return val.group(3)
#         elif isinstance(val.group(4), str) or val.group(4):
#            return val.group(4)
#         elif isinstance(val.group(6), str) or val.group(6):
#            return val.group(0)
#         elif isinstance(val.group(7), str) or val.group(7):
#            return val.group(0)

# def preprocess(template_string):
#     template_string = re.sub(os.linesep + r'\Z','',template_string)
#     #template_string = template_string.strip("\n")
#     #compiled_exp_remove_new_line = re.compile('%}\n')
#     #template_string = compiled_exp_remove_new_line.sub('%}', template_string)
#     if BLENDED_TRIM_BLOCKS:
#          template_string = re.sub(r"""(?s)((?:{%\s*verbatim\s*%}.*?)?{%\s*endverbatim\s*%})|%}\n""",
#                 lambda m: (m.group(1) if m.group(1) else "%}"), template_string)
#     compiled_exp_remove_white_space_after = re.compile('-%} *\s* *')
#     template_string = compiled_exp_remove_white_space_after.sub('%}', template_string)
#     compiled_exp_remove_white_space_before = re.compile(' *\s* *{%-')
#     template_string = compiled_exp_remove_white_space_before.sub('{%', template_string)
#     compiled_exp_remove_whitespace_after_exp = re.compile('-}} *\s* *')
#     template_string = compiled_exp_remove_whitespace_after_exp.sub('}}', template_string)
#     compiled_exp_remove_whitespace_before_exp = re.compile(' *\s* *{{-')
#     template_string = compiled_exp_remove_whitespace_before_exp.sub('{{', template_string)
    
#     compiled_exp_to_allow_multiline_comment = re.compile(r'\n[ \t]*(?=(?:(?!{#).)*#})', re.S)
#     template_string = compiled_exp_to_allow_multiline_comment.sub(" ", template_string)
#     compiled_exp_to_allow_multiline_tag = re.compile(r'\n[ \t]*(?=(?:(?!{%?).)*%})', re.S)
#     template_string = compiled_exp_to_allow_multiline_tag.sub(" ", template_string)
#     compiled_exp_to_allow_multiline_var = re.compile(r'\n[ \t]*(?=(?:(?!{{?).)*}})', re.S)
#     template_string = compiled_exp_to_allow_multiline_var.sub(" ", template_string)
#     #template_string = re.sub(
#      #  r'''(?s)((?:{%\s*verbatim\s*%}.*?)?{%\s*endverbatim\s*%})|(\'{{(\s*.*\s*)}}\')|(\"{{(\s*.*\s*)}}\")|{{(\s*.*?\s*)}}(?!(\"|\'))''', substitute, template_string, re.S)
#     template_string = re.sub(
#        r'''(?s)((?:{%\s*verbatim\s*%}.*?)?{%\s*endverbatim\s*%})|(\'{{(\s*.*\s*)}}\')|(\"{{(\s*.*\s*)}}\")|"(.*?[^{{]*.*?[^}}]*?.*?)"|'(.*?[^{{]*.*?[^}}]*?.*?)'|{{(\s*.*?\s*)}}(?!(\"|\'))''', substitute, template_string, 0, re.S)

#     return template_string

def substitute(val):
 
    if ((val.group(1)==None) and (val.group(2)==None) and 
          (val.group(3)==None) and (val.group(4)==None) and 
          (val.group(6)==None) and (val.group(7)==None)):
         if re.match('^\s*[_][\w\.]+?\s*$', val.group(8), re.S):
             return "{%% print %s %%}" % val.group(8).strip()
         elif re.match('^\s*.*[\.\*\+\-\/]+.*?\s*$|^\s*\([\w\.]+.*\)*?\s*$', val.group(8), re.S):
            return "{%% print %s %%}" % val.group(8).strip()
         elif re.match('^\s*[\w\.]+?\s*$', val.group(8), re.S):
             return "{{%s}}" % val.group(8)
         else:
             return "{%% print %s %%}" % val.group(8).strip()
    else:
        if isinstance(val.group(1), str) or val.group(1):
           return val.group(1)
        elif isinstance(val.group(2), str) or val.group(2):
           if re.match('^\s*[\(\w\.\)]+?\s*$|^\s*\([\w\.]+.*\)*?\s*$', val.group(3),  re.S):
               return "'{%% print %s %%}'" % val.group(3).strip()
           else: 
                return val.group(2)
        elif isinstance(val.group(3), str) or val.group(3):
           return val.group(3)
        elif isinstance(val.group(4), str) or val.group(4):
           if re.match('^\s*[\(\w\.\)]+?\s*$|^\s*\([\w\.]+.*\)*?\s*$', val.group(5), re.S):
               return '"{%% print %s %%}"' % val.group(5).strip()
           else: 
                return val.group(4)
        elif isinstance(val.group(5), str) or val.group(5):
            return val.group(5)
        elif isinstance(val.group(6), str) or val.group(6):
            #if re.search(r'''{{(\s*.*?\s*)}}(?!(\"|\'))''', val.group(6)):
            
            string = re.sub(
       r'''{{(\s*.*?\s*)}}|(\'{{(\s*.*?\s*)}}\')|(\"{{(\s*.*?\s*)}}\")''', substitute_rec, val.group(6), 0, re.S)
            return '"%s"' % (string,)
            #return val.group(0)
        elif isinstance(val.group(7), str) or val.group(7):
            #if re.search(r'''{{(\s*.*?\s*)}}(?!(\"|\'))''', val.group(7)):
            string = re.sub(
       r'''{{(\s*.*?\s*)}}|(\'{{(\s*.*?\s*)}}\')|(\"{{(\s*.*?\s*)}}\")''', substitute_rec, val.group(7), 0, re.S)
            return "'%s'" % (string,)
            #return val.group(0)


def substitute_rec(val):
     if val.group(1) and re.match('^\s*[_].*?\s*$', val.group(1), re.S):
         return "{%% print %s %%}" % val.group(1).strip() 
     elif val.group(1) and re.match('^\s*[\w\.]+?\s*$', val.group(1)):
         return val.group(0)
     elif val.group(1) and re.match('^\s*.*[\.\*\+\-\/]+.*?\s*$|^\s*.*\([\w\.]+.*\)\s*$|^\s*.*\([\w\.]*.*\)\s*$', val.group(1), re.S):
         return "{%% print %s %%}" % val.group(1).strip()
     elif val.group(2) and re.match('^\s*[\(\w\.\)]+?\s*$|^\s*\([\w\.]+.*\)*?\s*$|^\s*.*\([\w\.]+.*\)\s*$|^\s*.*\([\w\.]*.*\)\s*$', val.group(3), re.S):    
         return "'{%% print %s %%}'" % val.group(3).strip()
     elif val.group(4) and re.match('^\s*[\(\w\.\)]+?\s*$|^\s*\([\w\.]+.*\)*?\s*$|^\s*.*\([\w\.]+.*\)\s*$|^\s*.*\([\w\.]*.*\)\s*$', val.group(5), re.S):    
         return '"{%% print %s %%}"' % val.group(5).strip()
     else:
         return val.group(0)
    


def preprocess(template_string):
    
    template_string = re.sub(os.linesep + r'\Z','',template_string)
    # template_string = template_string.strip("\n")
    # compiled_exp_remove_new_line = re.compile('%}\n')
    # template_string = compiled_exp_remove_new_line.sub('%}', template_string)

    if BLENDED_TRIM_BLOCKS:
         template_string = re.sub(r"""(?s)((?:{%\s*verbatim\s*%}.*?)?{%\s*endverbatim\s*%})|%}\n""",
                lambda m: (m.group(1) if m.group(1) else "%}"), template_string)
    compiled_exp_remove_white_space_after = re.compile('-%} *\s* *')
    template_string = compiled_exp_remove_white_space_after.sub('%}', template_string)
    compiled_exp_remove_white_space_before = re.compile(' *\s* *{%-')
    template_string = compiled_exp_remove_white_space_before.sub('{%', template_string)
    compiled_exp_remove_whitespace_after_exp = re.compile('-}} *\s* *')
    template_string = compiled_exp_remove_whitespace_after_exp.sub('}}', template_string)
    compiled_exp_remove_whitespace_before_exp = re.compile(' *\s* *{{-')
    template_string = compiled_exp_remove_whitespace_before_exp.sub('{{', template_string)

    compiled_exp_to_allow_multiline_comment = re.compile(r'\n[ \t]*(?=(?:(?!{#).)*#})', re.S)
    template_string = compiled_exp_to_allow_multiline_comment.sub(" ", template_string)
    compiled_exp_to_allow_multiline_tag = re.compile(r'\n[ \t]*(?=(?:(?!{%?).)*%})', re.S)
    template_string = compiled_exp_to_allow_multiline_tag.sub(" ", template_string)
    compiled_exp_to_allow_multiline_var = re.compile(r'\n[ \t]*(?=(?:(?!{{?).)*}})', re.S)
    template_string = compiled_exp_to_allow_multiline_var.sub(" ", template_string)


    #template_string = re.sub(
    #   r'''(?s)((?:{%\s*verbatim\s*%}.*?)?{%\s*endverbatim\s*%})|(\'{{\s*(\s*.*?\s*)?\s*}}\')|(\"{{\s*(\s*.*?\s*)?\s*}}\")|"(.*?{{.*?}}?.*?)"|'(.*?{{.*?}}?.*?)'|{{(\s*.*?\s*?)}}(?!(\"|\'))''', substitute, template_string, 0, re.S)
    
    template_string = re.sub(
       r'''(?s)((?:{%\s*verbatim\s*%}.*?)?{%\s*endverbatim\s*%})|(\'{{(\s*.*?\s*)?}}\')|(\"{{(\s*.*?\s*)?}}\")|"(.*{{.*?}}.*?)"|'(.*{{.*?}}.*?)'|{{(\s*.*?\s*)}}(?!(\"|\'))''', substitute, template_string, 0, re.S)

    return template_string



def template_from_string(template_string):
    # import pdb; pdb.set_trace()
    template_string = preprocess(template_string)
    template_obj = Template(template_string)
    return template_obj



class Loader(BaseLoader):
    
    is_usable = True
    
    '''
    In general, it is enough to define get_template_sources() and get_contents()
    for custom template loaders. get_template() will usually not need to be overridden.
    '''
    
    def get_contents(self, origin):
        # return origin
        try:
            filepath = origin.name
            with io.open(filepath, encoding=self.engine.file_charset) as fp:
                # breakpoint()
                template_string = fp.read()
                template_string = preprocess(template_string) 
                return template_string
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)
    

    def load_template_source(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        if not template_dirs:
            template_dirs = list(self.engine.dirs)
            app_dirs = get_app_template_dirs('templates')
            if app_dirs:
                 for i in app_dirs:
                     template_dirs.append(i)
        for template_dir in template_dirs:
            try:
                # breakpoint()
                yield safe_join(template_dir, template_name)
            except SuspiciousOperation:
                # The joined path was located outside of this template_dir
                # (it might be inside another one, so this isn't fatal).
                pass

    def get_template_sources(self, template_name, template_dirs=None):
        tried = []
        # a=self.load_template_sources(template_name, template_dirs)
        for filepath in self.load_template_source(template_name, template_dirs):
            try:
                with io.open(filepath, encoding=self.engine.file_charset) as fp:
                    # template_string = fp.read()
                    # template_string = preprocess(template_string) 
                    # return template_string, filepath
                    yield Origin(
                        name=filepath,
                        template_name=template_name,
                        loader=self
                    )
            except IOError:
                tried.append(filepath)
        if tried:
            error_msg = "Tried %s" % tried
        else:
            error_msg = ("Your template directories configuration is empty. "
                         "Change it to point to at least one template directory.")
        raise TemplateDoesNotExist(error_msg)
    get_template_sources.is_usable = True

