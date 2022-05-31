*** Settings ***
#*** Variables ***

#${robotVar} =            FooBarBaz
*** Test Cases ***

TC0001- Create new customer
    [tags]  2022
#    GET         /users/1

#    ${schema}   catenate   SEPARATOR=
#           ...    {
#           ...     	"client_id": "str",
#           ...     	"client_secret": "str",
#           ...     	"grant_type": "str"
#           ...    }

    log    hello
#       ${body}      evaluate  json.loads('''${body}''')    json
#       [common] - Set variable       name=${output}      value=${body}
#    Do An Action        Argument
#    Do Another Action   ${robotVar}
