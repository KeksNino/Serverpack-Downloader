import requests
import os
from dotenv import load_dotenv
import inquirer

load_dotenv()

headers = {
    'x-api-key': os.getenv("CURSEFORGE_API_KEY")
}

input_name = input("Enter modpack name: ")
response = requests.get(f'https://api.curseforge.com/v1/mods/search?gameId=432&searchFilter={input_name}', headers=headers)
data = response.json()

modpack_name = {}
modpack_id = {}
url_dict = {}
found = False

modpack_names = []
for mod in data['data']:
    modpack_url = mod['links']['websiteUrl']
    if modpack_url.startswith("https://www.curseforge.com/minecraft/modpacks/"):
        modpack_names.append(mod['name'])
        # modpack_id = mod['id']
        # modpack_name = mod['name']
        # url_dict[mod['links']['websiteUrl']] = modpack_url + str(modpack_id) + modpack_name
        # modpack = f"{modpack_name} {modpack_id} {url_dict}"
        found = True
    else:
        pass

if not found:
    print("No modpack found with that name.")
else:
    pass

questions = [
    inquirer.List('name',
                  message="Select a modpack",
                  choices=modpack_names,
            ),
]

answers = inquirer.prompt(questions)

selected_modpack_id = -1

selected_modpack_name = answers['name']
# get modpack id from selected modpack name
for mod in data['data']:
    if mod['name'] == selected_modpack_name:
        selected_modpack_id = mod['id']
        selected_url = mod['links']['websiteUrl']

print(selected_modpack_id)


r = requests.get(f"https://api.curseforge.com/v1/mods/{selected_modpack_id}/files", headers = headers)
file_data = r.json()
print(file_data)
for file in file_data['data']:
    # server_file = file['isServerPack']
    server_file = file['serverPackFileId']
    print (server_file)
else:
    print("No server pack found for this modpack.")

# if answers is None:
#     print("No selection made.")
# else:
#     selected_url = answers['url']
#     print(f"You selected: {selected_url}")
