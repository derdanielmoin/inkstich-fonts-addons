#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
import json
import os
# The simplestyle module provides functions for style parsing.
from simplestyle import *

def getChildNum(node):
    parent = node.getparent()
    return parent.index(node)

def draw_svg_path(name,parent,color,d,attribs_dict):
    style = {
        'stroke':color,
        'stroke-width':0.2,
        'fill':"none"}
    attribs = dict(attribs_dict)
    attribs['style'] = formatStyle(style)
    attribs[inkex.addNS('label','inkscape')] = name
    attribs['d'] = d
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'),attribs)

replace_dict = {
    "M":"M ",
    "L":"L ",
    "H":"H ",
    "V":"V ",
    "C":"C ",
    "S":"S ",
    "Q":"Q ",
    "T":"T ",
    "A":"A ",
    "Z":"Z ",
    "m":"m ",
    "l":"l ",
    "h":"h ",
    "v":"v ",
    "c":"c ",
    "s":"s ",
    "q":"q ",
    "t":"t ",
    "a":"a ",
    "z":"z ",
    ",":" , "}

def pathDataIndent(dataold):
    data = str(dataold)
    for key, val in replace_dict.iteritems():
        data = data.replace(key,val)
    data = data.replace("  "," ")
    return data

def checkFormat(datastr):
    data = datastr.split(' ')
    if (len(data) < 5): return False
    if (data[0] != 'm'): return False
    if (data[2] != ","): return False
    try:
        float(data[1])
    except:
        return False
    try:
        float(data[3])
    except:
        return False
    return True

def equal(d1,d2):
    delta = 1e-5
    pathData1 = d1.split(' ',4)[4].split(' ')
    pathData2 = d2.split(' ',4)[4].split(' ')

    if (len(pathData1) != len(pathData2)):
        return False
    
    for i in range(len(pathData1)):
        token1 = pathData1[i]
        token2 = pathData2[i]
        
        if (len(token1) == 0 or len(token2) == 0):
            if (token1 != token2):
                return False
        
        elif (token1.isalpha() or token1 == ","):
            if (token1 != token2):
                return False
            
        else:
            if (token2.isalpha() or token2 == ","):
                return False
            
            #sys.stderr.write(token1 + "\n\n")
            #sys.stderr.write(token2 + "\n\n")
            
            num1 = float(token1)
            num2 = float(token2)
            
            if (abs(num1 - num2) > delta):
                return False
    return True

def draw_rep(oldname,parent,color,d1,d2,lst):
    d1s = d1.split(' ')
    d2s = d2.split(' ')
    for i in range(len(lst)):
        name = oldname + "_" + str(i)
        elem = lst[i][0]
        attribs_dict = lst[i][1]
        elems = elem.split(' ',4)
        val1x = float(d1s[1])
        val1y = float(d1s[3])
        val2x = float(d2s[1])
        val2y = float(d2s[3])
        valix = float(elems[1])
        valiy = float(elems[3])
        
        newx = val1x + valix - val2x
        newy = val1y + valiy - val2y
        
        d = "m" + " " + str(newx) + " , " + str(newy) + " " + elems[4]
        
        #sys.stderr.write(d + "\n\n")
        
        draw_svg_path(name,parent,color,d,attribs_dict)

class ReplaceCharsEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-f', '--fn', action = 'store',
          type = 'string', dest = 'fn', default = '~/.config/inkscape/replace-chars.json',
          help = 'Filename that contains chars-path to replace.')

    def effect(self):
        fn = os.path.expanduser(self.options.fn)
        
        #open file and read in dict
        
        replaceObjs = {}
        
        if (not os.path.isfile(fn)):
            sys.stderr.write("input file not found!")
            return
            
        with open(fn, 'r') as infile:
            replaceObjs = json.load(infile)

        selected_sorted_list_path = []
            
        #Iterate through all the selected objects in Inkscape
        for id, node in self.selected.iteritems():
            if (node.tag == inkex.addNS('path','svg')):
                selected_sorted_list_path += [node]
            
        if (len(selected_sorted_list_path) == 0):
            return
        
        selected_sorted_list_path.sort(key = getChildNum)
        
        for node in selected_sorted_list_path:
            d1 = node.get('d')
            d1space = pathDataIndent(d1)
            #sys.stderr.write(d1space)
            if (not checkFormat(d1space)):
                sys.stderr.write("d1 format not ok!")
                continue

            parent = node.getparent()
            style = parseStyle(node.get('style'))
            color = style['fill']
            
            for charname, pair in replaceObjs.iteritems():
                d2 = pair[0]
                lst = pair[1]
                d2space = pathDataIndent(d2)
                if (not checkFormat(d1space)):
                    sys.stderr.write("d2 format not ok!")
                    continue
                
                eq = equal(d1space,d2space)
                #if (not eq):
                #    sys.stderr.write(d1space + "\n\n" + d2space)
                
                if (eq):
                    lstspace = []
                    for pair2 in lst:
                        di = pair2[0]
                        attribs_dict = pair2[1]
                        #sys.stderr.write(di + " ---(DI)---\n\n")
                        dispace = pathDataIndent(di)
                        if (not checkFormat(dispace)):
                            sys.stderr.write("di format not ok!")
                            continue
                        lstspace += [(dispace,attribs_dict)]
                    draw_rep(node.get('id'),parent,color,d1space,d2space,lstspace)

# Create effect instance and apply it.
effect = ReplaceCharsEffect()
effect.affect()

