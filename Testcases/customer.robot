*** Settings ***
Library         ../Library/py/json_template.py
Resource        ../Resources/Apis/import.robot
Resource        ../Resources/Utilities/import.robot

*** Variables ***
${UPPER_CASES}    ABCDEFGHIJKLMNOPQRSTUVWXYZ
${LOWER_CASES}    abcdefghijklmnopqrstuvwxyz
${NUMBERS}        0123456789
${LETTERS}        ${UPPER_CASES}${LOWER_CASES}

*** Test Cases ***

TC0001- Create new customer
    [tags]   2022
    ${list}   create list
    [Customer][API] - Create customer message
       ...   o_request=test_customer
       ...   o_response=test_response
       ...   name=custom name
#       ...   rooms[]=${None}
#        ...   rooms[]=${list}
       ...   rooms[0].room_name=custom room 1
       ...   rooms[1].room_name=custom room 2
#       ...   rooms[1].value[]=${None}
       ...   rooms[1].value[]=${list}
#       ...   messages[]=${None}
#       ...   messages[]=${list}
#       ...   messages[0]=value
#       ...   messages[1]=value2


    log   ${test_customer}
    log   ${test_response}