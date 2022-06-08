*** Settings ***
Resource        ../2_Resources/import.robot

*** Variables ***

*** Test Cases ***

TC0002 - [Fail] Create customer with Invalid client
    [tags]   2022
    ${list}   create list
    [Customer][API] - Create customer message
        ...   o_request=test_customer
        ...   response_status=400
        ...   response_code=AGW00002
        ...   response_message=Header [Client-ID] is Required
        ...   name=custom name
        ...   rooms[0].room_name=custom room 1
        ...   rooms[1].room_name=custom room 2
        ...   rooms[1].value[]=${list}
    log   ${test_customer}

TC0003 - Create customer with Invalid client
    [tags]   2022
    ${list}   create list
    [Rest] - Build header   o_header=test_headers
    [Customer][API] - Create customer message
        ...   o_request=test_customer
        ...   o_response=test_response
        ...   headers=${test_headers}
        ...   name=custom name
        ...   rooms[0].room_name=custom room 1
        ...   rooms[1].room_name=custom room 2
        ...   rooms[1].value[]=${list}
    [Customer][API] - Create customer message
            ...   o_request=test_customer
            ...   o_response=test_response
            ...   headers=${test_headers}
            ...   name=custom name
            ...   rooms[0].room_name=custom room 1
            ...   rooms[1].room_name=custom room 2
            ...   rooms[1].value[]=${list}

    [Customer][API] - Create customer message
            ...   o_request=test_customer
            ...   o_response=test_response
            ...   headers=${test_headers}
            ...   name=custom name
            ...   rooms[0].room_name=custom room 1
            ...   rooms[1].room_name=custom room 2
            ...   rooms[1].value[]=${list}
    [Customer][API] - Create customer message
            ...   o_request=test_customer
            ...   o_response=test_response
            ...   headers=${test_headers}
            ...   name=custom name
            ...   rooms[0].room_name=custom room 1
            ...   rooms[1].room_name=custom room 2
            ...   rooms[1].value[]=${list}
    log   ${test_customer}
    log   ${test_response}