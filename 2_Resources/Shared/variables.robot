*** Variables ***

&{URL}   mb=http://localhost:2525
...     customer_direct=http://localhost:8021/customer
...     customer=http://localhost:8024/api-gateway/customer

${UPPER_CASES}    ABCDEFGHIJKLMNOPQRSTUVWXYZ
${LOWER_CASES}    abcdefghijklmnopqrstuvwxyz
${NUMBERS}        0123456789
${LETTERS}        ${UPPER_CASES}${LOWER_CASES}