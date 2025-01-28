# Setup
1) Open up a terminal. Terminal > New Terminal
2) Create a virtual environment by typing this into the terminal: ```py -m venv venv```
3) Activate the virtual environment: ```.\venv\Scripts\activate```
4) Install other packages: ```pip install pywin32 tkfilebrowser```

# Running Script
1) In terminal type: ```py main.py```
    - Add -fd if you are working with folders that have the missed and dropped pick columns in pick execution
    - Add -nd if you are working with folders on the network drive (have to select folders one at a time)
2) The terminal will prompt you for a file name: E.g. bottles
3) A window will pop up to let you choose the saving location of your output csv file
4) A window will pop up to let you select multiple folders

# Clipping Videos
## Dependencies
Install moviepy if it hasn't already been: ```pip install moviepy```


## How To Run
1) In terminal type: ```py clip_timestamps.py```
2) Select video
3) Select the timestamp text file
4) Select the folder to save clips in

## Notes
You can adjust total clip times inside clip_timestamps.py with the VIDEO_CLIP_TIME_S variable
