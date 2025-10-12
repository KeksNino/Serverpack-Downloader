import requests
import os
from dotenv import load_dotenv
import inquirer
import zipfile

load_dotenv()

headers = {
    'x-api-key': os.getenv("CURSEFORGE_API_KEY")
}



modpack_names = []
found = False
selected_modpack_id = -1


def search_modpacks(query):
    global data
    global found

    response = requests.get(f'https://api.curseforge.com/v1/mods/search?gameId=432&searchFilter={query}', headers=headers)
    data = response.json()
    for mod in data['data']:
        modpack_url = mod['links']['websiteUrl']
        if modpack_url.startswith("https://www.curseforge.com/minecraft/modpacks/"):
            modpack_names.append(mod['name'])
            found = True
    if not found:
        print("No modpack found with that name.")

    return modpack_names


def select_modpacks(modpack_names):

    if found == True:
        questions = [
        inquirer.List('name',
            message="Select a modpack",
            choices=modpack_names
        ),
    ]

    answers = inquirer.prompt(questions)


    selected_modpack_name = answers['name']
    for mod in data['data']:
        if mod['name'] == selected_modpack_name:
            selected_modpack_id = mod['id']

    return selected_modpack_name, selected_modpack_id



def download_modpack(selected_modpack_name, selected_modpack_id):

    r = requests.get(f"https://api.curseforge.com/v1/mods/{selected_modpack_id}/files", headers = headers)
    file_data = r.json()
    for file in file_data['data']:
        server_file_id = file['serverPackFileId']
        file = requests.get(f"https://www.api.curseforge.com/v1/mods/{selected_modpack_id}/files/{server_file_id}", headers=headers)
        download_url = file.json()['data']['downloadUrl']
        print(f"Download Url: {download_url}")
        
        dl_response = requests.get(download_url, stream=True)
        with open(f"{selected_modpack_name}-server.zip", 'wb') as f:
            for chunk in dl_response.iter_content(chunk_size=8192):
                f.write(chunk)

        with zipfile.ZipFile(f"{selected_modpack_name}-server.zip", 'r') as zip_ref:
            zip_ref.extractall(f"{selected_modpack_name}-server")
        os.remove(f"{selected_modpack_name}-server.zip")
        break
    else:
        print("No server pack found for this modpack.")


if __name__ == "__main__":
    print("Serverpack Downloader")

    query = input("Enter Search Query: ")
    modpack_names = search_modpacks(query)

    selected_modpack_name, selected_modpack_id = select_modpacks(modpack_names)

    download_modpack(selected_modpack_name, selected_modpack_id)


