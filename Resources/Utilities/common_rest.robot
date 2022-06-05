
*** Keywords ***

[Rest] - Extract
    [Arguments]    ${path}   ${name}
    ${value}   REST.Output   ${path}
    [common] - Set variable   ${name}   ${value}

[Rest] - Verify and Extract
    [Arguments]   ${o_request}=None   ${o_response}=None   ${response_status}=200
    REST.Output
    REST.integer   response status   ${response_status}
    Run Keyword If   $o_request is not None   [Rest] - Extract   request body   ${o_request}
    Run Keyword If   $o_response is not None   [Rest] - Extract   $.data   ${o_response}
