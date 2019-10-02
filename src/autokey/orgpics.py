import sys
import os
import subprocess


def mcsMove():
    pwd = os.getcwd()
    files = os.listdir(pwd)
    for f in files:
        filePathOld = os.path.abspath(f)
        filePathNew = filePathOld.replace(
            'pendingFlashcards', 'createdFlashcards')
        pathDirectory = filePathNew.split('/')
        del pathDirectory[-1]
        pathDirectory = '/'.join(pathDirectory)

        if os.path.exists(pathDirectory):
            os.rename(filePathOld, filePathNew)
        else:
            os.makedirs(pathDirectory)
            os.rename(filePathOld, filePathNew)
    rmOrgPy = str(pathDirectory + '/orgpics.py')
    os.remove(rmOrgPy)


# def mcsRemoveEmptyDirs():
#     pwd = os.getcwd()
#     os.chdir(pwd)
#     subprocess.run(['find', '.', '-empty', '-type', 'd', '-delete'])


mcsMove()
