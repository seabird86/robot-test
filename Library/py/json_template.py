#!/usr/bin/env python3

import re
import json
import random
import copy

def random_str(size, chars):
    return ''.join(random.choice(chars) for _ in range(size))

def random_int(min, max):
    return random.randint(min, max)

def random_bool():
    return random_int(0, 1) == 1

def random_decimal(min, max, decimal_digits):
    return _round_decimal(random.uniform(min, max), decimal_digits)

def random_enum(*args):
    index = random_int(0, len(args) - 1)
    return args[index]

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
# If null -> keep null
# If absent or If conflict type with template -> get template to overwrite with default
# If is dic -> merge key
# If is [] and body absent or If conflict type with template-> get template to overwrite with default
# If template is primitive -> set default if body is primitive or body is not primitive

def generate_json_now(body,json_template):
    json_body=json.dumps(body,separators=(',', ':'))
    body = json.loads(json_body)
    template = json.loads(json_template)
    body = generate_json(body,template)
    json_body=json.dumps(body,separators=(',', ':'))
    # print("===={}".format(json_body))
    return json_body

def parse_value(value):
    print("++{} ".format(value))
    return eval(value.partition(' ')[2])

def _generate_json(template):
    if type(template) is dict:
        for key, child in template.items():
            template[key] = _generate_json(template[key])
            # if type(template[key]) is dict:
            #     template[key] = _generate_json(template[key])
            # elif type(template[key]) is list:
            #     if len(template[key])==0:
            #         return template
            #     if len(template[key])==1:
            #         template[key]=_generate_json(template[key])
            # else:
            #     template[key]=parse_value(template[key])
    elif type(template) is list:
        if len(template)==0:
            return template
        if len(template)==1:
            template[0]=_generate_json(template[0])
    else:
        return parse_value(template)
    return template

def generate_json(body,template):
    print("--- {} --- {}".format(body, template))
    if type(template) is dict:
        if body is None:
            return body
        if type(body) is not dict:
            raise Exception("Incompatible type dict")
        for key, child in template.items():
            if type(template[key]) is dict:
                if key not in body:
                    template[key] = _generate_json(template[key])
                    continue
                elif body[key] is None:
                    template[key]=None
                    continue
                elif type(body[key]) is not dict:
                    raise Exception("Incompatible type dict")
                template[key] = generate_json(body[key],template[key])
            elif type(template[key]) is list:
                if key not in body:
                    template[key] = _generate_json(template[key])
                    continue
                elif body[key] is None:
                    template[key]=None
                    continue
                elif type(body[key]) is not list:
                    raise Exception("Incompatible type list")
                template[key] = generate_json(body[key],template[key])
            else:
                print("====>")
                if key not in body:
                    print("++++>")
                    template[key] = parse_value(template[key])
                    continue
                elif body[key] is None:
                    template[key]=None
                    continue
                elif type(body[key]) is dict or type(body[key]) is list:
                    raise Exception("Incompatible type primitive")
                template[key]=body[key]
    elif type(template) is list:
        if body is None:
            return _generate_json(template)
        if type(body) is not list:
            raise Exception("Incompatible type list")
        if len(template) == 0:
            return list
        if len(template) == 1:
            if len(body) == 0:
                return []
            for i in range(1, len(body)):
                template.append(copy.deepcopy(template[0]))
            for i in range(0, len(body)):
                template[i]= generate_json(body[i],template[i])
    else:
        if  type(body) is dict or type(body) is list:
            raise Exception("Incompatible type primitive")
        return body
    return template


# default value & wrong format
assert  merge_json('{}','{"A":"int random_enum(1)"}')=='{"A":1}'
assert  merge_json('{}','{"A":{"AA":"int random_enum(1)"}}')=='{"A":{"AA":1}}'
assert  merge_json('{}','{"A":{"AA":{"AAA":"int random_enum(1)"}}}')=='{"A":{"AA":{"AAA":1}}}'
assert  merge_json('{}','{"A":[{"AA":"int random_enum(1)"}]}')=='{"A":[{"AA":1}]}'
assert  merge_json('{}','{"A":["int random_enum(1)"]}')=='{"A":[1]}'
assert  merge_json('{}','{"A":[{"AA":"int random_enum(1)","AB":"int random_enum(1)"}]}')=='{"A":[{"AA":1,"AB":1}]}'
assert  merge_json('{}','{"A":[{"AA":[{"AAA":"int random_enum(1)"}]}]}')=='{"A":[{"AA":[{"AAA":1}]}]}'
assert  merge_json('{"A":1}','{"A":"int random_enum(1)"}')=='{"A":1}'
assert  merge_json('{"A":2,"B":2}','{"A":"int random_enum(1)"}')=='{"A":2}'
assert  merge_json('{"A":{"AA":{}}}','{"A":{"AA":{"AAA":"int random_enum(1)"}}}')=='{"A":{"AA":{"AAA":1}}}'
assert  merge_json('{"A":{"AA":null}}','{"A":{"AA":{"AAA":"int random_enum(1)"}}}')=='{"A":{"AA":null}}'
assert  merge_json('{"A":{"AA":{"AAA":2}}}','{"A":{"AA":{"AAA":"int random_enum(1)"}}}')=='{"A":{"AA":{"AAA":2}}}'

assert  merge_json('{"A":null}','{"A":[{"AA":"int random_enum(1)"}]}')=='{"A":null}'
assert  merge_json('{"A":[]}','{"A":[{"AA":"int random_enum(1)"}]}')=='{"A":[]}'
assert  merge_json('{"A":[{"AA":2}]}','{"A":[{"AA":"int random_enum(1)"}]}')=='{"A":[{"AA":2}]}'
# assert  merge_json('{"A":[{},{}]}','{"A":[{"AA":"int random_enum(1)"}]}')=='{"A":[{"AA":1},{"AA":1}]}'
assert  merge_json('[{},{}]','[{"AA":"int random_enum(1)"}]')=='[{"AA":1},{"AA":1}]'

# assert  merge_json('{"A":[[{"AA":2}]]}','{"A":[[{"AA":"int random_enum(1)"}]]}')=='{"A":[{"AA":2}]}'

# assert  merge_json('{"A":[]}','{"A":[{"AA":"int random_enum(1)"}]}')=='{"A":[]}'
# assert  merge_json('{}','{"A":[{"AA":"int random_enum(1)"}]}')=='{"A":[{"AA":1}]}'
