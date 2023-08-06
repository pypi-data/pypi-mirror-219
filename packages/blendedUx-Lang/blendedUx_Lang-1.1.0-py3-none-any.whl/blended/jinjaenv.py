
import os
import re
import sys
import jinja2
import unittest
import json
from jinja2.utils import htmlsafe_json_dumps as Markup    # add for Markup
from unittest import TestCase
from jinja2 import Environment, Template
from jinja2.compiler import CodeGenerator
from jinja2.runtime import Undefined 
# from jinja2 import Undefined 
from jinja2.sandbox import safe_range
from jinja2.nodes import OverlayScope
from collections.abc import Mapping
import traceback
import sys
import re
import datetime
from jinja2.parser import Parser
from numbers import Number
from functools import reduce

import jinja2
import jinja2.ext
import jinja2.sandbox

from jinja2 import nodes
from jinja2.runtime import  Macro
from jinja2.environment import TemplateExpression
from blended._compat import encode_filename, string_types, iteritems,\
     text_type, imap
from jinja2.defaults import BLOCK_START_STRING,\
    BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING,\
    COMMENT_START_STRING, COMMENT_END_STRING, LINE_STATEMENT_PREFIX,\
    LINE_COMMENT_PREFIX, TRIM_BLOCKS, NEWLINE_SEQUENCE,\
    KEEP_TRAILING_NEWLINE, LSTRIP_BLOCKS


from blended.functions import builtins
from blended.trimfloat import trimfloat, trimint


class BlendedParser(jinja2.parser.Parser):
    """
    This parser subclass overrides the parsing of the include tag, in order to provide
    a local context feature.  It also overrides parse_primary to ensure that numbers are
    printed without trailing zeros.
    """
    def _wrap_as_const(self, as_const):
        """
        """
        def as_const_wrapper(eval_ctx=None):
            """
            """
            value = as_const(eval_ctx)
            if isinstance(value, Number):
                return self.environment._trimfloat(value)
            return value
        return as_const_wrapper

    def _wrap_parse(parse_method):
        """
        """
        def parse_wrapper(self, *args, **kwargs):
            """
            """
            node = parse_method(self, *args, **kwargs)
            if node == None:              # add this because sometimes may be node is NoneType object
                return node
            node.as_const = self._wrap_as_const(node.as_const)
            return node
        
        return parse_wrapper

    parse_primary = _wrap_parse(jinja2.parser.Parser.parse_primary)
    parse_filter = _wrap_parse(jinja2.parser.Parser.parse_filter)
    
    def parse_include(self):
        """
        Reimplementation of Parser.parse_include, necessary for new Include functionality
        """
        lineno = lineno = next(self.stream).lineno
        node = nodes.Include(lineno=lineno)
        node.fields = nodes.Include.fields + ('with_expression',) ## compiler needs this

        node.template = self.parse_expression()
        if self.stream.current.test('name:ignore') and\
           self.stream.look().test('name:missing'):
            node.ignore_missing = True
            self.stream.skip(2)
        else:
            node.ignore_missing = False

        node.with_expression = None
        if self.stream.current.test_any('name:with', 'name:without') and\
           self.stream.look().test('name:context'):
            node.with_context = next(self.stream).value == 'with'
            self.stream.skip()
        elif self.stream.current.test('name:with'):
            self.stream.skip()
            node.with_expression = self.parse_expression()
            if self.stream.current.test('name:only'):
                node.with_context = False
                self.stream.skip()
            else:
                node.with_context = True

        elif self.stream.current.test('name:only'):
            node.with_context = False
            self.stream.skip()
        else:
            node.with_context = True
        return node


# add custom extension
class CommentExtension(jinja2.ext.Extension):
    """Extension for comment tag."""
    tags = set(['comment'])

    def parse(self, parser):
        token = parser.stream.current
        lineno = next(parser.stream).lineno
        if token.type == 'name' and token.value == 'comment':
            parser.parse_statements(['name:endcomment'], drop_needle=True)
            return nodes.Const("")
        else:
            jinja2.exceptions.TemplateSyntaxError("Expected token 'comment'")

class ParentExtension(jinja2.ext.Extension):
    """Extension for Parent tag."""
    tags = set(['parent'])

    def parse(self, parser):
        """
        """
        lineno = next(parser.stream).lineno
        name_node = nodes.Name('super', 'load', lineno=lineno)
        call_node = nodes.Call(name_node, [], [], None, None, lineno=lineno)
        outp_node = nodes.Output([call_node], lineno=lineno)
        return outp_node

class IfblockExtension(jinja2.ext.Extension):
    """Extension for ifblock tag."""
    tags = set(['ifblock'])

    def parse(self, parser):
        """
        Parser method for ifblock tag
        """
        lineno = parser.stream.expect('name:ifblock').lineno

        params = self.get_inline_params(parser.stream)
        node = result = nodes.If(lineno=lineno)
        param_count = len(params)

        if param_count == 1:
            node.test = self.build_test(params[0], lineno)
        else:
            node.test = self.get_or_expr(params, param_count-1, lineno)

        node.body = parser.parse_statements(('name:elif','name:else', 'name:endifblock'))
        node.elif_ = []
        token = next(parser.stream)
        if token.test("name:elif"):
            node = nodes.If(lineno=self.stream.current.lineno)
            result.elif_.append(node)

        elif token.test('name:else'):
            node.else_ = parser.parse_statements(('name:endifblock',), drop_needle=True)
        else:
            node.else_ = []
        return result

    def get_or_expr(self, params, index, lineno):
        if index == 0:
            return self.build_test(params[0], lineno)
        return nodes.Or(self.get_or_expr(params, index-1, lineno), self.build_test(params[index], lineno), lineno=lineno)

    def build_test(self, block_name, lineno):
        """
        """
        name_node = nodes.Name('self', 'load', lineno=lineno)
        attr_node = nodes.Getattr(name_node, block_name, 'load', lineno=lineno)
        call_node = nodes.Call(attr_node, [], [], None, None, lineno=lineno)
        return nodes.Filter(call_node, 'trim', [], [], None, None, lineno=lineno)

    def get_inline_params(self, parser_stream):
        params = []
        while(parser_stream.current.type != 'block_end' ):
            if (parser_stream.current.type == 'name'):
                params.append(parser_stream.current.value)
                next(parser_stream)
            else:
                raise jinja2.exceptions.TemplateSyntaxError("Expected block name.")
        return params



def number_filter(value, default=0):
    """Convert the value into an number. basically in float type
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@jinja2.pass_eval_context
def render_filter(eval_ctx, template, context=None):
    """renders the context in the template object.
    """
    if context is None:
        context = {}
    elif not isinstance(context, dict):
        raise TypeError("The `render` filter can only be passed a dict as an argument.")
    if hasattr(template, 'render'):
        return template.render(context)
    else:
        raise TypeError("The `render` filter should only be "
                        "applied to objecst that implement `render`.")


datetime_isoformat = "%Y-%m-%dT%H:%M:%SZ"
numbers_default_string_format = "%g"
# def datetime_filter(obj, formatting=None):
#     """
#     Return a datetime object for the current time of the day
#     """
#     return datetime.datetime.now()

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
        return datetime.datetime(*imap(int, obj), tzinfo=None)



class TemplateNull(object):
    """object of class represents 'null' which is replacing None in string_filter
    """
    def __repr__(self):
        return "null"

class TemplateTrue(object):
    """object of class represents 'true' which is replacing True in string_filter
    """
    def __repr__(self):
        return "true"

class TemplateFalse(object):
    """object of class represents 'false' which is replacing False in string_filter
    """
    def __repr__(self):
        return "false"

null = TemplateNull()
true = TemplateTrue()
false = TemplateFalse()

# use custom string filter we can modified string wrt its format


def string_filter(value, format=None, recursion=False):

    try:  # try except block to fix the absence of unicode in py3
        if value and isinstance(value, str):
            value = value
    except NameError:
        pass
    # print(value)
    if format:
        if isinstance(value, Number) and not isinstance(value, bool):
            return format % value
        if isinstance(value, str):
            return format % trimfloat(value)        #include  trimfloat
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
                return "%s" % value
        elif isinstance(value, Number):
            return str(trimfloat(value))              # include trimfloat
        elif isinstance(value, datetime.datetime):
            return datetime.datetime.strftime(value, datetime_isoformat)
        elif isinstance(value, (list, tuple)):
            rendered = []
            for item in value:
                rendered.append(string_filter(item, recursion=True))
            return "[%s]" % ", ".join(rendered)
        elif isinstance(value, dict):
            rendered = []
            for key in sorted(value.keys()):
                rendered_value = string_filter(value[key], recursion=True)
                rendered.append('\'%s\': %s' % (key, rendered_value))
            return "{%s}" % ", ".join(rendered)
        # elif isinstance(value, type):
        #     return value.__class__
        else:
            raise TypeError("Type %s unsupported by string filter" % value.__class__)


from jinja2.filters import do_dictsort
filters_add = {
    "render": render_filter,
    "items": do_dictsort,
    "string": string_filter,
    "number": number_filter,
    "datetime": datetime_filter,
}
#


class BlendedTemplate(jinja2.environment.Template):
    """Template class for Blended"""
    spontaneous_environments = jinja2.utils.LRUCache(10)

    def __new__(cls, source,
                block_start_string=BLOCK_START_STRING,
                block_end_string=BLOCK_END_STRING,
                variable_start_string=VARIABLE_START_STRING,
                variable_end_string=VARIABLE_END_STRING,
                comment_start_string=COMMENT_START_STRING,
                comment_end_string=COMMENT_END_STRING,
                line_statement_prefix=LINE_STATEMENT_PREFIX,
                line_comment_prefix=LINE_COMMENT_PREFIX,
                trim_blocks=TRIM_BLOCKS,
                lstrip_blocks=LSTRIP_BLOCKS,
                newline_sequence=NEWLINE_SEQUENCE,
                keep_trailing_newline=KEEP_TRAILING_NEWLINE,
                extensions=(),
                optimized=True,
                undefined=Undefined,
                finalize=None,
                autoescape=False,
                trim_floats=True,
                dict_attrs=False,
                enable_async=False,
                ):
        # only changed this to use BlendedEnvironment
        env = cls.get_spontaneous_blended_environment(
            block_start_string, block_end_string, variable_start_string,
            variable_end_string, comment_start_string, comment_end_string,
            line_statement_prefix, line_comment_prefix, trim_blocks,
            lstrip_blocks, newline_sequence, keep_trailing_newline,
            frozenset(extensions), optimized, undefined, finalize, autoescape,
            trim_floats, dict_attrs,enable_async, None, 0, False, None)
        return env.from_string(source, template_class=cls)

    @classmethod
    def get_spontaneous_blended_environment(cls, *args):
        """This is just implemented here to be able to use BlendedEnvironment"""
        try:
            env = cls.spontaneous_environments.get(args)
        except TypeError:
            return BlendedEnvironment(*args)
        if env is not None:
            return env
        cls.spontaneous_environments[args] = env = BlendedEnvironment(*args)
        env.shared = True
        return env
    
    def new_context(self, vars=None, shared=False, locals=None, args=None):
        """Reimplementation of Template.new_context,
        needed for handling Include node args.
        """
        
        if args:
            new_locals = dict(locals, **args) if locals else {}
            # for key, value in new_locals.items():
            #     new_locals[key] = value
        else:
            new_locals = locals
        return jinja2.runtime.new_context(self.environment, self.name, self.blocks,
                                          vars, shared, self.globals, new_locals)
    
    
              
        

# Adding new proper jinja environment with some additional features
class BlendedEnvironment(jinja2.sandbox.SandboxedEnvironment):

    template_class = BlendedTemplate                 # Blended template class
    EXTENSIONS = [ ParentExtension, IfblockExtension, CommentExtension, jinja2.ext.i18n ]           
    # jinja don't have ParentExtension, jinja use super() instead of parent

    def __init__(self,
                 block_start_string=BLOCK_START_STRING,
                 block_end_string=BLOCK_END_STRING,
                 variable_start_string=VARIABLE_START_STRING,
                 variable_end_string=VARIABLE_END_STRING,
                 comment_start_string=COMMENT_START_STRING,
                 comment_end_string=COMMENT_END_STRING,
                 line_statement_prefix=LINE_STATEMENT_PREFIX,
                 line_comment_prefix=LINE_COMMENT_PREFIX,
                 trim_blocks=TRIM_BLOCKS,
                 lstrip_blocks=LSTRIP_BLOCKS,
                 newline_sequence=NEWLINE_SEQUENCE,
                 keep_trailing_newline=True,
                 extensions=(),
                 optimized=True,
                 undefined=Undefined,
                 finalize=None,
                 autoescape=False,
                 loader=None,
                 cache_size=400,
                 auto_reload=True,
                 bytecode_cache=None,
                 trim_floats=True,
                 sandboxed_access=True,
                 dict_attrs=False,
                 enable_async=False,
                 ):
        """
        The new extensions and functions are added to the environment here
        """
        self.sandboxed = sandboxed_access       # adding the sandboxed parameter
        self.trim_floats = trim_floats
        self.dict_attrs = dict_attrs
        self.sandboxed_access = sandboxed_access
        self.is_async = enable_async
        extensions = list(extensions)
        extensions.extend(self.EXTENSIONS)
        super(BlendedEnvironment, self).__init__(block_start_string,
                                                 block_end_string,
                                                 variable_start_string,
                                                 variable_end_string,
                                                 comment_start_string,
                                                 comment_end_string,
                                                 line_statement_prefix,
                                                 line_comment_prefix,
                                                 trim_blocks,
                                                 lstrip_blocks,
                                                 newline_sequence,
                                                 keep_trailing_newline,
                                                 extensions,
                                                 optimized,
                                                 undefined,
                                                 finalize,
                                                 autoescape,
                                                 loader,
                                                 cache_size,
                                                 auto_reload,
                                                 bytecode_cache,
                                                 enable_async        # by adding enable async at this point solve all test related to async_filters
                                                 )
        
        self.globals.update(builtins())
        self.filters.update(filters_add)
        self.globals.update({"null": None})
        self.globals["range"] = safe_range      # By adding "safe_range" then in this env, only iterate 10000 times in loop
        
        

        def template_filter(template):
            """filter to create template from the string"""
            if isinstance(template, jinja2.environment.Template):
                return template
            elif isinstance(template, string_types):
                return self.from_string(template)
            else:
                raise TypeError("The `template` filter must only operate on "
                                "strings or template instances.")

        self.filters['template'] = template_filter
        self.filters.update(filters_add)
    def __substitute(self, val):
        """Substitution of verbaim to raw performs here
        """
        if re.match(r'''{%\s*verbatim\s*%}(.*?){%\s*endverbatim\s*%}''',
                    val.group(0), re.S):
            return "{%% raw %%}%s{%% endraw %%}" % val.group(1)
        elif re.match(r'''{%\s*verbatim\s*%}''', val.group(0)):
            return "{% raw %}"

    def __add_newline(self, val):
        """New line after endverbatim tag checks here
        If it newline followed by endverbatim tag this regex
        add an additional newline after endverbatim so single
        newline remove when trim_block is true
        """
        content = val.group(1)
        if re.match('\n.*', content, re.S):
            return "{%% endverbatim %%}\n%s" % content
        else:
            return "{%% endverbatim %%}%s" % content

    def preprocess(self, source, name=None, filename=None):
        """Preprocesses the source with all extensions.  This is automatically
        called for all parsing and compiling methods but *not* for :meth:`lex`
        because there you usually only want the actual source tokenized.
        Regex for conversion of verbatim to raw tag.
        """
        if self.trim_blocks:
            source = re.sub(r'''{%\s*endverbatim\s*%}(\n.*?)''', self.__add_newline, source, re.S)
        ptrn = r'''(?s)(?:{%\s*verbatim\s*%}(.*?))?{%\s*endverbatim\s*%}|{%\s*verbatim\s*%}'''
        source = re.sub(ptrn, self.__substitute, source, re.S)

        return reduce(lambda s, e: e.preprocess(s, name, filename),
                      self.iter_extensions(), text_type(source))

    def _parse(self, source, name, filename):
        """overridden to change Parser to BlendedParser"""
        return BlendedParser(self, source, name, encode_filename(filename)).parse()

    def _generate(self, source, name, filename, defer_init=False, optimized=True):
        """
        Should be same algorithm as superclass, but with BlendedCodeGenerator instead.
        This is the place to look at the compiled code.
        """
        if not isinstance(source, nodes.Template):
            raise TypeError('Can\'t compile non template nodes')

        generator = BlendedCodeGenerator(self, name, filename, defer_init=defer_init, optimized=optimized)
        generator.visit(source)
        result = generator.stream.getvalue()
        return result
    def _trimfloat(self, value):
        """
        trimfloat method to remove fractional part from float value.
        """
        if self.trim_floats and isinstance(value, Number) and not (isinstance(value, bool) or isinstance(value, complex)):
            if isinstance(value, int):
                return trimint(value)     # include trimint
            else:
                return trimfloat(value)   # include trimfloat
        return value

    def getattr(self, obj, attribute):
        """
        """
        if not self.dict_attrs and isinstance(obj, Mapping):
            try:
                return self._trimfloat(obj[attribute])
            except (TypeError, LookupError):
                return self.undefined(obj=obj, name=attribute)
        if self.sandboxed_access:
            return self._trimfloat(super(BlendedEnvironment, self).getattr(obj, attribute))
        else:
            CurrentEnv = self.__class__
            while object not in CurrentEnv.__bases__:
                CurrentEnv = CurrentEnv.__bases__[0]
            return self._trimfloat(CurrentEnv.getattr(self, obj, attribute))

    def getitem(self, obj, argument):
        """
        """
        if not self.dict_attrs and isinstance(obj, Mapping):
            try:
                return self._trimfloat(obj[argument])
            except (TypeError, LookupError):
                return self.undefined(obj=obj, name=argument)
        return self._trimfloat(super(BlendedEnvironment, self).getitem(obj, argument))


class BlendedImmutableEnvironment(BlendedEnvironment):
    '''

    '''
    def __init__(self,
                 block_start_string=BLOCK_START_STRING,
                 block_end_string=BLOCK_END_STRING,
                 variable_start_string=VARIABLE_START_STRING,
                 variable_end_string=VARIABLE_END_STRING,
                 comment_start_string=COMMENT_START_STRING,
                 comment_end_string=COMMENT_END_STRING,
                 line_statement_prefix=LINE_STATEMENT_PREFIX,
                 line_comment_prefix=LINE_COMMENT_PREFIX,
                 trim_blocks=TRIM_BLOCKS,
                 lstrip_blocks=LSTRIP_BLOCKS,
                 newline_sequence=NEWLINE_SEQUENCE,
                 keep_trailing_newline=True,
                 extensions=(),
                 optimized=True,
                 undefined=Undefined,
                 finalize=None,
                 autoescape=False,
                 loader=None,
                 cache_size=400,
                 auto_reload=True,
                 bytecode_cache=None,
                 trim_floats=True,
                 sandboxed_access=True,
                 dict_attrs=True,
                 enable_async=False,
                 ):
                 
        super(BlendedImmutableEnvironment, self).__init__(block_start_string,
                 block_end_string, variable_start_string, variable_end_string,
                 comment_start_string, comment_end_string, line_statement_prefix,
                 line_comment_prefix, trim_blocks, lstrip_blocks, newline_sequence,
                 keep_trailing_newline, extensions, optimized, undefined,
                 finalize, autoescape, loader, cache_size, auto_reload,
                 bytecode_cache,trim_floats,sandboxed_access,dict_attrs,enable_async)
    
    def is_safe_attribute(self, obj, attr, value):
        if not super(BlendedEnvironment, self).is_safe_attribute(obj, attr, value):
            return False
        return not jinja2.sandbox.modifies_known_mutable(obj, attr)

class BlendedCodeGenerator(jinja2.compiler.CodeGenerator):
    """
    This subclass does a couple of things: it helps standardize all numbers in Jinja
    as floats, but with the feature that trailing zeroes are not printed; it also adds
    functionality to the include tag.

    What is added to include is the ability to pass specific arguments into the tag.

    .. sourcecode:: jinja

        {% include "included_file.html" with { "arg1": strval, "arg2": numval } %}
    """


    def visit_Const(self, node, frame):
        """
        """
        # val = node.value
        val = node.as_const(frame.eval_ctx)
        if isinstance(val, Number):
            self.write('environment._trimfloat(' + str(val) + ')')
        else:
            self.write(repr(val))
    
    
    def visit_Filter(self, node, frame):
        """
        """
        self.write('environment._trimfloat(')
        super(BlendedCodeGenerator, self).visit_Filter(node, frame)
        self.write(')')


    def visit_Include(self, node, frame):
        """
        Handles includes. Overrides base functionality to add new Include node functionality
        """
        
        if node.ignore_missing:
            self.writeline('try:')
            self.indent()

        func_name = 'get_or_select_template'
        if isinstance(node.template, nodes.Const):
            if isinstance(node.template.value, string_types):
                func_name = 'get_template'
            elif isinstance(node.template.value, (tuple, list)):
                func_name = 'select_template'
        elif isinstance(node.template, (nodes.Tuple, nodes.List)):
            func_name = 'select_template'

        self.writeline('template = environment.%s(' % func_name, node)
        self.visit(node.template, frame)
        self.write(', %r)' % self.name)
        if node.ignore_missing:
            self.outdent()
            self.writeline('except TemplateNotFound:')
            self.indent()
            self.writeline('pass')
            self.outdent()
            self.writeline('else:')
            self.indent()
        
        skip_event_yield = False
        if node.with_expression:
            # breakpoint()
            self.writeline('args = dict(')
            self.visit(node.with_expression, frame)
            self.write(')')
            
            if node.with_context:
                self.writeline('vars = dict(context.parent)')
                self.writeline('ctxt = template.new_context(vars, True, locals(), args)')
            else:
                self.writeline('ctxt = template.new_context(args, True)')
            self.writeline('for event in template.root_render_func(ctxt):')
        else:
            
            if node.with_context:
                self.writeline(
                f"{self.choose_async()}for event in template.root_render_func("
                "template.new_context(context.get_all(), True,"
                f" {self.dump_local_context(frame)})):"
            )
            
            elif self.environment.is_async:
                self.writeline(
                    "for event in (await template._get_default_module_async())"
                    "._body_stream:"
                )
            else:
                self.writeline("yield from template._get_default_module()._body_stream")
                skip_event_yield = True
                
        if not skip_event_yield:
            self.indent()
            self.simple_write("event", frame)
            self.outdent()

        if node.ignore_missing:
            self.outdent()
    

# NativeEnvironment for Blended
'''
The default Environment renders templates to strings. 
With NativeEnvironment, rendering a template produces a native Python type.
====
env = NativeEnvironment()
env_t = env.from_string('{{ x + y }}')
result = env_t.render(x=4, y=2)
print(result)     ---> 6
print(type(result))   ---> int      [ if we don't use NativeEnvironment then type is 'str' ]

'''
from jinja2.nativetypes import native_concat, NativeCodeGenerator, NativeTemplate, NativeEnvironment
from jinja2.compiler import has_safe_repr
import typing as t

class Blended_NativeCodeGenerator(BlendedCodeGenerator):
    @staticmethod
    def _default_finalize(value):
        return value

    def _output_const_repr(self, group) -> str:
        return repr("".join([str(v) for v in group]))

    def _output_child_to_const(
        self, node: nodes.Expr, frame, finalize: BlendedCodeGenerator._FinalizeInfo
    ):
        const = node.as_const(frame.eval_ctx)

        if not has_safe_repr(const):
            raise nodes.Impossible()

        if isinstance(node, nodes.TemplateData):
            return const

        return finalize.const(const)  # type: ignore

    def _output_child_pre(
        self, node: nodes.Expr, frame, finalize: BlendedCodeGenerator._FinalizeInfo
    ) -> None:
        if finalize.src is not None:
            self.write(finalize.src)

    def _output_child_post(
        self, node: nodes.Expr, frame, finalize: BlendedCodeGenerator._FinalizeInfo
    ) -> None:
        if finalize.src is not None:
            self.write(")")

class Blended_NativeEnvironment(BlendedEnvironment):
    
    code_generator_class = Blended_NativeCodeGenerator
    concat = staticmethod(native_concat)
    


class Blended_NativeTemplate(BlendedTemplate):
    environment_class = Blended_NativeEnvironment
    def render(self, *args, **kwargs):
        """Render the template to produce a native Python type. If the
        result is a single node, its value is returned. Otherwise, the
        nodes are concatenated as strings. If the result can be parsed
        with :func:`ast.literal_eval`, the parsed value is returned.
        Otherwise, the string is returned.
        """
        ctx = self.new_context(dict(*args, **kwargs))

        try:
            # temp = self.environment_class.concat(self.root_render_func(ctx))
            # if temp not in [False, True]:
            return self.environment_class.concat(  # type: ignore
                self.root_render_func(ctx)  # type: ignore
            ) 
        except Exception:
            return self.environment.handle_exception()

Blended_NativeEnvironment.template_class = Blended_NativeTemplate


