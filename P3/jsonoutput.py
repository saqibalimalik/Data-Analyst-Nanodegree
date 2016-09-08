#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Terrace", "Way", "Walk", "Pike", "Park", "Circle",
            "Broadway", "Alley", "Dale", "Champions", "Esplanade", "Green", "Limestone","North","East","South","West"]

mapping = {
    "St": "Street",
    "Ave": "Avenue",
    "Blvd": "Boulevard",
    "Dr": "Drive",
    "DR": "Drive",
    "Ct": "Court",
    "Pl": "Place",
    "Sq": "Square",
    "Ln": "Lane",
    "Rd.": "Road",
    "Rd": "Road",
    "Trl": "Trail",
    "Pkwy": "Parkway",
    "Ter": "Terrace",
    "N": "North",
    "E": "East",
    "S": "South",
    "W": "West",
}

cardinals = {
    
}

def update_name(name):
    """Update name of streets with issues"""
    name=name.title() # Convert to Camel case
    name = name.strip(' .')#remvoe trailing dot
    street=street_type_re.search(name).group()
    if street not in expected:
        if street in mapping:
            name=name.replace(street,mapping[street])

    return name

def shape_element(el):
    node = {}
    if el.tag == "node" or el.tag == "way" :
        node['id'] = el.attrib['id']
        node['type'] = el.tag
        try:
            node['visible'] = el.attrib['visible']
        except KeyError:
            pass
        node['created'] = {}
        node['created']['version'] = el.attrib['version']
        node['created']['changeset'] = el.attrib['changeset']
        node['created']['timestamp'] = el.attrib['timestamp']
        node['created']['user'] = el.attrib['user']
        node['created']['uid'] = el.attrib['uid']
        try:
            node['pos'] = []
            node['pos'].append(float(el.attrib['lat']))
            node['pos'].append(float(el.attrib['lon']))
        except KeyError:
            del node['pos']
        node['address'] = {}
        node['node_refs'] = []
                
        for child in el:
            if 'k' in child.attrib and child.attrib['k'] == 'addr:street':
                if child.attrib['v'] == '9700 Medlock Bridge Rd.,Suite 186, Johns Creek, GA, 30097':
                    node['address']['street']=update_name('9700 Medlock Bridge Rd.')
                    node['address']['postcode'] ='30097'
                    node['address']['housenumber'] ='186'
                    node['address']['city']='Johns Creek'
                    node['address']['state'] ='GA'
                node['address']['street'] = update_name(child.attrib['v'])

            elif 'k' in child.attrib and child.attrib['k'] == 'addr:city':
                node['address']['city'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] == 'addr:state':
                node['address']['state'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] == 'addr:postcode':
                node['address']['postcode'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] == 'addr:housenumber':
                node['address']['housenumber'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] in ['addr:name', 'name']:
                node['name'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] in ['addr:phone', 'phone']:
                node['phone'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] == 'gnis:county_name':
                node['address']['county'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] in ['addr:amenity', 'amenity']:
                node['amenity'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] in ['addr:cuisine', 'cuisine']:
                node['cuisine'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] == 'maxspeed':
                node['maxspeed'] = child.attrib['v']
            elif 'k' in child.attrib and child.attrib['k'] == 'smoothness':
                node['smoothness'] = child.attrib['v']
            elif 'ref' in child.attrib and child.tag == 'nd':
                node['node_refs'].append(child.attrib['ref'])
            
        if node['address'] == {}:
            del node['address']
        if node['node_refs'] == []:
            del node['node_refs']
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == "__main__":
    process_map('file.osm',True)