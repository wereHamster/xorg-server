#!/usr/bin/env python

from xml.etree.cElementTree import *
from os.path import basename

import getopt
import getopt
import sys
import re

args = sys.argv[1:]

from mako.template import Template

data = { 'version':'0.1', 'simple':[], 'enum':[], 'struct':[],
         'union':[], 'request':[], 'event':[], 'error':[] }

def c_open(self):
    pass

def c_close(self):
    template = Template(filename='proto/template.c.py')
    f = open('proto/%s.c' % module.namespace.header, 'w')
    f.write(template.render(**data))
    
    template = Template(filename='proto/template.h.py')
    f = open('proto/%s.h' % module.namespace.header, 'w')
    f.write(template.render(**data))

def c_simple(self, name):
    data['simple'].append((self, name))

def c_enum(self, name):
    data['enum'].append((self, name))

def c_struct(self, name):
    data['struct'].append(self)

def c_union(self, name):
    data['union'].append(self)

def c_request(self, name):
    data['request'].append(self)

def c_event(self, name):
    data['event'].append(self)

def c_error(self, name):
    data['error'].append(self)


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
from xcbgen.state import Module

module = Module(args[0], output)
data['module'] = module

module.register()
module.resolve()
module.generate()
