
*** Keywords ***

[common] - Extract request body
    [Arguments]    ${path}   ${name}
    ${request}   REST.Output   ${path}
    [common] - Set variable   ${name}   ${request}

[common] - Extract response data
    [Arguments]    ${path}    ${name}
    ${response}   REST.Output   ${path}
    [common] - Set variable   ${name}   ${response}

[Common] - Verify and Extract
    [Arguments]   ${o_request}=None   ${o_response}=None   ${response_status}=200
    REST.Output
    REST.integer   response status   ${response_status}
    Run Keyword If   $o_request is not None   [common] - Extract request body   request body   ${o_request}
    Run Keyword If   $o_response is not None   [common] - Extract response data   $.data   ${o_response}
