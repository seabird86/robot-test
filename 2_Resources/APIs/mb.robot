*** Settings ***
Resource         ../../0_Library/import.robot

*** Variables ***



*** Keywords ***

[MB] - Delete all mocks
    REST.delete   ${URL.mb}/imposters
    REST.output
    REST.integer   response status     200

[MB] - Delete specific mock
    [Arguments]  ${port}
    REST.delete   ${URL.mb}/imposters/${mock_port}
    REST.output
    REST.integer   response status     200

[MB] - Create mock
    [Arguments]  ${body}
    REST.post   ${URL.mb}/imposters   body=${body}
    REST.output
    REST.integer   response status     201

[MB] - Create mock in a port
    [Arguments]  ${body}    ${port}
    [MB] - Delete specific mock   ${port}
    Create mock   ${body}