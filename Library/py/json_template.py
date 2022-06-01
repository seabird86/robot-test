#!/usr/bin/env python3

import re
import json

def unflat_json(body):
    d = {}
    for key, value in j.items():
        s = d
        tokens = re.findall(r'\w+', key)
        for count, (index, next_token) in enumerate(zip(tokens, tokens[1:] + [value]), 1):
            value = next_token if count == len(tokens) else [] if next_token.isdigit() else {}
            if isinstance(s, list):
                index = int(index)
                while index >= len(s):
                    s.append(value)
            elif index not in s:
                s[index] = value
            s = s[index]
    return d

# j = {'a': 1, 'b.0': 5,'b.1': 5}
# {
#   "item[0].subitem[0].key": "value1",
#   "item[0].subitem[1].key": "value2",
#   "item[1].subitem[0].key": "value3",
#   "item[1].subitem[1].key": "value4",
#   "item2[0].subitem[0]": "value5",
#   "item2[0].subitem[1]": "value6",
#   "item2[1][0].key1": "value7",
#   "item2[1][1].key2": "value8"
# }
# print(unflat_json(j))

def merge_json(json_body,json_template):
    print("*** {} *** {}".format(json_body, json_template))
    template = json.loads(json_template)
    body = json.loads(json_body)
    body = generate_json(body,template)
    json_body=json.dumps(body,separators=(',', ':'))
    print("{}".format(json_body))
    return json_body



def generate_json(body,template):
    if body is None:
        return body
    print("--- {} --- {}".format(body, template))
    if type(template) is dict:
        if type(body) is not dict:
            body= {}
        for key, child in template.items():
            if key in body and body[key] is None:
                continue
            if type(child) is dict:
                if (key not in body):
                    body[key]={}
                body[key]= generate_json(body[key],child)
            elif type(child) is list:
                if len(child)==0:
                    if key not in body or type(body[key]) is not list:
                        body[key] = []
                    continue
                if type(child[0]) is list:
                    print('NOT SUPORT')
                elif type(child[0]) is dict:
                    if (key in body) and type(body[key]) is list and len(body[key])==0:
                        body[key]=[]
                        continue
                    if (key not in body) or type(body[key]) is not list or type(body[key][0]) is not dict:
                        body[key] = [None]*1
                        body[key][0]= generate_json({},child[0])  # todo
                    for i in range(0, len(body[key])):
                        body[key][i]= generate_json(body[key][i],child[0])  # todo
                else:
                    if key not in body or type(body[key]) is not list:
                        body[key] = child
            elif child is not None:
                if key not in body or type(body[key]) is list or type(body[key]) is dict:
                    body[key] = child
                else:
                    body.setdefault(key,child)
    elif type(template) is list:
        if len(template) == 0:
            return body if type(body) is list else []
        if type(body) is not list:
            if type(template[0]) is list:
                body =  [None]*1
                body[0]= generate_json([],template[0])
            elif type(template[0]) is dict:
                body =  [None]*1
                body[0]= generate_json({},template[0])
            else:
                return template
        else:
            if (len(body)==0):
                return body
            if type(template[0]) is list:
                if type(body[0]) is not list:
                    body[0] = template[0]
                else:
                    for i in range(0, len(body)):
                        print("+++ {} --- {}".format(body[i], template[0]))
                        body[i]= generate_json(body[i],template[0])
            elif type(template[0]) is dict:
                if type(body[0]) is not dict:
                    body[0] = template[0]
                else:
                    for i in range(0, len(body)):
                        body[i]= generate_json(body[i],template[0])

            else:
                return body
    elif template is not None:
        return template
    return body

# default value & wrong format
assert  merge_json('[]','{}')=='{}'
assert  merge_json('{}', '[]')=='[]'

# Overwrite default value
assert  merge_json('{"A":1}','{}')=='{"A":1}'
assert  merge_json('{"A":null}','{}')=='{"A":null}'
assert  merge_json('{"A":{"AA":1}}','{}')=='{"A":{"AA":1}}'
assert  merge_json('{"A":{"AA":null}}','{}')=='{"A":{"AA":null}}'
assert  merge_json('{"A":["AA"]}','{}')=='{"A":["AA"]}'
assert  merge_json('{"A":["AA","AB"]}','{}')=='{"A":["AA","AB"]}'
assert  merge_json('{"A":1,"B":2}','{}')=='{"A":1,"B":2}'

assert  merge_json('["A"]','[]')=='["A"]'
assert  merge_json('["A","B"]','[]')=='["A","B"]'
assert  merge_json('[{"A":1}]','[]')=='[{"A":1}]'
assert  merge_json('[{"A":null}]','[]')=='[{"A":null}]'
assert  merge_json('[{"A":{"AA":1}}]','[]')=='[{"A":{"AA":1}}]'
assert  merge_json('[{"A":{"AA":null}}]','[]')=='[{"A":{"AA":null}}]'
assert  merge_json('[{"A":["AA"]}]','[]')=='[{"A":["AA"]}]'
assert  merge_json('[{"A":["AA","AB"]}]','[]')=='[{"A":["AA","AB"]}]'
assert  merge_json('[{"A":1},{"B":2}]','[]')=='[{"A":1},{"B":2}]'

# default value & wrong format
assert  merge_json('{}', '{"A":1}')=='{"A":1}'
assert  merge_json('{"A":[]}','{"A":1}')=='{"A":1}'
assert  merge_json('{"A":{}}','{"A":1}')=='{"A":1}'

# overwrite default value
assert  merge_json('{"A":2}','{"A":1}')=='{"A":2}'
assert  merge_json('{"A":null}','{"A":1}')=='{"A":null}'
assert  merge_json('{"A":2,"B":2}','{"A":1}')=='{"A":2,"B":2}'



# default value & wrong format
assert  merge_json('{}','{"A":["AA"]}')=='{"A":["AA"]}'
assert  merge_json('{"A":1}','{"A":["AA"]}')=='{"A":["AA"]}'
assert  merge_json('{"A":{}}','{"A":["AA"]}')=='{"A":["AA"]}'


# overwrite default value
assert  merge_json('{"A":[]}','{"A":["AA"]}')=='{"A":[]}'
assert  merge_json('{"A":[]}','{"A":[{"A0A":1}]}')=='{"A":[]}'
assert  merge_json('{"A":[]}','{"A":[["A00"]]}')=='{"A":[]}'
assert  merge_json('{"A":[[]]}','{"A":[["A00"]]}')=='{"A":[[]]}'

assert  merge_json('{"A":["AB"]}','{"A":["AA"]}')=='{"A":["AB"]}'
assert  merge_json('{"A":null}','{"A":["AA"]}')=='{"A":null}'
assert  merge_json('{"A":{"AA":null}}','{"A":{}}')=='{"A":{"AA":null}}'

# Default vaule dic in list
assert  merge_json('{"A":[{}]}','{"A":[{"A0A":1}]}')=='{"A":[{"A0A":1}]}'
assert  merge_json('{"A":[{},{}]}','{"A":[{"A0A":1}]}')=='{"A":[{"A0A":1},{"A0A":1}]}'
assert  merge_json('{"A":[{"A1A":2},{}]}','{"A":[{"A0A":1}]}')=='{"A":[{"A1A":2,"A0A":1},{"A0A":1}]}'

# Default vaule list in dict
assert  merge_json('{"A":{}}','{"A":{"AA":["AA0","AB0"]}}')=='{"A":{"AA":["AA0","AB0"]}}'
assert  merge_json('{"A":{}}','{"A":{"AA":[{"AA0":1}]}}')=='{"A":{"AA":[{"AA0":1}]}}'
assert  merge_json('{"A":{"AA":[]}}','{"A":{"AA":[{"AA0":1}]}}')=='{"A":{"AA":[]}}'
assert  merge_json('{"A":{"AA":[{"AA0":2}]}}','{"A":{"AA":[{"AA0":1}]}}')=='{"A":{"AA":[{"AA0":2}]}}'
assert  merge_json('{"A":{"AA":[{"AB0":2}]}}','{"A":{"AA":[{"AA0":1}]}}')=='{"A":{"AA":[{"AB0":2,"AA0":1}]}}'

# Default vaule dist in dict

assert  merge_json('{"A":{}}','{"A":{"AA":{"AAA":2}}}')=='{"A":{"AA":{"AAA":2}}}'
assert  merge_json('{"A":{"AB":{"AAA":2}}}','{"A":{"AA":{"AAA":2}}}')=='{"A":{"AB":{"AAA":2},"AA":{"AAA":2}}}'


# assert  merge_json('{"A":[{},{}]}','{"A":[{"A0A":1}]}')=='{"A":[{"A0A":1},{"A0A":1}]}'
# assert  merge_json('{"A":[{"A1A":2},{}]}','{"A":[{"A0A":1}]}')=='{"A":[{"A1A":2,"A0A":1},{"A0A":1}]}'



# Default vaule list in list -- NOT SUPPORT
# assert  merge_json('{}','{"A":[["A0A"]]}')=='{"A":[["A0A"]]}'
# assert  merge_json('{"A":[[]]}','{"A":[["A0A"]]}')=='{"A":[[]]}' # TODO not support



# overwrite default value



# assert  merge_json('["A"]','[]')=='["A"]'
# assert  merge_json('["A","B"]','[]')=='["A","B"]'
# assert  merge_json('[{"A":1}]','[]')=='[{"A":1}]'
# assert  merge_json('[{"A":null}]','[]')=='[{"A":null}]'
# assert  merge_json('[{"A":{"AA":1}}]','[]')=='[{"A":{"AA":1}}]'
# assert  merge_json('[{"A":{"AA":null}}]','[]')=='[{"A":{"AA":null}}]'
# assert  merge_json('[{"A":["AA"]}]','[]')=='[{"A":["AA"]}]'
# assert  merge_json('[{"A":["AA","AB"]}]','[]')=='[{"A":["AA","AB"]}]'
# assert  merge_json('[{"A":1},{"B":2}]','[]')=='[{"A":1},{"B":2}]'
#
#
#
# assert  merge_json('{"A":1,"B":null,"C":true}','{}')=='{"A":1,"B":null,"C":true}'
# assert  merge_json('[{"A":1},{"B":null},{"C":true}]','[]')=='[{"A":1},{"B":null},{"C":true}]'
# assert  merge_json('["A","B",true,1,null]','[]')=='["A","B",true,1,null]'
# assert  merge_json('{}','["A","B"]')=='["A","B"]'
# assert  merge_json('[]','["A","B"]')=='[]'
# assert  merge_json('["C"]','["A","B"]')=='["C"]'
# assert  merge_json('{}','{"root":["A","B"]}')=='{"root":["A","B"]}'
# assert  merge_json('{}','{"A":1}')=='{"A":1}'
# assert  merge_json('{"A":null}','{"A":1}')=='{"A":null}'
# assert  merge_json('{"A":1}','{"A":1}')=='{"A":1}'
# assert  merge_json('{"A":2}','{"A":1}')=='{"A":2}'
# assert  merge_json('{"A":["AA","BB"]}','{"A":1}')=='{"A":1}'
# assert  merge_json('{"B":2}','{"A":1}')=='{"B":2,"A":1}'
# assert  merge_json('{"B":null}','{"A":1}')=='{"B":null,"A":1}'
# assert  merge_json('["A"]', '[{"A":1}]')=='[{"A":1}]'
