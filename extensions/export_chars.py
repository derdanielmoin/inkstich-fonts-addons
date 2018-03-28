#!/usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
import json
import os

from simplestyle import *

#def getChildNum(node):
#    parent = node.getparent()
#    return parent.index(node)

def getFontSize():
    pass

class ExportCharsEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-f', '--fn', action = 'store',
          type = 'string', dest = 'fn', default = '~/.config/inkscape/replace-chars.json',
          help = 'Filename that contains chars-path to replace.')
        
    def effect(self):
        fn = os.path.expanduser(self.options.fn)
        
        #open file and read in dict
        
        replaceObjs = {}
        
        if (os.path.isfile(fn)):
            with open(fn, 'r') as infile:
                replaceObjs = json.load(infile)

        #Iterate through all the selected objects in Inkscape
        
        selected_sorted_list_path = []
        
        for id, node in self.selected.iteritems():
            #sys.stderr.write(node.tag + "\n\n")
            if (node.tag == inkex.addNS('g','svg')):
                #sys.stderr.write("group found: " + id + "\n")
                lst = node.getchildren()
                #sys.stderr.write(str(lst[0].tag) + "\n\n" + inkex.addNS('path','svg'))
                selected_sorted_list_path = []
                for node0 in lst:
                    if (node0.tag == inkex.addNS('path','svg')):
                        selected_sorted_list_path += [node0]
            
                if (len(selected_sorted_list_path) == 0):
                    return
        
                first = selected_sorted_list_path[0]
                style = parseStyle(first.get('style'))
                fontsize = int(round(self.uutounit(float(style['font-size'][0:-3]),'pt')))
                fontname = style['font-family']
                
                prekey = fontname + "_" + str(fontsize) + "_"
                
                #sys.stderr.write(prekey)
                
                key = prekey + node.get('id')
                
                charData = first.get('d')
                
                acltLst = []
                
                for i in range(1,len(selected_sorted_list_path)):
                    node1 = selected_sorted_list_path[i]
                    attrib_dict = {}
                    for name,value in node1.attrib.iteritems():
                        if (name[0:10] == "embroider_"):
                            attrib_dict[name] = value
                    acltLst += [(node1.get('d'),attrib_dict)]

                replaceObjs[key] = (charData,acltLst)
                
                with open(fn, 'w') as outfile:
                    json.dump(replaceObjs, outfile)
    
# Create effect instance and apply it.
effect = ExportCharsEffect()
effect.affect()
