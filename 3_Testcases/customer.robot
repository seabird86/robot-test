*** Settings ***
Resource        ../2_Resources/import.robot

Suite Setup     Run keywords   Set Suite Variable    ${name}     $example   AND
                ...   log   ${name}   AND
                ...   Set Suite Variable    ${name}     value   AND
                ...   log   ${name}   AND
                ...   Set Suite Variable    $name       value    AND
                ...   log   ${name}   AND
                ...   Set Suite Variable    \${name}    value

*** Variables ***
${UPPER_CASES}    ABCDEFGHIJKLMNOPQRSTUVWXYZ
${LOWER_CASES}    abcdefghijklmnopqrstuvwxyz
${NUMBERS}        0123456789
${LETTERS}        ${UPPER_CASES}${LOWER_CASES}



Set Suite Variable    ${name}     value    # Creates ${example}.
Set Suite Variable    $name       value    # Creates ${name}.
Set Suite Variable    \${name}    value    # Creates ${name}.

*** Test Cases ***

TC0001- Create new customer
    [tags]   2022
    ${list}   create list
    [Customer][API] - Create customer message
       ...   o_request=test_customer
       ...   o_response=test_response
       ...   headers=
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