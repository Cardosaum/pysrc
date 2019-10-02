import pyperclip
import pyautogui
import os
import time

# CONFIGURATION

anki_profile_name = 'study'

# Verify if anki and gthumb are open


allActiveWindowsIDs = os.popen("xdotool search --all --onlyvisible --desktop $(xprop -notype -root _NET_CURRENT_DESKTOP | cut -c 24-) ''").read().split()   # get a list of all active windows (Only the ID of them)
allActiveWindowsNames = []
ankiAddWindow = ''
ankiImageOcclusionWindow = ''
gThumbWindow = ''

for windowID in allActiveWindowsIDs:
    print(windowID)
    windowName = os.popen(f'xdotool getwindowname "{windowID}"').read().replace('\n','')    # get the name of all windowIDs
    print(windowName)
    allActiveWindowsNames.append(windowName)

    if windowName == 'gThumb':
        gThumbWindow = windowID
    if windowName == (anki_profile_name + ' - Anki'):
        ankiWindow = windowID
    if windowName == 'Add':
        ankiAddWindow = windowID
    if windowName == 'Image Occlusion Enhanced - Add Mode':
        ankiImageOcclusionWindow = windowID

activeWindow = os.popen('xdotool getactivewindow').read().replace('\n','')

if ankiAddWindow:
    if gThumbWindow:

        while activeWindow != gThumbWindow:
            os.popen(f'xdotool windowactivate --sync {gThumbWindow}')
            time.sleep(0.02)
            activeWindow = os.popen('xdotool getactivewindow').read().replace('\n','')

        width, height = pyautogui.size()
        pyautogui.mouseDown(button='right', x=int(width/2), y=int(height/2))
        pyautogui.mouseUp(button='right', x=int((width/2)+70), y=int((height/2)+140))
        # TODO: Open Image Occlusion on Anki

        if not ankiImageOcclusionWindow:
            while activeWindow != ankiAddWindow:
                os.popen(f'xdotool windowactivate --sync {ankiAddWindow}')
                time.sleep(0.02)
                activeWindow = os.popen('xdotool getactivewindow').read().replace('\n','')
                pyautogui.hotkey('ctrl', 'shift', 'o')
                while activeWindow != ankiImageOcclusionWindow:
                    os.popen(f'xdotool windowactivate --sync {ankiImageOcclusionWindow}')
                    time.sleep(0.02)
                    activeWindow = os.popen('xdotool getactivewindow').read().replace('\n','')
                    print('IC opend')





    else:
        pyautogui.alert(title='ERROR - gThumbToImageOcclusion', text='"gThumb" window isn\'t open.\n\nPlease, open it firt.', button='Ok!')


else:

    pyautogui.alert(title='ERROR - gThumbToImageOcclusion', text='"Add" window isn\'t open.\n\nPlease, open it firt.', button='Ok!')



# TODO: Fit image on window and select 'r' for retangle occlusion
