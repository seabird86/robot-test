*** Keywords ***
[mms-api-gateway][pre_request] - client login - body
   [Arguments]   ${output}=body   ${remove_null}=${True}   ${remove_empty}=${True}   &{arg_dic}
   ${schema}              catenate     SEPARATOR=
       ...    {
       ...     	"client_id": "str",
       ...     	"client_secret": "str",
       ...     	"grant_type": "str"
       ...    }
   ${body}     generate json
        ...     json_schema=${schema}
        ...     args=${arg_dic}
        ...     remove_null=${remove_null}
        ...     remove_empty=${remove_empty}
   ${body}      evaluate  json.loads('''${body}''')    json
   [common] - Set variable       name=${output}      value=${body}