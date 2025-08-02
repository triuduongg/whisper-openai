# whisper-openai speech to text
## Install:
### Python: https://www.python.org/downloads/
#### Remember to select "Add python.exe to PATH" before installing
### ffmpeg: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip
#### unzip the file, add the path ...\ffmpeg-master-latest-win64-gpl-shared\bin to the environment variable
### Install libraries
#### use terminal cmd or powershell
##### pip: 
`
python -m pip install --upgrade pip
`
##### openai-whisper: ` python -m pip install openai-whisper `
##### ffmpeg-python: ` python -m pip install ffmpeg-python `
##### pyinstaller: ` python -m pip install pyinstaller `
### Install main app
#### main.py: https://github.com/triuduongg/whisper-openai/blob/main/main.py
#### use terminal cmd or powershell
##### main.exe: ` python -m PyInstaller main.py `
### After installation is complete, the main.exe application is located in the ...\dist\main folder and from next time just run it.
## Guide:
### Open main.exe
### Copy the folder path containing the audio files and paste it into the first parameter
### Select the model you want by entering the corresponding number
### Select the output file format you want by entering the corresponding number
### Copy the path for the output files and paste it into the last parameter
## After that just wait for the results
## Note that the warning ":132: UserWarning: FP16 is not supported on CPU; using FP32 instead warnings.warn("FP16 is not supported on CPU; using FP32 instead")" does not affect the conversion process
## Good luck!




