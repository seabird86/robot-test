*** Settings ***
Resource        ../../0_Library/import.robot
Resource        ../../2_Resources/APIs/url.robot

*** Keywords ***

[MB][API] - Delete all mocks
    REST.delete   ${URL.mb}/imposters
    REST.output
    REST.integer   response status     200

[MB][API] - Delete mock
    [Arguments]  ${port}
    REST.delete   ${URL.mb}/imposters/${port}
    REST.output
    REST.integer   response status     200

[MB][API] - Create mock
    [Arguments]  ${body}   ${port}=${None}
    REST.post   ${URL.mb}/imposters   ${body}
    REST.output
    REST.integer   response status     201

*** Test Cases ***

TC9999- Create mock
    [tags]   2022
    [MB][API] - Delete mock   1100
    [MB][API] - Create mock   ${CURDIR}/body/customer.json