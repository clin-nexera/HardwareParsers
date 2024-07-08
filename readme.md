# Setup
1) Open up a terminal. Terminal > New Terminal
2) Create a virtual environment by typing this into the terminal: ```py -m venv venv```
3) Activate the virtual environment: ```.\venv\Scripts\activate```
4) Install nexera packages: ```pip install git+https://github.com/GripperDominationOrg/nexera_packages.git```
5) Install other packages: ```pip install pywin32 tkfilebrowser```

# Running Script
1) In terminal type: ```py main.py```
    - Add -pt if you are working with folders that have the updated pick trigger column in the pick execution csv
    - Add -nd if you are working with folders on the network drive (have to select folders one at a time)
2) The terminal will prompt you for a file name: E.g. bottles
3) A window will pop up to let you choose the saving location of your output csv file
4) A window will pop up to let you select multiple folders
