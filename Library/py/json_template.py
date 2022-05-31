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

def merge_json(json_template, json_body):
    print(json_body)
    print(json_template)
    template = json.loads(json_template)
    body = json.loads(json_body)
    generate_json(template, body)
    print("******")
    print(json.dumps(body, indent = 4))



def generate_json(template, body):
    print(" ---> {} -- {}".format(template, body))
    for key, child in template.items():
        if type(child) is dict:
            if (key not in body) or (body[key] is None):
                body[key]={}
            generate_json(child, body[key])
        elif type(child) is list:
            if (key not in body) or body[key] is None:
                body[key]=[{}]
            if type(body[key]) is list:
                if len(body[key])==0:
                    body[key]=[{}]
                for row in body[key]:
                    generate_json(child[0], row)
        elif child is not None:
            body.setdefault(key,child)
            # if body[key] is None:
            #     body[key]=child;


# merge_json('{"A": 1}', '{}')
# merge_json('{"A": 1}', '{"A": null}')
# merge_json('{"A": {"AA":"AAval"}}', '{}')
# merge_json('{"A": {"AA":"AAval"}}', '{"A": {"AA":null}}')
# merge_json('{"A": {"AA":"AAval"}}', '{"A": {}}')
# merge_json('{"A": {"AA":"AAval"}}', '{"A": null}')
# merge_json('{"A": {"AA":"AAval"},"B":"Bval"}', '{"A": null,"B":"Bval1"}')
# merge_json('{"A": {"AA":"AAval"},"B":"Bval"}', '{"A": {"AA":null},"B":"Bval1"}')
# merge_json('{"A": {"AA":"AAval"},"B":"Bval"}', '{"B":"Bval1"}')

# merge_json('{"A": [{"AA":"AAval"}]}', '{}')
# merge_json('{"A": [{"AA":null}]}', '{}') ==> TODO  {"A": [{}]} or {"A": []}  or {"A": null}
# merge_json('{"A": [{"AA":null,"AB":null}]}', '{}')
# merge_json('{"A": [{"AA":null,"AB":"ABval"}]}', '{}')
# merge_json('{"A": [{"AA":null,"AB":"ABval"}]}', '{}')
# merge_json('{"A": [{"AA":null,"AB":"ABval"}]}', '{"A": [{"AA":"AAval","AB":"ABval2"}]}')
# merge_json('{"A": [{"AA":null,"AB":"ABval"}]}', '{"A": [{"AA":"AAval","AB":null}]}')
# merge_json('{"A": [{"AA":null,"AB":"ABval"}]}', '{"A": [{"AA":"AAval"}]}')
# merge_json('{"A": [{"AA":null,"AB":"ABval"}]}', '{"A": [{"AB":null}]}')

# merge_json('{"A": [{"AA":null,"AB":"ABval"}]}', '{"A": [{"AB":null},{}]}')

merge_json('{"A": [{"AA":"AAval","AB":"ABval"}]}', '{"A": [{"AB":null},{}]}')

merge_json('{"A": [{"AA":"AAval","AB":"ABval"}]}', '{"A": [{"AB":null},{}]}')
