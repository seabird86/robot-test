
*** Keywords ***

[Rest] - Extract
    [Arguments]    ${path}   ${name}
    ${value}   REST.Output   ${path}
    [common] - Set variable   ${name}   ${value}

[Rest] - Verify and Extract
    [Arguments]   ${o_request}=${None}   ${o_response}=${None}   ${response_status}=200   ${response_code}=${None}   ${response_message}=${None}
    REST.output
    REST.Integer   response status   ${response_status}
    Run Keyword If   $o_request is not None   [Rest] - Extract   request body   ${o_request}
    Run Keyword If   $o_response is not None   [Rest] - Extract   $   ${o_response}
    Run Keyword If   $response_code is not None   REST.String   $.error.code   ${response_code}
    Run Keyword If   $response_message is not None   REST.String   $.error.message   ${response_message}

[Rest] - Build header
    [Arguments]    ${client_id}=ANH   ${lang}=en   ${o_header}=test_headers
    ${value}   create dictionary   Client-ID=${client_id}   Accept-Language=${lang}
    [common] - Set variable   ${o_header}   ${value}
# and $response_code is None