*** Settings ***
Resource         ../../0_Library/import.robot

*** Keywords ***

[Customer][API][Direct] - Create customer message
    [Arguments]   ${o_request}=${None}   ${o_response}=${None}   ${headers}={}   ${params}={}   ${response_status}=200   &{args}
    ${template}   catenate   SEPARATOR=
       ...  {
       ...       "name":"str random_str(4,'${LETTERS}')",
       ...       "messages":["str random_str(4,'${LETTERS}')"],
       ...       "rooms":[
       ...           {
       ...             "room_name":"str random_str(4,'${LETTERS}')",
       ...             "value":[{
       ...                 "furniture_name": "str random_str(4,'${LETTERS}')",
       ...                 "value":["str random_str(4,'${LETTERS}')"]
       ...             }]
       ...           }
       ...       ]
       ...   }
   ${body}   build body   ${args}   ${template}
   REST.post   ${URL.customer_direct}/messages   headers=${headers}   body=${body}   data=${params}
   [Rest] - Verify and Extract   ${o_request}   ${o_response}   ${response_status}

[Customer][API] - Create customer message
    [Arguments]   ${o_request}=${None}   ${o_response}=${None}   ${headers}={}   ${params}={}   ${response_status}=200   ${response_code}=${None}   ${response_message}=${None}   &{args}
    ${template}   catenate   SEPARATOR=
       ...  {
      ...       "name":"str random_str(4,'${LETTERS}')",
      ...       "messages":["str random_str(4,'${LETTERS}')"],
      ...       "rooms":[
      ...           {
      ...             "room_name":"str random_str(4,'${LETTERS}')",
      ...             "value":[{
      ...                 "furniture_name": "str random_str(4,'${LETTERS}')",
      ...                 "value":["str random_str(4,'${LETTERS}')"]
      ...             }]
      ...           }
      ...       ]
      ...   }
   ${body}   build body   ${args}   ${template}
   REST.post   ${URL.customer}/messages   headers=${headers}   body=${body}   data=${params}
   [Rest] - Verify and Extract   ${o_request}   ${o_response}   ${response_status}   ${response_code}   ${response_message}

[Customer][API] - Create customer
    [Arguments]   ${o_request}=${None}   ${o_response}=${None}   ${remove_null}=${True}   ${remove_empty}=${True}   ${response_status}=200    &{args}
    log    ${args}
    ${template}   catenate   SEPARATOR=
       ...    {
       ...     	"username": "str random_str(4,'${LETTERS}')",
       ...     	"name": "str random_str(4,'${LETTERS}')",
       ...     	"mobile": "str random_str(4,'${LETTERS}')",
       ...      "date_of_birth": "str random_str(4,'${LETTERS}')",
       ...      "verified_datetime":  "str random_str(4,'${LETTERS}')",
       ...      "available_time":  "str random_str(4,'${LETTERS}')"
       ...    }
   ${body}   build body   ${args}   ${template}
   REST.post   ${URL.customer}/customers   headers=${headers}   body=${body}
   [Rest] - Verify and Extract   ${o_request}   ${o_response}   ${response_status}