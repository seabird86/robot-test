
*** Keywords ***

[common] - Set variable
    [Arguments]    ${name}    ${value}
    Run keyword if    $name.startswith('suite_')   set suite variable   \${${name}}   ${value}
    ...    ELSE    set test variable    \${${name}}    ${value}
