*** Keywords ***
[customer] - Create customer
    [Arguments]   ${body}   ${headers}=${SUITE_ADMIN_HEADERS}
    REST.post   http://localhost:8021/customer/customers   body=${body}
    rest extract
    [common][verify] - Http status code is "200"
