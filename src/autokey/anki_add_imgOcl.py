#!/usr/bin/env python3
import pyperclip
import pyautogui
from os import popen, system, chdir, getcwd
from os.path import expanduser, abspath
from time import sleep
import re
from sys import exit
import mcs
### CONFIGURATION ###

anki_profile_name = 'study'

#####################

ankiWindow = ''
addWindow = ''
imgOclWindow = ''
gthumbWindow = ''
gthumb_x = ''
gthumb_y = ''
gthumb_width = ''
gthumb_height = ''
home = expanduser('~')
clipboard = pyperclip.paste()

mcs.normalizePath()
chdir(abspath(f'{getcwd()}/src/autokey/'))

# function to get active window
def activeWindow():
    activeWindow = popen('xdotool getactivewindow getwindowname').read().replace('\n','')
    return activeWindow

# TODO: function to open image occlusion and click on fit
def openImgOcl():
    global imgOclWindow, addWindow
    # if img occlusion is already open, close it first (we must do it in order to open a new instance with our recentrly copies image)
    if imgOclWindow:
        popen(f'wmctrl -ic {imgOclWindow}')
        popen(f'wmctrl -ia {addWindow}')
        while True:
            try:
                pyautogui.locateOnScreen(f'imgtlf/2019-07-26_12-13-24_1564154004_flameshot.png', grayscale=True)
                break
            except:
                sleep(0.2)
                continue
        pyautogui.hotkey('ctrl', 'shift', 'o')
        while True:
            try:
                buttFit = pyautogui.center(pyautogui.locateOnScreen(f'imgtlf/2019-07-25_12-08-46_1564067326_flameshot.png', grayscale=True))
                pyautogui.click(buttFit[0], buttFit[1])
                break
            except:
                pass
            try:
                buttFit = pyautogui.center(pyautogui.locateOnScreen(f'imgtlf/2019-07-25_13-38-16_1564072696_flameshot.png', grayscale=True))
                pyautogui.click(buttFit[0], buttFit[1])
                break
            except:
                pass
            sleep(0.2)
        getWindows = popen('wmctrl -lG').read()
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

        for line in windowRegex.findall(getWindows):
            if line[8] == f'{anki_profile_name} - Anki':
                ankiWindow = line[1]
            if line[8] == 'Add':
                addWindow = line[1]
            if line[8] == 'Image Occlusion Enhanced - Add Mode':
                imgOclWindow = line[1]
            if line[8] == 'gThumb':
                gthumbWindow = line[1]
                gthumb_x = int(line[3])
                gthumb_y = int(line[4])
                gthumb_width = int(line[5])
                gthumb_height = int(line[6])

        popen(f'wmctrl -ir {imgOclWindow} -b add,maximized_vert,maximized_horz')
        sleep(0.1)
        pyautogui.press('f')
        pyautogui.press('r')
    # if img occlusion is not open, open it and select fit
    else:
        popen(f'wmctrl -ia {addWindow}')
        while True:
            try:
                pyautogui.locateOnScreen(f'imgtlf/2019-07-26_12-13-24_1564154004_flameshot.png', grayscale=True)
                break
            except:
                sleep(0.2)
                continue
        pyautogui.hotkey('ctrl', 'shift', 'o')
        while True:
            try:
                buttFit = pyautogui.center(pyautogui.locateOnScreen(f'imgtlf/2019-07-25_12-08-46_1564067326_flameshot.png', grayscale=True))
                pyautogui.click(buttFit[0], buttFit[1])
                break
            except:
                pass
            try:
                buttFit = pyautogui.center(pyautogui.locateOnScreen(f'imgtlf/2019-07-25_13-38-16_1564072696_flameshot.png', grayscale=True))
                pyautogui.click(buttFit[0], buttFit[1])
                break
            except:
                pass
            sleep(0.2)
        getWindows = popen('wmctrl -lG').read()
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

        for line in windowRegex.findall(getWindows):
            if line[8] == f'{anki_profile_name} - Anki':
                ankiWindow = line[1]
            if line[8] == 'Add':
                addWindow = line[1]
            if line[8] == 'Image Occlusion Enhanced - Add Mode':
                imgOclWindow = line[1]
            if line[8] == 'gThumb':
                gthumbWindow = line[1]
                gthumb_x = int(line[3])
                gthumb_y = int(line[4])
                gthumb_width = int(line[5])
                gthumb_height = int(line[6])

        popen(f'wmctrl -ir {imgOclWindow} -b add,maximized_vert,maximized_horz')
        sleep(0.1)
        pyautogui.press('f')
        pyautogui.press('r')


# function to copy gThumb img to clipboard, restoring previus clipboard after that

def gthumCopyImage():
    pressMouseIn = (int(gthumb_width/2), int((gthumb_height/2)-(gthumb_height*0.3)))
    pyautogui.moveTo((gthumb_x+pressMouseIn[0], gthumb_y+pressMouseIn[1]))
    pyautogui.rightClick()
    # while True:
    #     try:
    #         buttCopy = pyautogui.center(pyautogui.locateOnScreen(f'imgtlf/2019-07-26_11-18-58_1564150738_flameshot.png', grayscale=True))
    #         break
    #     except:
    #         sleep(0.2)
    #         continue
    pyautogui.click(((gthumb_x+pressMouseIn[0]+40), (gthumb_y+pressMouseIn[1]+122)))

# Verify if anki and gthumb are open


getWindows = popen('wmctrl -lG').read()
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

for line in windowRegex.findall(getWindows):
    if line[8] == f'{anki_profile_name} - Anki':
        ankiWindow = line[1]
    if line[8] == 'Add':
        addWindow = line[1]
    if line[8] == 'Image Occlusion Enhanced - Add Mode':
        imgOclWindow = line[1]
    if line[8] == 'gThumb':
        gthumbWindow = line[1]
        gthumb_x = int(line[3])
        gthumb_y = int(line[4])
        gthumb_width = int(line[5])
        gthumb_height = int(line[6])

# TODO: copy image from gthumb

# Only execute if current window is 'Anki - Add' or 'gThumb'

if gthumbWindow:
    if addWindow:
        if activeWindow() == 'gThumb':
            # copy img to clipboard
            gthumCopyImage()
            # open img occlusion and click on fit
            openImgOcl()
        elif activeWindow() == 'Add':
            # change to gthumb and copy img to clipboard
            popen(f'wmctrl -ia {gthumbWindow}')
            while True:
                try:
                    pyautogui.locateOnScreen(f'imgtlf/2019-07-26_11-52-19_1564152739_flameshot.png', grayscale=True)
                    break
                except:
                    sleep(0.2)
                    continue
            gthumCopyImage()
            # open img occlusion and click on fit
            openImgOcl()
        else:
            pyautogui.alert(title='ERROR: gThumbToImageOcclusion', text="Your current window must be 'Add' or 'gThumb' to execute this shortcut!", button='OK!')
    else:
        pyautogui.alert(title='ERROR: gThumbToImageOcclusion', text="Anki 'Add' window is closed!\nPlease, open it first.", button='OK!')


else:
    pyautogui.alert(title='ERROR: gThumbToImageOcclusion', text='gThumb is closed!\nPlease, open it first.', button='OK!')
exit(0)
