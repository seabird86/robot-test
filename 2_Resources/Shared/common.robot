
*** Keywords ***

[common] - Set variable
    [Arguments]    ${name}    ${value}
    Run keyword if    $name.startswith('suite_')   set suite variable   \${${name}}   ${value}
    ...    ELSE    set test variable    \${${name}}    ${value}

[common] - Set extracted variable
    [Arguments]   ${path}   ${name}
    ${result}     REST.output    ${path}
    [common] - set variable    ${name}   ${result}

[common] - Merge dictionary
    [Arguments]   ${output}   ${dictionary}
    FOR    ${key}     IN    @{dictionary}
           ${passed}=    Run Keyword And Return Status   Evaluate    type(${dictionary["${key}"]})
           ${input_type}    Run Keyword If     ${passed}     Evaluate    type(${dictionary["${key}"]})
           ${passed}=    Run Keyword And Return Status   Evaluate    type(${output["${key}"]})
           ${output_type}   Run Keyword If     ${passed}     Evaluate    type(${output["${key}"]})
           Run keyword if   "${input_type}"=="<class 'dict'>" and "${output_type}"=="<class 'dict'>"   [common] - Merge dictionary    ${output["${key}"]}   ${dictionary["${key}"]}
           ...   ELSE   set to dictionary    ${output}    ${key}=${dictionary["${key}"]}
    END