from django.template import TemplateSyntaxError

__all__ =  ['BaseError', 'TagNameError', 'ArgumentRequiredError', 'InvalidArgument', 
            'InvalidFlag', 'BreakpointExpected', 'TooManyArguments', 'TooFewArguments', 'TooFewArgumentsFor', 
            'KeywordInUse', 'FormatError', 'UnexpectedElement', 'ArgumentRequiredErrorGeneral']


class BaseError(TemplateSyntaxError):
    template = '%(message)s'

    def __init__(self, message):
        self.message = message
    
    def __str__(self): # pragma: no cover
        return self.template % self.__dict__


class TagNameError(BaseError):
    template = "The name of the tag encounterd by the parser ('%(bad_name)s') is not the name that is expected ('%(name)s')."

    def __init__(self, bad_name, name):
        self.bad_name = bad_name
        self.name = name 


class UnexpectedElement(BaseError):
    template = "The %(type)s type tag '%(tag_name)s' is unexpected in this position."

    def __init__(self, type, tag_name):
        self.type = type
        self.tag_name = tag_name
    

class ArgumentRequiredError(BaseError):

    template = "The tag '%(tagname)s' requires an argument of type '%(argtype)s' named '%(name)s'."

    def __init__(self, argument, tagname, msg):
        self.argtype = argument.__class__.__name__
        self.tagname = tagname 
        self.name = argument.name
        self.msg = msg

class ArgumentRequiredErrorGeneral(BaseError):           # added for general argument error demand
    
    template = "'%(msg)s'"
    def __init__(self, argument, tagname, msg):
        self.argtype = argument.__class__.__name__
        self.tagname = tagname 
        self.name = argument.name
        self.msg = msg

class InvalidArgument(BaseError):
    template = ("The tag '%(tagname)s' must not have the excluded value '%(excluded)s' "
                " at the '%(argument)s' position.")
    
    def __init__(self, argument, excluded, tagname):
        self.tagname = tagname
        self.excluded = excluded
        self.argument = argument.__repr__()
        
        
class InvalidFlag(BaseError):
    template = ("The flag '%(argname)s' for the tag '%(tagname)s' must be one "
                "of %(allowed_values)s, but got '%(actual_value)s'")
    
    def __init__(self, argname, actual_value, allowed_values, tagname):
        self.argname = argname
        self.tagname = tagname
        self.actual_value = actual_value
        self.allowed_values = allowed_values


class BreakpointExpected(BaseError):
    
    # template = ("Expected one of the following breakpoints: %(breakpoints)s in "
    #             "%(tagname)s, got '%(got)s' instead.")
  
    template = ("'%(tagname)s' tag received an invalid argument: %(msg)s")

    def __init__(self, tagname, breakpoints, got, msg):
        self.breakpoints = ', '.join(["'%s'" % bp for bp in breakpoints])
        self.tagname = tagname
        self.got = got
        self.msg = msg


class TooManyArguments(BaseError):
    template = "The tag '%(tagname)s' received too many arguments: %(extra)s"
    
    def __init__(self, tagname, extra):
        self.tagname = tagname
        self.extra = ', '.join(["'%s'" % e for e in extra])
        

class TooFewArguments(BaseError):
    template = ("The tag '%(tagname)s' at argument '%(argument)s' received "
                "too few tokens.")

    def __init__(self, argument, tagname):
        self.argument = argument
        self.tagname = tagname

# added for "for tag" if there is less argumnets
class TooFewArgumentsFor(BaseError):
    # template = ("The tag '%(tagname)s' at argument '%(argument)s' received "
    #             "too few tokens.")
    template = ("'%(tagname)s' statements should have at least four words: %(msg)s")

    def __init__(self, argument, tagname, msg):
        self.argument = argument
        self.tagname = tagname
        self.msg = msg

class KeywordInUse(BaseError):
    template = ("The name '%(name)s' specified for '%(type)s' is " 
                "already specified elsewhere in the syntax.")

    def __init__(self, name, type):
        self.name = name
        self.type = type


class FormatError(BaseError):
    # template = ("'%(argname)s' should be in the form '%(format)s'")
    template = (
            "'%(argname)s' statements should use the format"
            " 'for x in y': %(format)s"
        )

    def __init__(self, argname, format):
        self.argname = argname
        self.format = format


class UnexpectedTokenError(BaseError):
    template = ("Expected token %(expr)r, got %(current)r.")

    def __init__(self, expr, current):
        self.expr = expr
        self.current = current


class TemplateSyntaxWarning(Warning):
    """
    Used for variable cleaning TemplateSyntaxErrors when in non-debug-mode.
    """

