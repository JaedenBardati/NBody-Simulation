"""
This local module handles xml parsing.
"""

import os 

import xml.etree.cElementTree as ET


def getXMLRoot(filepath):
    return ET.parse(filepath).getroot()


CONSTANTS = getXMLRoot(os.path.join('resources', 'astronomical_constants.xml'))
DATA = getXMLRoot(os.path.join('resources', 'astronomical_data.xml'))


def getConstantFromSymbol(symbol):
    for constant in CONSTANTS.findall('c'):
        if constant.find('symbol').text == symbol:
            return float(constant.find('value').text) * 10 ** int(constant.find('value').get('order'))

def getConstantFromName(name):
    for constant in CONSTANTS.findall('c'):
        if constant.find('name').text == name:
            return float(constant.find('value').text) * 10 ** int(constant.find('value').get('order'))


def getData(name):
    d = dict()

    element = DATA.find(name)

    d['type'] = element.find('type').text

    for category in ['physical_data', 'rotation_data', 'orbital_data']:
        subelement = element.find(category)
        
        if subelement == None:    ## If one of the tags is missing
            continue

        for child in subelement:
            text = child.text

            try:                        ## If it is a number
                text = float(text)
                o = child.get('order')
                if o == None:
                    o = 0
                d[child.tag] = float(text) * 10 ** int(o)
            except ValueError:                     ## If it is text
                d[child.tag] = text
    
    return d

    


if __name__ == '__main__':
    """ TESTS """

    print("Testing module . . .\n")
    
    Croot = getXMLRoot('data/astronomical_constants.xml')
    for constant in Croot.findall('c'):
        print("%s (%s) :  %s * 10^%s  %s" % (constant.find('name').text, constant.find('symbol').text, constant.find('value').text, constant.find('value').get('order'), constant.find('unit').text))
    print()
    
    Droot = getXMLRoot('data/astronomical_data.xml')
    for body in Droot:
        print(body.tag + ": ")
        for child in body.find('physical_data'):
            if int(child.get('order')):
                print("   %s :  %s * 10^%s  %s" % (child.tag[0].upper() + child.tag[1:], child.text, child.get('order'), child.get('unit')))
            else:
                print("   %s :  %s  %s" % (child.tag[0].upper() + child.tag[1:], child.text, child.get('unit')))

    print()

