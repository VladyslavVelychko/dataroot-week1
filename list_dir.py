import os
def func():
    directory=os.getcwd()
    return os.listdir(directory)
print(func())