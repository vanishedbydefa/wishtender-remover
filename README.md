# Usage
Make sure to use a version of python <=3.11. In case you have multiple versions installed, use the full path to the python executable <=3.11 e.x `C:\Users\exampleuser\folder1\folder2\Programs\Python\Python311\python.exe`

1. Open a commandline
2. Clone the repository `git clone https://github.com/vanishedbydefa/wishtender-remover.git`
3. Move into the repository `cd wishtender-remover`
4. Create a virtual enviroment `python -m venv .venv`
5. Activate the virtual enviroment `.venv\Scripts\activate`
6. Install the requirements `python -m pip install -r requirements.txt`
7. Run the program `python main.py -p <Path/to/the/folder/where/to/find/wishtender/images>`
  * Use `-t <number>` to modify the amount of threads running
  * Use `-d` to delete detected wishtender images

```
usage: Wishtender-Remover [-h] [-p PATH] [-d] [-t THREADS]

Remove all wishtender images in a folder

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the folder in which to find wishtender images
  -d, --delete          Delete found wishtender images
  -t THREADS, --threads THREADS
                        Maximum amount of running threads

https://github.com/vanishedbydefa
```
