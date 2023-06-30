# Welcome to YATP!

# Running
1st way: `run the main.exe` in `output` folder if you want to run the compiled application

2nd way: `python main.py` if you want to run without compiled version

# Compiling

### MAKE SURE TO INSTALL
```pip install git+https://github.com/0xleft/PPGL.git```

the .exe was compiled using the following command
```
pyinstaller --noconfirm --onefile --windowed --icon "assets/maxresdefault-2512841701.ico" --add-data "./core;core/" "./main.py" -n YATP
```

this will not for you since you need to change the paths to your own

(a icon was added but it is unnecessary)

# Usage

1. Read the instructions
2. Open a folder where all the images are and select it
3. Now you can quickly convert them to the maximum size of 800 pixels or any dimension
4. Write comments for each image in the input field at the top of the window (its the white part)
5. You can preview images by clicking on them to see them in greater detail
6. You can preview how the table will look like by clicking on the "Preview" button
7. You can save the table by clicking on the "Save" button it will save it to the folder that the images are at (if you selected the smaller folder the images)

