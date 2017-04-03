import os, webbrowser
from pathlib import Path

url="/index.html"
my_file=Path(url)
if my_file.is_file():
    webbrowser.open("file://"+os.path.realpath(os.getcwd()+url))
else:
    os.system("twistd -no web --path=.")