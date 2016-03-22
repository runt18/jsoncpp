# Copyright 2007 Baptiste Lepilleur
# Distributed under MIT license, or public domain if desired and
# recognized in your jurisdiction.
# See file LICENSE for detail or copy at http://jsoncpp.sourceforge.net/LICENSE

"""Simple implementation of a json test runner to run the test against
json-py."""

from __future__ import print_function
import sys
import os.path
import json
import types

if len(sys.argv) != 2:
    print("Usage: %s input-json-file", sys.argv[0])
    sys.exit(3)
    
input_path = sys.argv[1]
base_path = os.path.splitext(input_path)[0]
actual_path = base_path + '.actual'
rewrite_path = base_path + '.rewrite'
rewrite_actual_path = base_path + '.actual-rewrite'

def valueTreeToString(fout, value, path = '.'):
    ty = type(value) 
    if ty  is types.DictType:
        fout.write('{0!s}={{}}\n'.format(path))
        suffix = path[-1] != '.' and '.' or ''
        names = value.keys()
        names.sort()
        for name in names:
            valueTreeToString(fout, value[name], path + suffix + name)
    elif ty is types.ListType:
        fout.write('{0!s}=[]\n'.format(path))
        for index, childValue in zip(xrange(0,len(value)), value):
            valueTreeToString(fout, childValue, path + '[{0:d}]'.format(index))
    elif ty is types.StringType:
        fout.write('{0!s}="{1!s}"\n'.format(path, value))
    elif ty is types.IntType:
        fout.write('{0!s}={1:d}\n'.format(path, value))
    elif ty is types.FloatType:
        fout.write('{0!s}={1:.16g}\n'.format(path, value))
    elif value is True:
        fout.write('{0!s}=true\n'.format(path))
    elif value is False:
        fout.write('{0!s}=false\n'.format(path))
    elif value is None:
        fout.write('{0!s}=null\n'.format(path))
    else:
        assert False and "Unexpected value type"
        
def parseAndSaveValueTree(input, actual_path):
    root = json.loads(input)
    fout = file(actual_path, 'wt')
    valueTreeToString(fout, root)
    fout.close()
    return root

def rewriteValueTree(value, rewrite_path):
    rewrite = json.dumps(value)
    #rewrite = rewrite[1:-1]  # Somehow the string is quoted ! jsonpy bug ?
    file(rewrite_path, 'wt').write(rewrite + '\n')
    return rewrite
    
input = file(input_path, 'rt').read()
root = parseAndSaveValueTree(input, actual_path)
rewrite = rewriteValueTree(json.write(root), rewrite_path)
rewrite_root = parseAndSaveValueTree(rewrite, rewrite_actual_path)

sys.exit(0)
