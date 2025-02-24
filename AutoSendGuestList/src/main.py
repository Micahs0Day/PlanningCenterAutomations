import requests
import time
import os
from dotenv import load_dotenv

## ENV Variables
load_dotenv()
APP_ID = os.getenv("APP_ID")
API_TOKEN = os.getenv("API_TOKEN")
LIST_ID = os.getenv("LIST_ID")

###------1-------###

## Run the List to update its results.
update_list = requests.post(f"https://api.planningcenteronline.com/people/v2/lists/{LIST_ID}/run" , auth = (APP_ID, API_TOKEN))

if 200 <= update_list.status_code < 300 :
    ## Success Message
    print("List Updated..\n")

    ## Wait for 5 min while the list updates
    ##time.sleep(300)

    ## Retrieve List results
    list_results = requests.get(f"https://api.planningcenteronline.com/people/v2/lists/{LIST_ID}/list_results?include=person", auth = (APP_ID, API_TOKEN))

    ## Success Message
    if list_results.status_code == 200:
        print("List results retrieved!\n")
    else:
    ## Error Message
        print(f"Result retrieval failed..", "Status Code: {list_results.status_code}")

    ## Retrieve response as JSON
    json_data = list_results.json()

    ## List to store IDs
    person_id_list = []

    ## Parse JSON (Person IDs)
    for obj in json_data['data']:
        data = obj['relationships']['person']['data']['id']
        person_id_list.append(data)
else:
    ## Error Message
        print("Request failed:", update_list.status_code)

###------2-------###
## Retrieve person's full name from id
def get_name_from_id(person_id):
    person_query = requests.get(f"https://api.planningcenteronline.com/people/v2/people?where[id]={person_id}", auth = (APP_ID, API_TOKEN))
    person_result = person_query.json()
    first_name = person_result["data"][0]["attributes"]["first_name"]
    last_name = person_result["data"][0]["attributes"]["last_name"]
    person = f"{first_name} {last_name}"
    return person


###------3-------###
# Remove pre-existing guest list file if it exists
current_directory = os.path.dirname(os.path.realpath(__file__))
guest_list_path = f"{current_directory}/guest_list.txt"

if os.path.exists(guest_list_path):
    os.remove(guest_list_path)

print(guest_list_path)
###------4-------###

## Retrieve notes by IDs
for id in person_id_list:
    person_name = get_name_from_id(id)
    note_data = requests.get(f"https://api.planningcenteronline.com/people/v2/people/{id}/notes", auth = (APP_ID,API_TOKEN))
    note_data = note_data.json()
    try:
        person_note = (note_data['data'][0]['attributes']['note'])
    except:
        person_note = 'N/A'
    finally: 
        print(f"{person_name}\n{person_note}")
        print(f"Entry Added for guest {id} - ({person_name})")
        with open(guest_list_path,"a") as guest_list:
            guest_list.write(f"{person_name}\n{person_note}\n\n")
