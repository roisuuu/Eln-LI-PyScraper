import requests
import sys
import sqlite3
import os

import helper
import fetch_functions

# main driver function
def get_page(start, count, cursor, connection):
    url = f"https://www.linkedin.com/sales-api/salesApiPeopleSearch?q=peopleSearchQuery&start={start}&count={count}&query=(companySize:List(D,E,F),doFetchHeroCard:false,functionV2:(includedValues:List((id:12))),bingGeo:(includedValues:List((id:101452733),(id:105490917))),industryV2:(excludedValues:List((id:67),(id:75),(id:79))),recentSearchParam:(doLogHistory:false,id:981486524),relationship:List(S),spotlightParam:(selectedType:ALL),titleV2:(scope:CURRENT,includedValues:List((text:Director%20Of%20Learning,id:2598),(text:Learning%20Manager,id:2328),(text:Learning%20Lead,id:7814),(text:Head%20Of%20Learning,id:8180),(text:Director%20of%20Learning%20and%20Development,id:4898),(text:Head%20of%20Learning%20and%20Development,id:8566),(text:Learning%20Development%20Officer,id:16817),(text:Chief%20People%20Officer,id:16343),(text:Director%20People%20Development,id:18215),(text:Capability%20Manager,id:5562),(text:Capability%20Development%20Manager,id:19240),(text:Talent%20Development%20Manager,id:8819),(text:Director%20Talent%20Development,id:12093),(text:Head%20Of%20Training%20And%20Development,id:9818),(text:Organizational%20Development%20Specialist,id:1256),(text:Organizational%20Development%20Manager,id:2289),(text:Head%20Organizational%20Development,id:7718),(text:Organizational%20Development%20Advisor,id:20635),(text:Organizational%20Development%20Officer,id:26522),(text:Vice%20President%20of%20Learning%20and%20Development,id:10186),(text:Learning%20and%20Development%20Advisor,id:14850),(text:Learning%20and%20Development%20Manager,id:1917),(text:Head%20of%20People%20%26%20Culture),(text:Head%20of%20People%20and%20Culture),(text:People%20%26%20Talent%20Manager),(text:People%20and%20Culture%20Manager),(text:People%20%26%20Culture%20Manager),(text:People%20%26%20Talent%20Lead),(text:Head%20of%20Employee%20Experience,id:27072),(text:Employee%20Experience%20Manager,id:27054),(text:Chief%20Employee%20Experience%20Officer,id:27020),(text:Director%20of%20Employee%20Experience,id:27043),(text:Director%20of%20People%20and%20Culture),(text:Director%20of%20People%20%26%20Culture),(text:People%20and%20Culture%20Director),(text:People%20%26%20Culture%20Director),(text:Leadership%20Development%20Program,id:3947),(text:Leadership%20Consultant,id:6292),(text:Leadership%20Development%20Manager,id:5962),(text:Director%20Leadership%20Development,id:6221),(text:Learning%20Coordinator,id:4652),(text:Head%20Of%20Human%20Resources,id:767))),trackingParam:(sessionId:PdtaKVfWRruV+GEoYUSkoA==),doFetchFilters:false,doFetchHits:true,doFetchSpotlights:false)&decorationId=com.linkedin.sales.deco.desktop.search.DecoratedPeopleSearchHitResult-10"

    payload={}
    headers = {
        'authority': 'www.linkedin.com',
        'csrf-token': 'ajax:7378062402392048172',
        'x-restli-protocol-version': '2.0.0',
        'cookie': 'JSESSIONID="ajax:7378062402392048172"; li_at=AQEFAHQBAAAAAATPiAEAAAF5aXbkawAAAXmxkzebVgAAF3VybjpsaTptZW1iZXI6MTg2MzYxOTM5zRb9K2is1fkvlmABnVpfCa7cCBL9wlbwPAvu5aiw1Jy3Dvy3aZeBz_GXyfq04XdviTe_oTFnegEReqca0huARiRRl2Zm2V332-bG5FvTQiLjbg0ghKudsaO28m4Hny1U7avwLo7RmApZMmumkb2Ghqp_OM234OGz5Iia1dOh862wQ4VPHyUvliv-CL4ZNkay6N3Kdg; li_a=AQJ2PTEmc2FsZXNfY2lkPTg0NDMwMjUwNyUzQSUzQTIzNDM2NjQwN7SMdY29EUr4g3di19h1JbakJ77-; bcookie="v=2&136c6eda-a9af-4849-8b93-ff35a892189b"; lidc="b=OB39:s=O:r=O:a=O:p=O:g=2977:u=160:i=1622073697:t=1622155743:v=2:sig=AQGaIeP92Bp1Y2nVgflXmXSGaP-JWMPB"; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; bscookie="v=1&20210526235455cba7a926-c051-418f-873b-4f40f7443ec8AQFGI_1uRfiKt82LEJ1aOuvFfpqtUVvB"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = response.json()
    results = json_data["elements"]

    # figuring out total search results
    global total_results
    if total_results == -1:
        # not defined yet, grab it from the json data and update global variable
        total_results = json_data["paging"]["total"]

    all_leads = []

    for candidate in results:
        fetch_functions.process_candidate(candidate, all_leads, cursor)

    # page done - ask if user wants to keep looking at next pages
    keep_going = input("keep searching? (Y/N): ")
    if keep_going == "N":
        connection.commit()
        connection.close()
        sys.exit()

if __name__ == "__main__":
    delete_db = input("Delete previous db and proceed with search? (Y/N): ")
    if delete_db == "N":
        print("Quitting...")
        sys.exit()

    # delete existing db if there
    if os.path.exists("leads.db"):
        os.remove("leads.db")
        print("Previous database removed")
    else:
        print("No previous database found, proceeding...")

    # initialise db
    connection = sqlite3.connect('leads.db')
    # create tables
    cursor = connection.cursor()
    cursor.execute(helper.CREATE_USERS_TABLE)
    cursor.execute(helper.CREATE_CONNECTIONS_TABLE)

    # counts total number of search results
    global total_results
    total_results = -1
    # which index the page starts at
    start = 0
    # count is the number of results per page - capped at 100
    count = 100
    curr_last = start + count
    while curr_last < total_results + count or total_results == -1:
        get_page(start, count, cursor, connection)
        start += count

    # close db connection
    connection.commit()
    connection.close()