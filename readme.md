<p align="center">
    <img src="https://i.imgur.com/9eWc6ZZ.jpg" alt="ClipIt-Banner">
</p>

# 🎥 ClipIt - Screen Capture App
ClipIt is a user-friendly application designed to simplify the process of recording short videos. You can effortlessly start recording a custom area of your screen and ClipIt will generate a video file as soon as you stop. At that point the file is ready to be shared. If you're not satisfied with the result you also have the option to trim the length, crop the resolution, or adjust the volume of the video using the built-in editor.

## Features
- Easy to use GUI.
- Record or screenshot a custom area of the screen.
- Record speaker and/or microphone audio along with the video.
- Edit video length, resolution and volume using the built-in editor.
- Configure custom hotkeys for quick recording or screenshot.
- Access the application via the system tray.

<p align="center">
  <img src="https://i.imgur.com/05mJa53.jpg" alt="GUI-Interfaces">
</p>

## Video Recording Demo
<p align="center">
  <img src="https://i.imgur.com/dPVCuxm.gif" alt="Video-Recording-Demo-GIF">
</p>

## Installation

##### Method 1 - Setup.exe (easiest)
- Download the setup.exe from 'Releases'.
- Install.
- Run the app's executable generated after the setup has finished.

##### Method 2 - Poetry
- Download and install Python 3.11.3.
- Clone the repository: `git clone [repository URL]`
- Navigate to the cloned directory via the terminal: `cd [cloned directory path]`
- Install Poetry: `pip install poetry`
- Run the following command to instruct Poetry to create virtual environments in the project's directory: `poetry config virtualenvs.in-project true`
- Create a virtual environment: `poetry env use [path-to-python-3.11-3.exe]`
- Activate the virtual environment:
  - bash: `source .venv/Scripts/activate`
  - shell: `.\.venv\Scripts\activate`
- Install project's dependencies: `poetry install`
- Start the application: `python main.py`

##### Method 3 - venv + requirements.txt
- Download and install Python 3.11.3.
- Clone the repository: `git clone [repository URL]`
- Navigate to the cloned directory via the terminal: `cd [cloned directory path]`
- Create a virtual environment: `py -3.11 -m venv venv`
- Activate the virtual environment:
  - bash: `source venv/Scripts/activate`
  - shell: `.\venv\Scripts\activate`
- Install project's dependencies: `pip install -r requirements.txt`
- Start the application: `python main.py`

## License
[MIT](https://choosealicense.com/licenses/mit/)