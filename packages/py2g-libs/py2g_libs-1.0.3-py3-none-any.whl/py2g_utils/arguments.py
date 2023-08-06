import yaml, os, re, sys, json

HELP_COMMAND = 'help'
ARGUMENT_PREFIX = '-'
ARGUMENT_PREFIX_LEN = len(ARGUMENT_PREFIX)

class ArgumentError(Exception): ...

class ArgumentType(object):
    def __init__(self, name, parser, converter, options):
        self.name = name
        self.parse = parser
        self.convert = converter
        self._options = options

    def options(self, argument_config):
        if 'options' in argument_config:
            return argument_config['options']
        options = []
        if 'default' in argument_config:
            default = argument_config['default']
            if type(default) == list:
                default = '\\"%s\\"' % json.dumps(default).replace(' ', '')
            options.append(default)
        intelli_options = self._options(argument_config)
        options.extend(intelli_options)
        return options

class ArgumentParser(object):
    def __init__(self):
        self.types = {}

    def add(self, name, parser, converter=lambda v: v, options=lambda c: []):
        if type(name) == list:
            for _name in name:
                self.add(_name, parser, converter)
            return
        assert name not in self.types
        self.types[name] = ArgumentType(name, parser, converter, options)

    def parse(self, name, value):
        assert self.types[name].parse(value)
        return self.types[name].convert(value)
    
    def options(self, type, argument_config):
        return self.types[type].options(argument_config)

_argument_parser = ArgumentParser()
_argument_parser.add(['int', 'integer'], lambda value: value.isdigit(), lambda value: int(value), lambda c: [0,1,2,3,4])
_argument_parser.add(['string', 'str'], lambda value: type(value) == str, options=lambda c: os.listdir())
_argument_parser.add('path', lambda value: type(value) == str and os.path.exists(value), options=lambda c: os.listdir())
_argument_parser.add('list', lambda value: type(value) == str, converter=lambda value: json.loads(value))
_argument_parser.add(['boolean', 'bool', 'flag'], lambda value: value is None, converter=lambda value: True, options=lambda c: [])
_argument_parser.add('float', lambda value: re.match(r'^-?\d+(?:\.\d+)?$', value) is not None, lambda value: float(value))


class ArgumentValidator(object):
    def __init__(self):
        self.validators = {}

    def add(self, type, validator):
        assert type not in self.validators
        self.validators[type] = validator

    def validate(self, val, value):
        return self.validators[val['type']](val, value)

_argument_validator = ArgumentValidator()
_argument_validator.add('regex', lambda val, value: re.match(val['expression'], value))
_argument_validator.add('max', lambda val, value: value <= float(val['max']))

class Arguments(object):
    def __init__(self):
        object.__setattr__(self, 'arguments', {})
    def set(self, name, value):
        _arguments = object.__getattribute__(self, 'arguments')
        _arguments[name] = value
    def __getattribute__(self, name):
        _arguments = object.__getattribute__(self, 'arguments')
        if name in _arguments:
            return _arguments[name]
        return object.__getattribute__(self, name)
    def keys(self):
        return object.__getattribute__(self, 'arguments').keys()

class FileArgumentParser(object):
    def __init__(self, *files, encoding='utf-8', basepath=None):
        self.arguments = {}
        for fp in files:
            if basepath is not None:
                fp = os.path.join(basepath, fp)
            with open(fp, 'r', encoding=encoding) as f:
                _keys = set()
                for argument in yaml.safe_load(f):
                    if argument['key'] in _keys:
                        raise ''
                    self.arguments[argument['key']] = argument
                    _keys.add(argument['key'])

    def _get_arguments(self):
        _arguments = {}
        last_arg = None
        for arg in sys.argv[1:]:
            if last_arg is None and arg[:ARGUMENT_PREFIX_LEN] != ARGUMENT_PREFIX:
                raise ArgumentError('{} has no argument to be assigned to'.format(arg[:ARGUMENT_PREFIX_LEN]))
            if last_arg is not None and arg[:ARGUMENT_PREFIX_LEN] != ARGUMENT_PREFIX:
                _arguments[last_arg] = arg
                last_arg = None
            elif arg[:ARGUMENT_PREFIX_LEN] == ARGUMENT_PREFIX:
                last_arg = arg[ARGUMENT_PREFIX_LEN:]
                _arguments[last_arg] = None
        return _arguments

    def print_options(self, subargument):
        if subargument is None:
            for k,v in self.arguments.items():
                print(ARGUMENT_PREFIX + "%s" % k)
        else:
            print('\n'.join(str(x) for x in _argument_parser.options(subargument['type'], subargument)))

    def parse(self):
        _arguments = self._get_arguments()
        arguments = Arguments()
        _required_arguments = {k for k,v in self.arguments.items() if 'default' not in v and v['type'] != 'flag'}
        _default_arguments = {k for k,v in self.arguments.items() if 'default' in v or v['type'] == 'flag'}

        for k,v in _arguments.items():
            if k == 'help':
                for k, arg in self.arguments.items():
                    print("Argument --%s {value}" % k)
                    print("\ttype: %s" % arg["type"])
                    if "default" in arg:
                        print("\tdefault: %s" % arg["default"])
                    if "validation" in arg:
                        print("\tvalidation:")
                        print("\t\t%s" % arg["validation"])
                exit(0)
            if k == 'options':
                if v is not None and v in self.arguments:
                    self.print_options(self.arguments[v])
                else:
                    self.print_options(None)
                exit(0)
            if k in self.arguments:
                argument = self.arguments[k]
            else:
                raise ArgumentError('Unknown argument {}'.format(k))
            v = _argument_parser.parse(argument['type'], v)
            if 'validation' in argument:
                for val in argument['validation']:
                    if not _argument_validator.validate(val, v):
                        raise ArgumentError("Validator of type {} failed for argument {}".format(val['type'], k))
            arguments.set(k,v)
            _required_arguments -= {k}
        if len(_required_arguments) > 0:
            raise ArgumentError('Arguments {} required'.format(_required_arguments))
        
        for k in _default_arguments:
            if self.arguments[k]['type'] == 'flag' and 'default' not in self.arguments[k]:
                self.arguments[k]['default'] = False

            if k not in arguments.arguments:
                arguments.set(k, self.arguments[k]['default'])
        
        return arguments

if __name__ == '__main__':
    parser = FileArgumentParser('./arguments/base.yaml')
    print(parser.parse().__dict__)