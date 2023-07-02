# Welcome to YATP!

#### DOWLOAD AT: https://github.com/0xleft/YATP/raw/main/dist/YATP.exe

This codebase is very messy and was made as a demo.

# Running
1st way: `run the main.exe` in `dist` folder if you want to run the compiled application

2nd way: `python main.py` if you want to run without compiled version

# Compiling

the .exe was compiled using the following command
```
pyinstaller main.py --add-data "bottle.py;bottle" --add-data "venv\lib\site-packages\eel\eel.js;eel" --add-data "web;web" --onefile --noconsole -n YATP
```

this will not for you since you need to change the paths to your own

(a icon was added but it is unnecessary)