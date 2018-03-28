#!/usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
import json
import os

label_name = inkex.addNS('label','inkscape')

class AddPrefixEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-p', '--prefix', action = 'store',
          type = 'string', dest = 'prefix', default = '',
          help = 'Prefix to add to each object.')
        
    def effect(self):
        prefix = self.options.prefix
        
        for id, node in self.selected.iteritems():
            newid = id
            #sys.stderr.write(str(node.attrib))
            if (label_name in node.attrib):
                #sys.stderr.write("label found!")
                newid = node.get(label_name)
                node.attrib.pop(label_name)
            node.set('id',prefix + newid)
    
# Create effect instance and apply it.
effect = AddPrefixEffect()
effect.affect()
