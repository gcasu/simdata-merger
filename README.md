# simdata-merger
The tool aims to speed up the process of modding the infamous simdata.simjson file, simply by merging the original file with a lighter, more readable diff file.

## Requirements
- To run the script you need a Python Interpreter installed on your computer: https://www.python.org/downloads
- CryBarEditor is also needed for extracting simdata.simjson file from AoM: Retold assets: https://github.com/CryShana/CryBarEditor

## Installation
1. Extract simdata.simjson file from the game assets with CryBarEditor. The file is located in the data/Data.bar archive. Once extracted, the expected file path will be {YOUR_AOM_RETOLD_PATH}/{YOUR_STEAM_ID}/mods/local/{YOUR_MOD_NAME}/game/data/gameplay
2. Rename the file to simdata.json
3. Copy the following files in the same folder of simdata.json: simmods.json, simdata_merger.py, requirements.txt
4. Open a command prompt and install the script requirements with the following command `pip install -r requirements.txt --user`
5. Run the script with the following command `python simdata_merger.py`

## Usage
- As long as the script is running, it will detect changes made to the simmods.json file and merge them with the simdata.json file into a new simdata.simjson file.
- You can use simdata.json as a readonly source, and simmods.json as an additive file for your modded entries. The script will then do the magic by creating a fresh simdata.simjson file each time you modify the diff file.

## Warnings
- If you had already modified simdata.simjson file before, please be sure to backup you changes into simmods.json before running the script, otherwise they will be overwritten.
- In case a new AoM: Retold patch is released, you will probably need to extract again simdata.simjson from the game assets and rename it to simdata.json.

Enjoy!
