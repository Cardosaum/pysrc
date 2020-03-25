#!/usr/bin/env python3

"""
This script cipy image from gThumb and open ImageOcclusion window
(Intended to work with both Anki and gThumb open)
"""

### CONFIGURATION ###

anki_profile_name = 'study'
anki_dir = './anki'

#####################

from pprint import pprint
import subprocess
import pyautogui
import mcs
import re
import time
import pathlib
import pyperclip
import collections
import os

###################
## Setup variables

# normalize path
mcs.normalizePath()
os.chdir(pathlib.Path.joinpath(pathlib.Path.cwd(), 'src/autokey/'))

# Get previous clipboard content to resetore later
previousClipboard = pyperclip.paste()

# Set absolute paths for variables
anki_dir = pathlib.Path(anki_dir).resolve()
gthumb_dir = pathlib.Path.joinpath(anki_dir, 'add_imgOcl/gthumbWindow')
imgOcl_dir = pathlib.Path.joinpath(anki_dir, 'add_imgOcl/imgOclWindow')
add_dir = pathlib.Path.joinpath(anki_dir, 'add_imgOcl/addWindow')

# Dictionary with window properties
win = collections.defaultdict(dict)
win['home'] = pathlib.Path.home()


###################


def activeWindow():
    """ function to get active window """
    activeWindow = subprocess.getoutput('xdotool getactivewindow getwindowname')
    return activeWindow

def waitWindowRaise(pattern:str):
    """wait until current window have `pattern` on its name"""
    win = re.compile(pattern)
    while True:
        match = win.search(activeWindow())
        if match:
            break
        time.sleep(0.1)
    return True

def getWindows():
    """ get a list of all open windows """
    return subprocess.getoutput('wmctrl -lG')

def parseWindows(windowsList):
    """ Parse result of `getWindows()` function and return wanted windows """

    global win

    windowRegex = re.compile(r'''(
                            ([\w\d]+)       # window id
                            \s+
                            ([\d-]+)        # desktop
                            \s+
                            (\d+)           # x-offset
                            \s+
                            (\d+)           # y-offset
                            \s+
                            (\d+)           # width
                            \s+
                            (\d+)           # height
                            \s+
                            ([\w-]+)        # owner
                            \s+
                            (.+)            # window name
                         )''', re.VERBOSE)

    for window in windowRegex.findall(windowsList):
        # Get window name, window id
        wn = window[8]
        wid = window[1]

        if wn == f"{anki_profile_name} - Anki":
            win['ankiWindow'] = wid

        elif wn == 'Add':
            win['addWindow'] = wid

        elif wn == 'Image Occlusion Enhanced - Add Mode':
            win['imgOclWindow'] = wid
            win['imgOclWindow_x'] = int(window[3])
            win['imgOclWindow_y'] = int(window[4])
            win['imgOclWindow_width'] = int(window[5])
            win['imgOclWindow_height'] = int(window[6])


        elif wn == 'gThumb':
            win['gthumbWindow'] = wid
            win['gthumbWindow_x'] = int(window[3])
            win['gthumbWindow_y'] = int(window[4])
            win['gthumbWindow_width'] = int(window[5])
            win['gthumbWindow_height'] = int(window[6])

    return win

def atualizeWindow():
    return parseWindows(getWindows())

def opengThumb():
    """ open `gThumb` window """

    atualizeWindow()
    assert win['gthumbWindow'], 'gThumb window is closed!'

    subprocess.getoutput(f'wmctrl -ia {win["gthumbWindow"]}')
    ensureOpen('gthumbWindow')



def gThumbCopyImg():
    """ Copy image on gThumb window, using mouse """

    atualizeWindow()

    # Get location where to press mouse button (certifying that is inside gThumb window)
    pressMouseIn = (int(win['gthumbWindow_width']/2), int((win['gthumbWindow_height']/2)-(win['gthumbWindow_height']*0.3)))
    pyautogui.moveTo((win['gthumbWindow_x']+pressMouseIn[0], win['gthumbWindow_y']+pressMouseIn[1]))
    pyautogui.rightClick()
    pyautogui.click(((win['gthumbWindow_x']+pressMouseIn[0]+40), (win['gthumbWindow_y']+pressMouseIn[1]+122)))


def openImgOcl(findOnScreen=False):
    """ Open Image Occlusion window """

    atualizeWindow()

    # TODO: handle img oclusion with mouse click hard coded

    # if img occlusion is already open, close it first (we must do it in order to open a new instance with our previous copied image)
    if win['imgOclWindow']:
        # Close open Image Occlusion Window
        subprocess.getoutput(f'wmctrl -ic {win["imgOclWindow"]}')

    # Activate `Add` window
    subprocess.getoutput(f'wmctrl -ia {win["addWindow"]}')

    # Ensure `Add` window is open and active
    ensureOpen('addWindow')

    # Shortcut to open `Image Occlusion Window`
    pyautogui.hotkey('ctrl', 'shift', 'o')
    ensureOpen('imgOclWindow')

    atualizeWindow()

    # Activate `ImgOcclusion` window
    subprocess.getoutput(f'wmctrl -ia {win["imgOclWindow"]}')
    waitWindowRaise('Image Occlusion Enhanced - Add Mode')

    if findOnScreen:
        findOnScreen(getDirImgs(imgOcl_dir))
        pointer = mouseCenter('imgOclWindow')
        pyautogui.click(pointer)
        pyautogui.press('f')
        pyautogui.press('r')
        pyautogui.moveTo(mouseCenter('imgOclWindow'))

    else:
        from pprint import pprint
        pprint(win)
        mouse_x = win['imgOclWindow_x'] + win['imgOclWindow_width']/2
        mouse_y = win['imgOclWindow_y'] + win['imgOclWindow_height']/2
        print(mouse_x, mouse_y)
        pyautogui.moveTo(mouse_x, mouse_y, 4, pyautogui.easeInBounce)
        pyautogui.click(clicks=5, pause=0.2)
        pyautogui.press('f')
        pyautogui.press('r')



def getDirImgs(directory=anki_dir, ext='png'):
    """ return all images from directory """
    return list(directory.glob(f'*.{ext}'))



def mouseCenter(window):
    """ click in the middle of `window` """

    atualizeWindow()
    mousePosition = ( int((win[f"{window}_x"] + win[f"{window}_width"]) / 2) , int((win[f"{window}_y"] + win[f"{window}_height"]) / 2) )

    return mousePosition


def findOnScreen(imgsList):
    """ try to locate image on screen """

    position = ''
    while not position:
        for img in imgsList:
            img = str(img)
            position = pyautogui.locateOnScreen(img)
            if position:
                break
    return position


def ensureOpen(window):
    """ Ensure `window` window is open and active """

    while not isWindowActive(window):
        time.sleep(0.5)



def isWindowActive(window):
    """ Check if window is currently active """
    atualizeWindow()
    if win[window]:
        return True
    else:
        return False


def logicCheck():
    """ perform logic checks to ensure script can run """

    atualizeWindow()

    assert win['addWindow'], pyautogui.alert(title='Error - Anki Add ImgOcl', text='Window "Add" from Anki must be open!', button='OK')
    assert win['gthumbWindow'], pyautogui.alert(title='Error - Anki Add ImgOcl', text='Window "gThumb" must be open!', button='OK')

def main():
    """ main program flow """


    logicCheck()
    opengThumb()
    gThumbCopyImg()
    openImgOcl()

if __name__ == '__main__':


    main()
