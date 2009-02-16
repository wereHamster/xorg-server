#!/usr/bin/env python
from xml.etree.cElementTree import *
from os.path import basename
import getopt
import sys
import re

# Jump to the bottom of this file for the main routine

# Some hacks to make the API more readable, and to keep backwards compability
_cname_re = re.compile('([A-Z0-9][a-z]+|[A-Z0-9]+(?![a-z])|[a-z]+)')
_cname_special_cases = {'DECnet':'decnet'}

_extension_special_cases = ['XPrint', 'XCMisc', 'BigRequests']

_cplusplus_annoyances = {'class' : '_class',
                         'new'   : '_new',
                         'delete': '_delete'}

_cardinal_types = ['CARD8', 'uint8_t',
                   'CARD16','uint16_t',
                   'CARD32','uint32_t',
                   'INT8', 'int8_t',
                   'INT16', 'int16_t',
                   'INT32', 'int32_t',
                   'BYTE',
                   'BOOL',
                   'char',
                   'void',
                   'float',
                   'double']
_clines = []
_ns = None

def _c(fmt, *args):
    '''
    Writes the given line to the source file.
    '''
    _clines.append(fmt % args)
    
def _n_item(str):
    '''
    Does C-name conversion on a single string fragment.
    Uses a regexp with some hard-coded special cases.
    '''
    if str in _cname_special_cases:
        return _cname_special_cases[str]
    else:
        split = _cname_re.finditer(str)
        name_parts = [match.group(0) for match in split]
        return '_'.join(name_parts)
    
def _cpp(str):
    '''
    Checks for certain C++ reserved words and fixes them.
    '''
    if str in _cplusplus_annoyances:
        return _cplusplus_annoyances[str]
    else:
        return str

def _ext(str):
    '''
    Does C-name conversion on an extension name.
    Has some additional special cases on top of _n_item.
    '''
    if str in _extension_special_cases:
        return _n_item(str).lower()
    else:
        return str.lower()
    
def _n(list):
    '''
    Does C-name conversion on a tuple of strings.
    Different behavior depending on length of tuple, extension/not extension, etc.
    Basically C-name converts the individual pieces, then joins with underscores.
    '''
    if len(list) == 1:
        parts = list
    elif len(list) == 2:
        parts = [list[0], _n_item(list[1])]
    elif _ns.is_ext:
        parts = [list[0], _ext(list[1])] + [_n_item(i) for i in list[2:]]
    else:
        parts = [list[0]] + [_n_item(i) for i in list[1:]]
    return '_'.join(parts).lower()

def _t(list):
    '''
    Does C-name conversion on a tuple of strings representing a type.
    Same as _n but adds a "_t" on the end.
    '''
    if len(list) < 4:
        parts = list
    else:
        return '__%s_%s' % ( list[3], list[2] )
    return '_'.join(parts).lower()
        

def c_open(self):
    '''
    Exported function that handles module open.
    Opens the files and writes out the auto-generated comment, header file includes, etc.
    '''
    global _ns
    _ns = self.namespace
    _ns.c_ext_global_name = _n(_ns.prefix + ('id',))

def c_close(self):
    '''
    Exported function that handles module close.
    Writes out all the stored content lines, then closes the files.
    '''

    # Write source file
    cfile = open('%s.c' % _ns.header, 'w')
    for line in _clines:
        cfile.write(line + '\n')
    cfile.write('\n')
    cfile.close()

def c_enum(self, name):
    '''
    Exported function that handles enum declarations.
    '''

    count = len(self.values)

    for (enam, eval) in self.values:
        count = count - 1
        equals = ' = ' if eval != '' else ''
        comma = ',' if count > 0 else ''
        _c(enam)

def _c_type_setup(self, name, postfix):
    '''
    Sets up all the C-related state by adding additional data fields to
    all Field and Type objects.  Here is where we figure out most of our
    variable and function names.

    Recurses into child fields and list member types.
    '''
    # Do all the various names in advance
    self.c_type = _t(name + postfix)
    self.c_wiretype = 'char' if self.c_type == 'void' else self.c_type

    self.c_iterator_type = _t(name + ('iterator',))
    self.c_next_name = _n(name + ('next',))
    self.c_end_name = _n(name + ('end',))

    self.c_request_name = _n(name)
    self.c_checked_name = _n(name + ('checked',))
    self.c_unchecked_name = _n(name + ('unchecked',))
    self.c_reply_name = _n(name + ('reply',))
    self.c_reply_type = _t(name + ('reply',))
    self.c_cookie_type = _t(name + ('cookie',))

    if self.is_container:

        self.c_container = 'union' if self.is_union else 'struct'
        prev_varsized_field = None
        prev_varsized_offset = 0
        first_field_after_varsized = None

        for field in self.fields:
            _c_type_setup(field.type, field.field_type, ())
            if field.type.is_list:
                _c_type_setup(field.type.member, field.field_type, ())

            field.c_field_type = _t(field.field_type)
            field.c_field_const_type = ('' if field.type.nmemb == 1 else 'const ') + field.c_field_type
            field.c_field_name = _cpp(field.field_name)
            field.c_subscript = '[%d]' % field.type.nmemb if (field.type.nmemb > 1) else ''
            field.c_pointer = ' ' if field.type.nmemb == 1 else '*'

            field.c_iterator_type = _t(field.field_type + ('iterator',))      # xcb_fieldtype_iterator_t
            field.c_iterator_name = _n(name + (field.field_name, 'iterator')) # xcb_container_field_iterator
            field.c_accessor_name = _n(name + (field.field_name,))            # xcb_container_field
            field.c_length_name = _n(name + (field.field_name, 'length'))     # xcb_container_field_length
            field.c_end_name = _n(name + (field.field_name, 'end'))           # xcb_container_field_end

            field.prev_varsized_field = prev_varsized_field
            field.prev_varsized_offset = prev_varsized_offset

            if prev_varsized_offset == 0:
                first_field_after_varsized = field
            field.first_field_after_varsized = first_field_after_varsized

            if field.type.fixed_size():
                prev_varsized_offset += field.type.size
            else:
                self.last_varsized_field = field
                prev_varsized_field = field
                prev_varsized_offset = 0

def c_simple(self, name):
    '''
    Exported function that handles cardinal type declarations.
    These are types which are typedef'd to one of the CARDx's, char, float, etc.
    '''
    _c_type_setup(self, name, ())

def _c_complex(self):
    '''
    Helper function for handling all structure types.
    Called for all structs, requests, replies, events, errors.
    '''
    _c('')
    _c('%s %s {', self.c_container, self.c_type)

    struct_fields = []
    maxtypelen = 0

    varfield = None
    for field in self.fields:
        if not field.type.fixed_size():
            varfield = field.c_field_name
            continue
        if varfield != None and not field.type.is_pad and field.wire:
            errmsg = '%s: warning: variable field %s followed by fixed field %s\n' % (self.c_type, varfield, field.c_field_name)
            sys.stderr.write(errmsg)
            # sys.exit(1)
        if field.wire:
            struct_fields.append(field)
        
    for field in struct_fields:
        if len(field.c_field_type) > maxtypelen:
            maxtypelen = len(field.c_field_type)

    for field in struct_fields:
        spacing = ' ' * (maxtypelen - len(field.c_field_type))
        _c('    %s%s %s%s;', field.c_field_type, spacing, field.c_field_name, field.c_subscript)

    _c('};')

def c_struct(self, name):
    '''
    Exported function that handles structure declarations.
    '''
    _c_type_setup(self, name, ())
    _c_complex(self)
    _c_accessors(self, name, name)
    _c_iterator(self, name)

def c_union(self, name):
    '''
    Exported function that handles union declarations.
    '''
    _c_type_setup(self, name, ())
    _c_complex(self)
    _c_iterator(self, name)

def _c_request_helper(self, name):
    '''
    Declares a request function.
    '''

    param_fields = []
    wire_fields = []
    maxtypelen = len('xcb_connection_t')

    for field in self.fields:
        if field.visible:
            # The field should appear as a call parameter
            param_fields.append(field)
        if field.wire and not field.auto:
            # We need to set the field up in the structure
            wire_fields.append(field)

    _c('')
    _c('static int')
    _c('__impl_%s(xcb_connection_t *c)' % name[2])
    _c('{')

    _c('    struct __req_%s *req = c->buffer;', name[2])
    _c('')

    for field in wire_fields:
        _c('    /* Validating %s */', field.field_name);
        _c('    if (req->%s < 0) return -1;', field.field_name)
        if field.type.fixed_size():
            if field.type.is_expr:
                _c('    xcb_out.%s = %s;', field.c_field_name, _c_accessor_get_expr(field.type.expr))

            elif field.type.is_pad:
                if field.type.nmemb == 1:
                    _c('    xcb_out.%s = 0;', field.c_field_name)
                else:
                    _c('    memset(xcb_out.%s, 0, %d);', field.c_field_name, field.type.nmemb)
            else:
                if field.type.nmemb == 1:
                    _c('    xcb_out.%s = %s;', field.c_field_name, field.c_field_name)
                else:
                    _c('    memcpy(xcb_out.%s, %s, %d);', field.c_field_name, field.c_field_name, field.type.nmemb)

    _c('    ')
    _c('    xcb_parts[2].iov_base = (char *) &xcb_out;')
    _c('    xcb_parts[2].iov_len = sizeof(xcb_out);')
    _c('    xcb_parts[3].iov_base = 0;')
    _c('    xcb_parts[3].iov_len = -xcb_parts[2].iov_len & 3;')

    if self.reply:
        _c('    struct __rep_%s rep;', name[2])
        _c('')

        for field in self.reply.fields:
            if not field.type.is_pad and not field.auto:
                _c('    rep.%s = 0;', field.field_name)

        _c('')

    count = 4
    for field in param_fields:
        if not field.type.fixed_size():
            _c('    xcb_parts[%d].iov_base = (char *) %s;', count, field.c_field_name)
            if field.type.is_list:
                _c('    xcb_parts[%d].iov_len = %s * sizeof(%s);', count, '', field.type.member.c_wiretype)
            else:
                _c('    xcb_parts[%d].iov_len = %s * sizeof(%s);', count, 'Uh oh', field.type.c_wiretype)
            _c('    xcb_parts[%d].iov_base = 0;', count + 1)
            _c('    xcb_parts[%d].iov_len = -xcb_parts[%d].iov_len & 3;', count + 1, count)
            count = count + 2

    _c('    xcb_ret.sequence = xcb_send_reply(c, reply, %d);', 4)
    _c('    return xcb_ret;')
    _c('}')

def _c_opcode(name, opcode):
    '''
    Declares the opcode define for requests, events, and errors.
    '''
    _c('')
    _c('/** Opcode for %s. */', _n(name))
    _c('#define %s %s', _n(name).upper(), opcode)
    
def c_request(self, name):
    '''
    Exported function that handles request declarations.
    '''
    _c_type_setup(self, name, ('req',))

    # Opcode define
    _c_opcode(name, self.opcode)

    # Request structure declaration
    _c_complex(self)

    if self.reply:
        _c_type_setup(self.reply, name, ('rep',))
        # Reply structure definition
        _c_complex(self.reply)
        # Request prototypes
        _c_request_helper(self, name)
    else:
        # Request prototypes
        _c_request_helper(self, name)

def c_event(self, name):
    '''
    Exported function that handles event declarations.
    '''
    _c_type_setup(self, name, ('evn',))

    # Opcode define
    _c_opcode(name, self.opcodes[name])

    if self.name == name:
        # Structure definition
        _c_complex(self)
    else:
        # Typedef
        _h('')
        _h('typedef %s %s;', _t(self.name + ('evn',)), _t(name + ('evn',)))

def c_error(self, name):
    '''
    Exported function that handles error declarations.
    '''
    _c_type_setup(self, name, ('err',))

    # Opcode define
    _c_opcode(name, self.opcodes[name])

    if self.name == name:
        # Structure definition
        _c_complex(self)
    else:
        # Typedef
        _h('')
        _h('typedef %s %s;', _t(self.name + ('err',)), _t(name + ('err',)))


# Main routine starts here

# Must create an "output" dictionary before any xcbgen imports.
output = {'open'    : c_open,
          'close'   : c_close,
          'simple'  : c_simple,
          'enum'    : c_enum,
          'struct'  : c_struct,
          'union'   : c_union,
          'request' : c_request,
          'event'   : c_event,
          'error'   : c_error
          }

# Boilerplate below this point

# Check for the argument that specifies path to the xcbgen python package.
try:
    opts, args = getopt.getopt(sys.argv[1:], 'p:')
except getopt.GetoptError, err:
    print str(err)
    print 'Usage: c_client.py [-p path] file.xml'
    sys.exit(1)

for (opt, arg) in opts:
    if opt == '-p':
        sys.path.append(arg)

# Import the module class
try:
    from xcbgen.state import Module
except ImportError:
    print ''
    print 'Failed to load the xcbgen Python package!'
    print 'Make sure that xcb/proto installed it on your Python path.'
    print 'If not, you will need to create a .pth file or define $PYTHONPATH'
    print 'to extend the path.'
    print 'Refer to the README file in xcb/proto for more info.'
    print ''
    raise

# Parse the xml header
module = Module(args[0], output)

# Build type-registry and resolve type dependencies
module.register()
module.resolve()

# Output the code
module.generate()
