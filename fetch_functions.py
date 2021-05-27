import requests
import helper

# given the profile ID of a LinkedIn user, returns their mutual connections
# TODO: ask if "count" in sharedConnectionsHighlight is actually the amount of shared connections
def get_connections(profile_id, num_connections, user_obj, cursor):
    url = f"https://www.linkedin.com/sales-api/salesApiWarmIntro?q=warmIntro&warmIntroSpotlightType=SHARED_CONNECTION&doSpotlightCount=false&profileAuthKey=(profileId:{profile_id},authType:NAME_SEARCH,authToken:BvvX)&count={num_connections}"

    payload={}
    headers = {
        'authority': 'www.linkedin.com',
        'csrf-token': 'ajax:7378062402392048172',
        'x-restli-protocol-version': '2.0.0',
        'cookie': 'JSESSIONID="ajax:7378062402392048172"; li_at=AQEFAHQBAAAAAATPiAEAAAF5aXbkawAAAXmxkzebVgAAF3VybjpsaTptZW1iZXI6MTg2MzYxOTM5zRb9K2is1fkvlmABnVpfCa7cCBL9wlbwPAvu5aiw1Jy3Dvy3aZeBz_GXyfq04XdviTe_oTFnegEReqca0huARiRRl2Zm2V332-bG5FvTQiLjbg0ghKudsaO28m4Hny1U7avwLo7RmApZMmumkb2Ghqp_OM234OGz5Iia1dOh862wQ4VPHyUvliv-CL4ZNkay6N3Kdg; li_a=AQJ2PTEmc2FsZXNfY2lkPTg0NDMwMjUwNyUzQSUzQTIzNDM2NjQwN7SMdY29EUr4g3di19h1JbakJ77-;  ; bcookie="v=2&136c6eda-a9af-4849-8b93-ff35a892189b"; lidc="b=OB39:s=O:r=O:a=O:p=O:g=2977:u=160:i=1622077234:t=1622155743:v=2:sig=AQFo0DbkUvipGAOTTtfoDAYtWMJAZUF8"; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; bscookie="v=1&2021052700584379b1e778-84bc-4522-87c0-eea54b2831f6AQEtHTRxA9VyuFq-PSlPjRDnSaO8uQRk"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = response.json()
    results = json_data["elements"]

    user_obj["mutuals_list"] = []
    user_obj["mutuals_count"] = 0

    for candidate in results:
        user_obj["mutuals_count"] += 1
        last_name = candidate["fullName"].split(" ")
        last_name.pop(0)

        mutual_obj = {
            "id": candidate["memberUrn"].split(":")[3],
            "first_name": candidate["firstName"],
            "last_name": helper.listToString(last_name), # lastName is not a field in the JSON object returned by LinkedIn
            "position": get_current_position_mutual(candidate)
        }
        user_obj["mutuals_list"].append(candidate["fullName"])

        # add mutual to db if not present already
        cursor.execute(helper.INSERT_NEW_USER, (mutual_obj["id"], mutual_obj["first_name"], mutual_obj["last_name"], mutual_obj["position"]["title"], mutual_obj["position"]["company_name"]))
        # adds connection to potential lead
        cursor.execute(helper.INSERT_NEW_CONNECTION, (profile_id, mutual_obj["id"]))

    return user_obj

# functions that process the JSON data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# processes a candidate from the search page
def process_candidate(candidate, all_leads, cursor):
    connectionsKey = "sharedConnectionsHighlight"
    num_connections = 0
    if (connectionsKey in candidate):
        num_connections = int(candidate[connectionsKey]["count"])
    profile_id = candidate["objectUrn"].split(":")[3]
    
    user_obj = {
        "first_name": candidate["firstName"],
        "last_name": candidate["lastName"],
        "current_positions": get_current_positions(candidate)
    }

    all_leads.append(get_connections(profile_id, num_connections, user_obj, cursor))

    # add to sqlite db
    cursor.execute(helper.INSERT_NEW_USER, (profile_id, user_obj["first_name"], user_obj["last_name"], user_obj["current_positions"][0]["title"], user_obj["current_positions"][0]["company_name"]))

    print("\ncandidate processed...\n")

# extracts the current positions of a user given their user object
def get_current_positions(candidate):
    current_positions = []
    for i in candidate["currentPositions"]:
        info = {}
        info["company_name"] = i["companyName"]
        info["title"] = i["title"]
        current_positions.append(info)

    return current_positions

# extracts the current positions of a mutual connection given their user object
def get_current_position_mutual(candidate):
    matched_pos = candidate["matchedPosition"]
    
    info = {}
    info["company_name"] = matched_pos["companyName"]
    info["title"] = matched_pos["title"]

    return info