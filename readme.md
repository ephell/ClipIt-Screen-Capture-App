<p align="center">
    <img src="https://i.imgur.com/9eWc6ZZ.jpg" alt="ClipIt-Banner">
</p>

# 🎥 ClipIt - Screen Capture App
ClipIt is an application that simplifies the creation of short video clips. Recording is initiated when an area is selected and an option to generate an .mp4 file is given upon stopping. Additionally, the built-in editor allows for trimming the video's length, cropping its resolution, and adjusting the volume.

## Features
- Easy to use GUI.
- Record or screenshot a custom area of the screen.
- Record speaker audio along with the video.
- Edit video length, resolution and volume using the built-in editor.
- Hotkey support for quick recording or screenshotting.
- Accessible via system tray.

<p align="center">
  <img src="https://i.imgur.com/IV5La5Q.jpg" alt="GUI-Interfaces">
</p>

## Video Recording Demo
<p align="center">
  <img src="https://i.imgur.com/dPVCuxm.gif" alt="Video-Recording-Demo-GIF">
</p>

## Additional Information
- One minute of recording at 1080p resolution generates a file between 15-30 MB in size.
- Recording is limited to 30 FPS.
- Application's demanding CPU usage may result in laggy videos, particularly on systems with lower specifications. Performance tests for a 1-minute 1080p recording:
  - Windows 10 64-bit VMWare VM (4-cores) averaged 10-11 FPS.
  - Windows 11 64-bit PC (8-cores): maintained stable 30 FPS.

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
