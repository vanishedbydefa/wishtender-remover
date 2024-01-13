# Usage(Windows only)
Make sure to use a version of python <=3.11

1. Open a commandline
2. Clone the repository `git clone https://github.com/vanishedbydefa/wishtender-remover.git`
3. Move into the repository `cd wishtender-remover`
4. Create a virtual enviroment `python -m venv .venv`
5. Activate the virtual enviroment `.venv\Scripts\activate`
6. Install the requirements `python -m pip install -r requirements.txt`
7. Run the program `python main.py -p <Path/to/the/folder/where/to/find/wishtender/images>`
  * Use `-t <number>` to modify the amount of threads running
  * Use `-d` to delete detected wishtender images
