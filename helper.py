from http.cookies import SimpleCookie

# makes a dictionary given a raw cookie
# https://stackoverflow.com/questions/32281041/converting-cookie-string-into-python-dict
def make_cookie_dict(raw_data):
    cookie = SimpleCookie()
    cookie.load(raw_data)

    # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
    # which is incompatible with requests. Manually construct a dictionary instead.
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value

    return cookies

# Function to convert a list to a string separated by spaces
def listToString(s): 
    # initialize an empty string
    str1 = " " 
    
    # return string  
    return (str1.join(s))

# SQLite Commands ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        uid             INTEGER PRIMARY KEY,
        first_name      TEXT,
        last_name       TEXT,
        current_role    TEXT,
        current_company TEXT
    );
"""

CREATE_CONNECTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS connections (
        uid1            INTEGER,
        uid2            INTEGER,
        FOREIGN KEY (uid1) REFERENCES users (uid),
        FOREIGN KEY (uid2) REFERENCES users (uid)
    );
"""

# the "OR REPLACE" accounts for if person already exists in the table
INSERT_NEW_USER = """
    INSERT OR REPLACE INTO users VALUES (?,?,?,?,?)
"""

INSERT_NEW_CONNECTION = """
    INSERT INTO connections VALUES (?,?)
"""

# Example cookie for use later
# EXAMPLE_COOKIE = "li_sugr=a139e1f3-eaaf-4db9-b8a8-89e840df6070; bcookie=\"v=2&146643ae-3b6d-4178-8d01-5968f575ba45\"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; _ga=GA1.2.1528297046.1589461568; aam_uuid=58832049292474466107487088016719316396; spectroscopyId=8b1bc840-50b0-48c4-897c-9645e8a09f05; visit=\"v=1&M\"; PLAY_LANG=en; __ssid=74602b58-6f92-4f89-8edb-ce7c1fd0eae9; ELOQUA=GUID=00AC0056F1044F1F99135F129B2754AE; s_cc=true; sl=\"v=1&3dyww\"; SID=1f01f412-c020-4b2d-9bc3-ee14769790c7; VID=V_2020_08_28_08_640; at_check=true; lil-lang=en_US; s_fid=3BCEF98C2892C316-2478BD59C8A0A0A2; G_ENABLED_IDPS=google; JSESSIONID=\"ajax:7378062402392048172\"; _gcl_au=1.1.1733225399.1609737531; liap=true; timezone=Australia/Sydney; liveagent_oref=https://www.linkedin.com/help/sales-navigator/answer/a106005/integration-between-sales-navigator-and-your-crm-overview?lang=en; liveagent_ptid=47dafc79-3ac3-4a2b-89a4-27e37022eeb7; liveagent_sid=6514b2e5-9e44-4bc3-832e-4c3d13c7d38f; liveagent_vc=3; _guid=8316278d-e066-4114-b76a-8b87a27797e6; lang=v=2&lang=en-us; s_sq=lnkddev%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fwww.linkedin.com%25252Ftalent%25252Fjob-posting%25252Fonline%25252Fbasic-info%25253FjobId%25253D2004866679%2526link%253DSydney%25252C%252520New%252520South%252520Wales%25252C%252520Australia%2526region%253Dember2264%2526.activitymap%2526.a%2526.c; cap_session_id=3186243841:1; li_er=v=1&r=urn:li:contract:263886261&t=1619269102699&g=MDIxnEgFwGOc/Dh4fIMW7lLgEsU2uBf5Py7CXNa0GiVU3Z4=; u_tz=GMT+10:00; _gac_UA-62256447-1=1.1621395155.CjwKCAjwy42FBhB2EiwAJY0yQnkZ6KgFhDp1Za4bsZ5iKAFoMEJj_miDA72zIPG-UOwC0xDtYfWsyBoCjosQAvD_BwE; mbox=PC#335a8f310a2944a0aed901c0a5c61682.36_0#1636947157|session#50c4e8a8d120400fb68b2160cb3a65a0#1621397016; gpv_pn=learning.linkedin.com%2Fen-us%2Fcx%2F2017%2Fmay%2Flls-sem-leaders; s_plt=2.35; s_pltp=learning.linkedin.com%2Fen-us%2Fcx%2F2017%2Fmay%2Flls-sem-leaders; s_tslv=1621395157053; _gcl_aw=GCL.1621395158.CjwKCAjwy42FBhB2EiwAJY0yQnkZ6KgFhDp1Za4bsZ5iKAFoMEJj_miDA72zIPG-UOwC0xDtYfWsyBoCjosQAvD_BwE; _gcl_dc=GCL.1621395158.CjwKCAjwy42FBhB2EiwAJY0yQnkZ6KgFhDp1Za4bsZ5iKAFoMEJj_miDA72zIPG-UOwC0xDtYfWsyBoCjosQAvD_BwE; s_ips=1553; s_tp=3301; s_ppv=learning.linkedin.com%2Fen-us%2Fcx%2F2017%2Fmay%2Flls-sem-leaders%2C100%2C47%2C3301%2C2%2C2; lms_ads=AQFajoQot8EEOAAAAXmR_-cgUY8cjCPzEU9tH7MawfxWroXbY0tgX5Ob0JgHX0LwpRKM5G2g0BC7LhzNvwdbbUaxSt535JqP; lms_analytics=AQFajoQot8EEOAAAAXmR_-cgUY8cjCPzEU9tH7MawfxWroXbY0tgX5Ob0JgHX0LwpRKM5G2g0BC7LhzNvwdbbUaxSt535JqP; _gid=GA1.2.1027317372.1621891640; AnalyticsSyncHistory=AQKa3E5xwhhzawAAAXmh4JKgjMwPTqBoYA62Qx3H_IQzGDhbcsuQ1r6q6WlFNXysQCHwNQWtFc6jBMKRx78HkQ; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; UserMatchHistory=AQKKi3IN0mdMKQAAAXmsmWc_fsu1FIgcDZDNdEmnSjXJ6wP_phVvV5-tpyFS0DP5bGeMdvy3CGc8vFYLTTKKeqz7c30nAcmRGMVwja8FI3XHzOMoMBm10-O3lMi1lYSb-g4omh9nD1oZvN_Te1JgKDinBR4FMfqLTZgqWJplgr4JnQJ4TAr2b-9_KB-s-unzQYb6SpOhOZh5eyTmDi0TsNCatobzNS_u6UG0QCRhrFCgsRy0S0nCEQez4uNLlJ8EKVQr3YzzYWVWcSdSJaM_kavaRXboibQH9qGxF9qK1kkr7IQR8GbwOeda8QynpevZ-w; lidc=\"b=TB39:s=T:r=T:a=T:p=T:g=3428:u=161:i=1622098406:t=1622102166:v=2:sig=AQGp5wzp_Js8voxOToLABKpBpKyNwIjh\"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C18774%7CMCMID%7C58666340022011795457433285600072005223%7CMCOPTOUT-1622105608s%7CNONE%7CvVersion%7C5.1.1%7CMCAAMLH-1622703208%7C8%7CMCAAMB-1622703208%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCCIDH%7C-247464000"
EXAMPLE_COOKIE = 'li_sugr=a139e1f3-eaaf-4db9-b8a8-89e840df6070; bcookie="v=2&146643ae-3b6d-4178-8d01-5968f575ba45"; bscookie="v=1&20200512123632440cd0f4-f4c7-4ad7-8e5f-a06fdb9ebbdfAQHcejGFjg9Nt8H_egg1JLXKysQ9Hp6C"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; _ga=GA1.2.1528297046.1589461568; aam_uuid=58832049292474466107487088016719316396; spectroscopyId=8b1bc840-50b0-48c4-897c-9645e8a09f05; visit="v=1&M"; PLAY_LANG=en; __ssid=74602b58-6f92-4f89-8edb-ce7c1fd0eae9; ELOQUA=GUID=00AC0056F1044F1F99135F129B2754AE; s_cc=true; sl="v=1&3dyww"; SID=1f01f412-c020-4b2d-9bc3-ee14769790c7; VID=V_2020_08_28_08_640; at_check=true; lil-lang=en_US; s_fid=3BCEF98C2892C316-2478BD59C8A0A0A2; li_rm=AQFyq_jmc5Cc0AAAAXTXgpWcQJr22rB89saaqGcjMvXY7h_FGukPGu0oVRiQsDFbblRvwlraBrJ5nSNzn1Fg4VwTRv5ZgzlUrr5HKrX7croMH4S0uZYft8jc; G_ENABLED_IDPS=google; JSESSIONID="ajax:7378062402392048172"; _gcl_au=1.1.1733225399.1609737531; liap=true; dfpfpt=ee303ab5a00345b09d66c174262c1ae2; timezone=Australia/Sydney; li_ep_auth_context=AFdhcHA9c2FsZXNOYXZpZ2F0b3IsYWlkPTEwNDUzNDk3OCxpaWQ9MTEyNTg4NDU4LHBpZD0xMTc1NzA5OTgsZXhwPTE2MTc0OTM0MTYyMTEsY3VyPXRydWUBS58xYxzt4Y5RjPl35NK7WgrirhY; fptctx2=taBcrIH61PuCVH7eNCyH0J3vcgCbtea3jxoypkMntAgUtnpNA%252fnhuL6bVMyKJFube1rIweGeaRtH3xFBK0MMaKzPTLVEkLnUj37ISmVktsoQXVXVWkFG6MVK2Dh6W4mDtaEpWlEY4aTX2A1trRURvYJPfOI47HpD7ezd%252f%252fSmsuGoyE8uxrixhKoFBFeUEOw4TCOKYr7t2sRB%252bzpj%252fmRoHaMmjt6qSoOr3OR2YhhckaeLxZqmJYypcYAf5EYpigzMi5My47mSX5gsvKk8rTgowEp%252bJuQKOe9K7chfrMjMWC190UUv0OunSnpIbOn1VW1B; liveagent_oref=https://www.linkedin.com/help/sales-navigator/answer/a106005/integration-between-sales-navigator-and-your-crm-overview?lang=en; liveagent_ptid=47dafc79-3ac3-4a2b-89a4-27e37022eeb7; liveagent_sid=6514b2e5-9e44-4bc3-832e-4c3d13c7d38f; liveagent_vc=3; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiI2NjhiMWJlNi1iYjIwLTRlZDAtOTczMS0zNDg2N2ZlYmQ0OWZ8MTYxNjEwNjAzNSIsInJlY2VudGx5LXNlYXJjaGVkIjoiIiwicmVmZXJyYWwtdXJsIjoiaHR0cHM6Ly93d3cubGlua2VkaW4uY29tL3RhbGVudC9qb2ItcG9zdGluZy9wb3N0P2NvbXBhbnk9RWxlbnRhJmNvdW50cnlDb2RlPXVybiUzQWxpJTNBdHNfY291bnRyeSUzQUFVJmdlb0xvY2F0aW9uSWQ9MTA0NzY5OTA1Jmdlb1Vybj11cm4lM0FsaSUzQXRzX2dlbyUzQTEwNDc2OTkwNSZsb2NhdGlvbj1TeWRuZXklMkMlMjBOZXclMjBTb3V0aCUyMFdhbGVzJTJDJTIwQXVzdHJhbGlhJnRpdGxlPUZ1bGwtU3RhY2slMjBTb2Z0d2FyZSUyMEVuZ2luZWVyaW5nJTIwTGVhZCZ0aXRsZUlkPTM5IiwiYWlkIjoiIiwiUk5ULWlkIjoifDAiLCJyZWNlbnRseS12aWV3ZWQiOiI3MTkxOXw2Njg0NHwyOXw4NTM1MXw5MTQyMyIsIkNQVC1pZCI6IsOaIUggXHUwMDBGwqM7w4PCh8ObI8OEK8OaQ1x1MDAxMCIsImZsb3dUcmFja2luZ0lkIjoiTGZBUjRBcitTZGVSeEZkNCtZc1pxUT09IiwiZXhwZXJpZW5jZSI6ImVudGl0eSIsImlzX25hdGl2ZSI6ImZhbHNlIiwid2hpdGVsaXN0Ijoie1wiQnVzaW5lc3MgU2VnbWVudDpTdHJhdGVnaWNcIjpcImZhbHNlXCJ9IiwidHJrIjoiIn0sIm5iZiI6MTYxNjEyNTIxMSwiaWF0IjoxNjE2MTI1MjExfQ.iHN2GuxlrNEAyjxkfeNSpwuRcbbVx-RP61_E1ZEoB18; _guid=8316278d-e066-4114-b76a-8b87a27797e6; lang=v=2&lang=en-us; s_sq=lnkddev%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fwww.linkedin.com%25252Ftalent%25252Fjob-posting%25252Fonline%25252Fbasic-info%25253FjobId%25253D2004866679%2526link%253DSydney%25252C%252520New%252520South%252520Wales%25252C%252520Australia%2526region%253Dember2264%2526.activitymap%2526.a%2526.c; cap_session_id=3186243841:1; li_er=v=1&r=urn:li:contract:263886261&t=1619269102699&g=MDIxnEgFwGOc/Dh4fIMW7lLgEsU2uBf5Py7CXNa0GiVU3Z4=; u_tz=GMT+10:00; _gac_UA-62256447-1=1.1621395155.CjwKCAjwy42FBhB2EiwAJY0yQnkZ6KgFhDp1Za4bsZ5iKAFoMEJj_miDA72zIPG-UOwC0xDtYfWsyBoCjosQAvD_BwE; mbox=PC#335a8f310a2944a0aed901c0a5c61682.36_0#1636947157|session#50c4e8a8d120400fb68b2160cb3a65a0#1621397016; gpv_pn=learning.linkedin.com%2Fen-us%2Fcx%2F2017%2Fmay%2Flls-sem-leaders; s_plt=2.35; s_pltp=learning.linkedin.com%2Fen-us%2Fcx%2F2017%2Fmay%2Flls-sem-leaders; s_tslv=1621395157053; _gcl_aw=GCL.1621395158.CjwKCAjwy42FBhB2EiwAJY0yQnkZ6KgFhDp1Za4bsZ5iKAFoMEJj_miDA72zIPG-UOwC0xDtYfWsyBoCjosQAvD_BwE; _gcl_dc=GCL.1621395158.CjwKCAjwy42FBhB2EiwAJY0yQnkZ6KgFhDp1Za4bsZ5iKAFoMEJj_miDA72zIPG-UOwC0xDtYfWsyBoCjosQAvD_BwE; s_ips=1553; s_tp=3301; s_ppv=learning.linkedin.com%2Fen-us%2Fcx%2F2017%2Fmay%2Flls-sem-leaders%2C100%2C47%2C3301%2C2%2C2; li_at=AQEFAHQBAAAAAATPiAEAAAF5aXbkawAAAXmxkzebVgAAF3VybjpsaTptZW1iZXI6MTg2MzYxOTM5zRb9K2is1fkvlmABnVpfCa7cCBL9wlbwPAvu5aiw1Jy3Dvy3aZeBz_GXyfq04XdviTe_oTFnegEReqca0huARiRRl2Zm2V332-bG5FvTQiLjbg0ghKudsaO28m4Hny1U7avwLo7RmApZMmumkb2Ghqp_OM234OGz5Iia1dOh862wQ4VPHyUvliv-CL4ZNkay6N3Kdg; lms_ads=AQFajoQot8EEOAAAAXmR_-cgUY8cjCPzEU9tH7MawfxWroXbY0tgX5Ob0JgHX0LwpRKM5G2g0BC7LhzNvwdbbUaxSt535JqP; lms_analytics=AQFajoQot8EEOAAAAXmR_-cgUY8cjCPzEU9tH7MawfxWroXbY0tgX5Ob0JgHX0LwpRKM5G2g0BC7LhzNvwdbbUaxSt535JqP; _gid=GA1.2.1027317372.1621891640; AnalyticsSyncHistory=AQKa3E5xwhhzawAAAXmh4JKgjMwPTqBoYA62Qx3H_IQzGDhbcsuQ1r6q6WlFNXysQCHwNQWtFc6jBMKRx78HkQ; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C18774%7CMCMID%7C58666340022011795457433285600072005223%7CMCOPTOUT-1621996208s%7CNONE%7CvVersion%7C5.1.1%7CMCAAMLH-1622593808%7C8%7CMCAAMB-1622593808%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCCIDH%7C-247464000; UserMatchHistory=AQIR7icIV_RqZAAAAXmme2NA5lk5gFVI2hmAMSApjfQIsdqOFkMTq5z5ckCXQVOkgnhWB9EQOLvjrRDD6aqNCVYCxyG9sFNL-EzmP4Et0rt2YIqXEqPMK1VvzgNOpHzSVFweS3GbpzN_Bo3GnNp1rqFxrv0bP1oc5IfSxiLJbTC9KInaOqCbuPXLSyO9PQtRWTwdLoUoTzO89FnWm2-m-wOvSiutrWSkeWrM07IWR-hYD3Db-OIeSTbhBwFAO0mT129yiud7-IMKYyn-Ve-rXqZf-3bOzelTL6NJnX28LUX-yl8jm-ECUjiOzd8YvR_Clw; lidc="b=OB39:s=O:r=O:a=O:p=O:g=2975:u=158:i=1621995776:t=1622073227:v=2:sig=AQF3CnXfQsv39an_tUOgRw-KIPZjqqh0"; li_a=AQJ2PTEmc2FsZXNfY2lkPTg0NDMwMjUwNyUzQSUzQTIzNDM2NjQwN7SMdY29EUr4g3di19h1JbakJ77-'