# Serverpack-Downloader
CLI Downloader to download server packs from CurseForge

# IMPORTANT
Add your own CurseForge API-Key to an .env file
```bash
CURSEFORGE_API_KEY=YOUR_API_KEY
```

You can get your own through https://console.curseforge.com/

# Dependencies
```bash
python-dotenv
inquirer
requests
```

Install with `pip install -r requirements.txt`


# Notes

If you get the following error, the Modpack you're trying to download most likely doesn't have a serverpack.

```bash
Traceback (most recent call last):
  File "Serverpack-Downloader\main.py", line 90, in <module>
    download_modpack(selected_modpack_name, selected_modpack_id)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Serverpack-Downloader\main.py", line 64, in download_modpack
    server_file_id = file['serverPackFileId']
```