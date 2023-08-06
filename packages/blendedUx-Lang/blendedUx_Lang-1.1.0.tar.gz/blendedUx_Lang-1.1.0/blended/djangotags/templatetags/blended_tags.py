import os
import posixpath
import sys
import warnings
import collections
import datetime
import json
from copy import copy
from numbers import Number
from django.template.base import Parser as dj_parser
from django.template.base import VariableDoesNotExist

from django.template import Template
from django.template import Library, Context, RequestContext, Variable, TemplateSyntaxError
from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode, BlockNode
from django.utils.safestring import mark_safe
from django.template.exceptions import TemplateDoesNotExist
try:
    from django.template.defaultfilters import escape_filter
except ImportError:
    from django.template.defaultfilters import escape as escape_filter
try:
    from django.utils.encoding import force_text 
except ImportError:
    # This doesn't really do anything, but it probably should. Here for old Django compatibility.
    def force_text(s, *args, **kwargs):
        return str(s)
try:
    from django.utils.deprecation import RemovedInDjango110Warning as DjangoDeprecationWarning
except ImportError:
    DjangoDeprecationWarning = DeprecationWarning
try:
    from django.utils.six import string_types
except ImportError:
    string_types = TypeError
try:
    from django.template.base import Template as BaseTemplate
    template_types = (Template, BaseTemplate)
except ImportError:
    template_types = Template

from django.template.base import render_value_in_context


from blended.customtags import core, arguments, utils
from blended.customtags._compat import text_type
from blended.customtags.trimfloat import trimfloat
from blended.djangotags.loader import template_from_string
from blended.functions import builtins as builtin_funcs
from blended.customtags.exceptions import *


register = Library()

datetime_isoformat = "%Y-%m-%dT%H:%M:%SZ"
numbers_default_string_format = "%g"
PYTHON_MAJOR_VER = sys.version_info[0]


def map_func(function, *iterables):
    if PYTHON_MAJOR_VER<3:
        from itertools import imap
        return imap(function, *iterables)
    elif PYTHON_MAJOR_VER>=3: #Assuming future python versions to be more compatible with py3
        return map(function, *iterables)
    else:
        raise ("Python version incompatible")       

class Parent(core.Tag):
    parent_var = Variable('block.super')

    def render_tag(self, context):
        return self.parent_var.resolve(context)




class Do(core.Tag):
    options = core.Options(arguments.Argument("expression"))

    def render_tag(self, context, expression):
         return ""


class Set(core.Tag):
    options = core.Options(
        arguments.Argument("variable", resolve=False),
        arguments.Constant("="),
        arguments.Expression("value")
    )

    def render_tag(self, context, variable, value):
        context[variable] = value
        return ""


class Verbatim(core.Tag):
    options = core.Options(
        arguments.Literal('literal'),
        arguments.EndTag()
    )

    def render_tag(self, context, literal):
        return literal


class Autoescape(core.Tag):
    options = core.Options(
        arguments.Argument("autoescape_on"),
        arguments.NodeList("nodelist"),
        arguments.EndTag()

    )

    def render_tag(self, context, autoescape_on, nodelist):
        old_setting = context.autoescape
        context.autoescape = autoescape_on
        output = nodelist.render(context)
        context.autoescape = old_setting
        if autoescape_on:
            return mark_safe(output)
        else:
            return output


def get_macro_context(context):
    rc = context.render_context
    macro_context = rc['macros'] = rc.get('macros', Context())
    return macro_context


def set_macro_context(context, macro_context):
    rc = context.render_context
    rc['macros'] = macro_context


def get_new_context(context, initial_data=None):
    if not initial_data:
        initial_data = {}
    ## the request context will allow us to populate the context with all
    ## global/default data, but that is only available if we already have a 
    ## RequestContext via context processors 
    # if isinstance(context, RequestContext):
    #     new_context = RequestContext(context.request, initial_data, autoescape=context.autoescape)
    if isinstance(context, RequestContext):
        #new_context = RequestContext(context.request, initial_data, autoescape=context.autoescape)
        from copy import copy, deepcopy
        """
        Instantiating RequestContext constructure is causing
        all the context_processors to execute everytime this is being called.
        # deepcopy throwing TypeError("cannot serialize '_io.BufferedReader' object")
        """
        new_context = copy(context)
        new_context.update(builtin_funcs())

    ## If we don't have a RequestContext, then we need to invoke the builtins
    ## context processor directly.  User functions will not be available
    ## inside the macro body unless added originally to the macro context.

    else:
        new_context = Context(autoescape=context.autoescape)
        new_context.update(builtin_funcs())
        new_context.update(initial_data)

    return new_context


class Macro(core.Tag):
    options = core.Options(
        arguments.Argument("macroname", resolve=False),
        arguments.Constant("("),
        arguments.MultiValueArgument("arg_names", resolve=False,
                                     required=False, commas=True),
        arguments.Constant(")"),
        arguments.NodeList("nodelist"),
        arguments.EndTag()
    )

    def render_tag(self, context, macroname, arg_names, nodelist):

        def macro(*args):
            #if len(arg_names) != len(args):
            #    raise TypeError("Macro '%s' expects %s arguments, %s provided." % 
            #                    (macroname, len(arg_names), len(args)))
                
            macro_context = get_macro_context(context)
            macro_context.push()

            ## get a fully scoped context with the macros as initial data
            inner_context = get_new_context(context, copy(macro_context))
            set_macro_context(inner_context, macro_context)

            i = 0
            for arg_name in arg_names:
                try:
                  inner_context[arg_name] = args[i]
                except IndexError:
                  break
                i += 1
            rendered = nodelist.render(inner_context)
            macro_context.pop()
            return rendered
        macro.is_macro = True
        macro.name = macroname

        macrocontext = get_macro_context(context)
        macrocontext[macroname] = context[macroname] = macro
        return ""


def import_macros(context, template):

    # Does this quack like a Template?
    if not callable(getattr(template, 'render', None)):
        # If not, as in include, we'll try get_template
        template = get_template(template)

    local_context = get_new_context(context)
    ## in future versions of Django, base templates may be wrapped by engine templates
    getattr(template, 'template', template).render(local_context)
    macro_dict = {}
    for sub in local_context:
        for key, value in sub.items():
            if getattr(value, 'is_macro', False) and key not in macro_dict:
                macro_dict[key] = value
    return macro_dict


class Import(core.Tag):
    options = core.Options(
        arguments.Argument("template"),
        arguments.Constant("as"),
        arguments.Argument("asname", resolve=False)
    )

    def render_tag(self, context, template, asname):
        context[asname] = import_macros(context, template)
        return ""


class From(core.Tag):
    options = core.Options(
        arguments.Argument("template"),
        arguments.Constant("import"),
        arguments.Argument("name", resolve=False),
        arguments.Optional(
            arguments.Constant("as"),
            arguments.Argument("asname", resolve=False)
        ),
        arguments.Repetition(
            "names",
            arguments.Constant(","),
            arguments.Argument("name", resolve=False),
            arguments.Optional(
                arguments.Constant("as"),
                arguments.Argument("asname", resolve=False)
            ),
        )
    )

    def render_tag(self, context, template, name, asname=None, names=None):
        macros_dict = import_macros(context, template)
        if name not in macros_dict:
            raise ImportError("Macro name '%s' not found in template." % name)
        if asname:
            context[asname] = macros_dict[name]
        else:
            context[name] = macros_dict[name]
        for nameobj in names:
            name = nameobj['name']
            if name not in macros_dict:
                raise ImportError("Macro name '%s' not found in template." % name)
            if 'asname' in nameobj:
                context[nameobj['asname']] = macros_dict[nameobj['name']]
            else:
                context[nameobj['name']] = macros_dict[nameobj['name']]
        
        return ''


def construct_relative_path(current_template_name, relative_name):
    """
    Convert a relative path (starting with './' or '../') to the full template
    name based on the current_template_name.
    """
    new_name = relative_name.strip("'\"")
    # breakpoint()
    if not new_name.startswith(("./", "../")):
        # relative_name is a variable or a literal that doesn't contain a
        # relative path.
        return relative_name
    new_name = posixpath.normpath(
        posixpath.join(
            posixpath.dirname(current_template_name.lstrip("/")),
            new_name,
        )
    )

    if new_name.startswith("../"):
        if repr(relative_name).startswith("'\""):           # this will generate error for "extend tag" as Django wanted  
            raise TemplateSyntaxError(
                "The relative path '%s' points outside the file hierarchy that "
                "template '%s' is in." % (relative_name, current_template_name)
            )
        else:           # this will generate error for "include tag" as Django wanted                   
            raise TemplateSyntaxError(
                "The relative path '%s' points outside the file hierarchy that "
                "template '%s' is in." % (json.dumps(relative_name), current_template_name)
            )
    if current_template_name.lstrip("/") == new_name:
        raise TemplateSyntaxError(
            "The relative path '%s' was translated to template name '%s', the "
            "same template in which the tag appears."
            % (relative_name, current_template_name)
        )
    has_quotes = (
        relative_name.startswith(('"', "'")) and relative_name[0] == relative_name[-1]
    )
    # if not get_template(new_name):
    #     breakpoint()
    return f'"{new_name}"' if has_quotes else new_name



class Include(core.Tag):
    options = core.Options(
        arguments.Argument("template"),
        arguments.Optional(
            arguments.Constant("ignore"),
            arguments.Constant("missing"),
        ),
        arguments.OneOf(
            arguments.MultiArgument(
                arguments.Constant("with"),
                arguments.OneOf(
                    arguments.MultiValueKeywordArgument("extra_context", required=True),
                    arguments.Argument("extra_context"),
                ),
                arguments.Flag('isolation', true_values=['only'], default=False, 
                               case_sensitive=True)
            ),
            arguments.MultiArgument(
                arguments.Flag('isolation', true_values=['only'], case_sensitive=True),
                arguments.Constant("with"),
                arguments.OneOf(
                    arguments.MultiValueKeywordArgument("extra_context", required=True),
                    arguments.Argument("extra_context"),
                )
            ),
            arguments.Flag('isolation', true_values=['only'], default=False, 
                           case_sensitive=True),
        ),
    )

    def render_tag(self, context, template, extra_context=None, isolation=False, ignore=False):
        try:
            extra_context = extra_context if extra_context else {}

            if not isinstance(extra_context, collections.abc.Mapping):
                raise TemplateSyntaxError(
                    "Extra context passed to include tag must act like a dict.")

            # Does this quack like a Template?
            # added as like in django == 4.1.7
            if not callable(getattr(template, 'render', None)):
                # If not, we'll try get_template
                # template = context.template.engine.get_template(template)
                # if "./../three.html" in template:
                #     breakpoint()
                template_name = template
                if isinstance(template_name, str):
                    template_name = (
                        construct_relative_path(
                            self.origin.template_name,
                            template_name,
                        ),
                    )
                else:
                    # this will handle the case if typeof template_name is Nonetype, can't iterate through NoneType
                    if template_name == None:    
                        raise TemplateDoesNotExist("No template names provided")
                    
                    template_name = tuple(template_name)
                cache = context.render_context.dicts[0].setdefault(self, {})
                template = cache.get(template_name)
                if template is None:
                    template = context.template.engine.select_template(template_name)
                    cache[template_name] = template
            elif hasattr(template, "template"):
                template = template.template
            
    
            old_ae_setting = context.autoescape
            if old_ae_setting:
                context.autoescape = not old_ae_setting
            if isolation:
                rendered = template.render(get_new_context(context, extra_context))
                context.autoescape = old_ae_setting
                return rendered

            ## this should be implemented as 'with context.push(**extra_context)'
            ## but we can't do that because we are supporting old Django
            
            context.update(extra_context)
            rendered = template.render(context)
            context.pop()
            context.autoescape = old_ae_setting
            return rendered
        # modified the exception because Blended support for "ignore missing" argument with include tag
        # Django remove the "ignore missing" functionalities from version 2.x
        except TemplateDoesNotExist:
            bits = self.token.split_contents()
            if bits[-2] == "ignore" and bits[-1] == "missing":
                if hasattr(context, 'template'):
                    # print(context.template.name)
                    if context.template.engine.debug:
                        raise
                    return ''
                else:
                    from django.conf import settings
                    if settings.DEBUG:
                        raise 
                    return ''
            elif template_name == None:
                raise TemplateDoesNotExist("No template names provided")
            else:
                raise TemplateDoesNotExist("".join(template_name))


class If(core.Tag):
    options = core.Options(
        arguments.Argument('conditional'),
        arguments.NodeList('nodelist'),
        arguments.Repetition(
            'elifs',
            arguments.BlockTag(
                'elif',
                arguments.Argument('conditional'),
                arguments.NodeList('nodelist', endtags=['elif','else','endif']),
            ),
        ),
        arguments.Optional(
            arguments.BlockTag('else'),
            arguments.NodeList('elsenodelist'),
        ),
        
        arguments.EndTag()
    )

    def render_tag(self, context, conditional, nodelist, elifs, elsenodelist=None):
        if conditional:                
            return nodelist.render(context)
        for block in elifs:
            if block['conditional']:
                return block['nodelist'].render(context)
        if elsenodelist:
            return elsenodelist.render(context)
        return ''

        
        

class Ifblock(core.Tag):
    name = 'ifblock'
    options = core.Options(
        arguments.MultiValueArgument('block_names', resolve=False),
        arguments.NodeList('nodelist'),
        arguments.Optional(
            arguments.BlockTag('else'),
            arguments.NodeList('elsenodelist'),
        ),
        arguments.EndTag()        
    )
    
    def render_tag(self, context, block_names, nodelist, elsenodelist=None):
        # breakpoint()
        nodes_list = context.template.nodelist.get_nodes_by_type(BlockNode)
        result = []
        for node in nodes_list:
            if node.name in block_names:
                exp_value = node.render(context).strip()
            else:
                exp_value = ''        
            result.append(exp_value)
        conditional = ''
        for val in result:
            conditional = (conditional or val)
        if conditional:
            return nodelist.render(context)
        if elsenodelist:
            return elsenodelist.render(context)        
        return '' 

class For(core.Tag):
    options = core.Options(
        arguments.MultiValueArgument('loopvars', resolve=False, commas=True),
        arguments.Constant('in'),
        arguments.Argument('values'),
        arguments.Flag('is_reversed', true_values=['reversed'], default=False),
        arguments.NodeList('pre_empty'),
        arguments.Optional(
            arguments.OneOf(
                arguments.BlockTag('empty'),
                arguments.BlockTag('else'),
            ),
            arguments.NodeList('post_empty'),
        ),
        arguments.EndTag()
    )

    def render_tag(self, context, loopvars, values, is_reversed, pre_empty, post_empty=None):
        if 'forloop' in context:
            parentloop = context['forloop']
        else:
            parentloop = {}
        #with context.push():
        context.push()
        if values is None:
            values = []
        if not hasattr(values, '__len__'):
            values = list(values)
        len_values = len(values)
        if len_values < 1:
            retval = post_empty.render(context)
        else:
            nodelist = []
            if is_reversed:
                values = reversed(values)
            num_loopvars = len(loopvars)
            unpack = num_loopvars > 1
            # Create a forloop value in the context.  We'll update counters on each
            # iteration just below.
            loop_dict = context['forloop'] = context['loop'] = {'parentloop': parentloop}
            for i, item in enumerate(values):
                # Shortcuts for current loop iteration number.
                loop_dict['counter0'] = loop_dict['index0'] = i
                loop_dict['counter'] = loop_dict['index'] = i + 1
                # Reverse counter iteration numbers.
                loop_dict['revcounter'] = loop_dict['revindex'] = len_values - i
                loop_dict['revcounter0'] = loop_dict['revindex0'] = len_values - i - 1
                # Boolean values designating first and last times through loop.
                loop_dict['first'] = (i == 0)
                loop_dict['last'] = (i == len_values - 1)

                pop_context = False
                if unpack:
                    # If there are multiple loop variables, unpack the item into
                    # them.

                    # To complete this deprecation, remove from here to the
                    # try/except block as well as the try/except itself,
                    # leaving `unpacked_vars = ...` and the "else" statements.
                    if isinstance(item, str):
                        len_item = len(item)
                    elif not isinstance(item, (list, tuple)):
                        len_item = 1
                    else:
                        len_item = len(item)
                    # Check loop variable count before unpacking
                    if num_loopvars != len_item:
                        # breakpoint()
                        warnings.warn(
                            "Need {} values to unpack in for loop; got {}. "
                            "This will raise an exception in Django 1.10."
                            .format(num_loopvars, len_item),
                            DjangoDeprecationWarning)
                        raise ValueError(                   
                            "Need {} values to unpack in for loop; got {}. ".format(
                                num_loopvars, len_item
                            ),
                        )
                    try:
                        unpacked_vars = dict(zip(loopvars, item))
                    except TypeError:
                        pass
                    else:
                        pop_context = True
                        context.update(unpacked_vars)
                else:
                    context[loopvars[0]] = item
                # In debug mode provide the source of the node which raised
                # the exception
                try:
                    debug_mode = context.template.engine.debug
                except:
                    from django.conf import settings
                    debug_mode = settings.DEBUG
                if debug_mode:
                    for node in pre_empty:
                        try:
                            nodelist.append(node.render(context))
                        except Exception as e:
                            if not hasattr(e, 'django_template_source'):
                                e.django_template_source = node.source
                            raise
                else:
                    for node in pre_empty:
                        nodelist.append(node.render(context))
                if pop_context:
                    # The loop variables were pushed on to the context so pop them
                    # off again. This is necessary because the tag lets the length
                    # of loopvars differ to the length of each set of items and we
                    # don't want to leave any vars from the previous loop on the
                    # context.
                    context.pop()
            retval = mark_safe(''.join(force_text(n) for n in nodelist))
        
        context.pop()
        return retval


extends_options = core.Options(arguments.Expression())
extends_options.initialize('extends')

def do_extends(parser, token):
    bits = token.split_contents()
    if len(bits) <= 1:
        raise TemplateSyntaxError("'%s' takes one argument" % bits[0])

    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    '''
     I have to pass this bits[1] in value of '<StringValue(Const(value='./dir2/one.html'))>'
     container.tag_args[0].var --> Const(value='./dir2/one.html')
     container.tag_args[0].var.value --> './dir2/one.html'

    '''
    # breakpoint()
    container = utils.Container()
    extends_options.parse(parser, token, container)
    if (bits[1] != token.split_contents()[-1]):
        container.tag_args[0].var.value = bits[1].strip('"')

    parent_name = container.tag_args[0]

    # breakpoint()
    
    parent_name.token = token
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError(
            "'%s' cannot appear more than once in the same template" % bits[0])
    try:
        return ExtendsNode(nodelist, parent_name)
    except TypeError:
        return ExtendsNode(nodelist, None, parent_name)
        

def items_filter(dict_val):
    try:
        keys = sorted(dict_val.keys())
    except:
        keys = dict_val.keys() 
        keys.sort()
    return [(key, dict_val[key]) for key in keys]


def number_filter(value, default=0):
    """Convert the value into an integer. If the
    conversion doesn't work it will return ``0``. You can
    override this default using the first parameter. You
    can also override the default base (10) in the second
    parameter, which handles input with prefixes such as
    0b, 0o and 0x for bases 2, 8 and 16 respectively.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def template_filter(template):
    if isinstance(template, string_types):
        template_obj = template_from_string(template)
        return template_obj
    elif isinstance(template, template_types):
        return template
    else:
        #raise TypeError("The `template` filter must be applied only to strings or templates.")
        ## or just convert it to a string first:
        template_obj = template_from_string(str(template))
        return template_obj 
    


def render_filter(template, context=None, autoescape=None):
    autoescape = False if autoescape is None else autoescape

    if context is None:
        context = {}
    elif not isinstance(context, (dict, Context)):
        raise TypeError("The `render` filter must be passed a dict or Context as an argument.")
    if not hasattr(template, 'render'):
        raise TypeError("The `render` filter should only be applied to Template instances.")

    new_context = Context(context, autoescape=autoescape)
    new_context.update(builtin_funcs())
    return template.render(new_context)


def string_filter(value, format=None, recursion= False):
    #return text_type(value)
    
    try: #try except block to fix the absence of unicode in py3
        if value and isinstance(value, unicode):
            value = value.encode('utf-8')
    except NameError:
        pass

    if format:
        if isinstance(value, Number) and not isinstance(value, bool):
            return format % value
        if isinstance(value, str):
            return format % trimfloat(value)
        elif isinstance(value, datetime.datetime):
            return datetime.datetime.strftime(value, format)
        elif isinstance(value, (list, tuple)):
            rendered = []
            for item in value:
                rendered.append(string_filter(item))
            return format % tuple(rendered)
        else:
            format % string_filter(value)
    else:
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, str):              
            if recursion:
                return "'%s'" % value
            else:
                return "%s" %  value   
        elif isinstance(value, Number):
            return str(trimfloat(value))
        elif isinstance(value, datetime.datetime ):
             return datetime.datetime.strftime(value, datetime_isoformat)
        elif isinstance(value, (list, tuple)):
            rendered = []
            for item in value:
                rendered.append(string_filter(item, recursion= True))
            return "[%s]" % ", ".join(rendered)
        elif isinstance(value, dict):
            rendered = []
            for key in sorted(value.keys()):
                rendered_value = string_filter(value[key], recursion= True)
                rendered.append('\'%s\': %s' % (key, rendered_value))
            return "{%s}" % ", ".join(rendered)
        else:
            raise TypeError("Type %s unsupported by string filter" % value.__class__)


def datetime_filter(obj, formatting=None):
    """this filter accepts string, list or dates and return a datetime object.
    """
    if isinstance(obj, datetime.datetime):
        return obj
    elif isinstance(obj, text_type):
        if formatting:
            return datetime.datetime.strptime(obj, formatting)
        else:
            return datetime.datetime.strptime(obj, datetime_isoformat)
    elif isinstance(obj, list):
        return datetime.datetime(*map_func(int, obj), tzinfo=None)

from django.utils.safestring import SafeText
class Print(core.Tag):
    options = core.Options(arguments.Argument("expression"))
    def render_tag(self, context, expression):
        expression = '' if expression is None or (isinstance(expression, SafeText) and expression == 'None') else expression
        return render_value_in_context(expression, context)


from django.template.defaultfilters import first


# register.tag(Verbatim.as_tag())            #use verbatim default

register.tag(If.as_tag())
register.tag(Ifblock.as_tag())


# # 
register.tag(Parent.as_tag())
register.tag(Print.as_tag())
register.tag(Do.as_tag())
register.tag(Set.as_tag())
register.tag(Import.as_tag())
register.tag(From.as_tag())
register.tag(For.as_tag())
register.tag(Autoescape.as_tag())
register.tag(Macro.as_tag())
register.tag(Include.as_tag())
# add due to blended
register.tag('extends', do_extends)
register.filter('items', items_filter)
register.filter('number', number_filter)
register.filter('e', escape_filter)
register.filter('escape', escape_filter)
register.filter('string', string_filter)
register.filter('template', template_filter)
register.filter('render', render_filter, needs_autoescape=True)
register.filter('datetime', datetime_filter)
