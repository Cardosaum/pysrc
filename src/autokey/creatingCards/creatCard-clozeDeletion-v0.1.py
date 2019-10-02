#!/usr/bin/env python3
#
#
# Writen by Matheus Cardoso, 2019/07/16
#
#
### USER CONFIGURATION ###
#
#
browser = 'Mozilla Firefox' # If you use another browser, change this variable.
#
delete_all_text_before = True # If False, the script will delete all previous data in the fields 'Text' and 'Extra'
#
always_select_note_type = True # if False, the script will NOT verify if <Note Type> note type is selected
#
note_type = 'Cloze' # Change the name of note type if you wish.
#
anki_profile_name = 'study' # Change this variable to correspond your actual Profile Name (NOTE: remember that <Profile_Name> is case sensitive. So, if your profile is 'EXAMPLE' and you typed 'example', the script will not work)
#
time_to_wait_long = 1   # These three variables correspond to the time that script will hold on until execute next command
#
time_to_wait_medium = 0.3
#
time_to_wait_short = 0.1
#
#
### That's is, end of user configuration :) ###



from pyautogui import hotkey, press, alert, typewrite
import pyperclip
from os import popen
from time import sleep

def delete_field_data_before():
    if delete_all_text_before == True:
        hotkey('ctrl', 'a')
        sleep(time_to_wait_short)
        press('backspace')
        sleep(time_to_wait_short)

def add_text_to_card():
    sleep(time_to_wait_medium)
    hotkey('ctrl', 'shift', 't')
    sleep(time_to_wait_short)
    hotkey('shift', 'tab')
    sleep(time_to_wait_short)
    delete_field_data_before()
    hotkey('ctrl', 'v')
    sleep(time_to_wait_short)
    hotkey('shift', 'tab')
    pyperclip.copy(highlighted_text)
    sleep(time_to_wait_short)
    delete_field_data_before()
    hotkey('ctrl', 'v')

def copy_url():
    popen('xdotool windowactivate {}'.format(browser_id)) # activate browser window
    sleep(time_to_wait_medium)
    hotkey('alt', 'd') # select address bar
    hotkey('ctrl', 'c') # copy url

def select_note_type(): # will change any current note type to <note_type> defined by user
    if always_select_note_type is True:
            sleep(time_to_wait_medium)
            hotkey('ctrl', 'n')
            sleep(time_to_wait_short)
            typewrite(note_type)
            sleep(time_to_wait_short)
            press('enter')

anki_add = 'Add'


# clipboard = pyperclip.copy('') # empties your clipboard

highlighted_text = popen('xsel').read() # get selected text

all_windows_active = popen("xdotool search --all --onlyvisible --desktop $(xprop -notype -root _NET_CURRENT_DESKTOP | cut -c 24-) ''").read().split() # get id of all active windows and creat an list with it

all_windows_names = [] # empty list

anki_add_window_open = False

anki_main_window_id = ''

anki_main_window_name = ''

browser_id = ''

browser_name = ''

for window in all_windows_active:
    window_name = popen('xdotool getwindowname "{}"'.format(window)).read().replace('\n','')
    all_windows_names.append(window_name) # append the name of all active windows


    if 'Add' == window_name: # check if Add window of Anki is already open
        anki_add_window_open = True
        anki_add_window_id = window

    if str('Anki - ' + anki_profile_name) == window_name: # get Anki main window's ID and Name
        anki_main_window_id = window
        anki_main_window_name = window_name

    if browser.lower() in window_name.lower():
        browser_id = window
        browser_name = window_name

if (browser_name != '') and (anki_main_window_name != ''): # if firefox and anki are open, copy url
    copy_url()



if anki_add_window_open == False: # if Add window is closed, open it
    if anki_main_window_id != '':
        popen('xdotool windowactivate {}'.format(anki_main_window_id)) # activate Anki main and open Add window
        sleep(time_to_wait_medium)
        press('a')
        select_note_type()
        add_text_to_card()
    else:
        alert(title="Error - Anki is closed!", text='No one running instance of Anki was found.\nPlease, open Anki before try to add any card.', button='OK') # Alert message if Anki is closed

else:
    popen('xdotool windowactivate {}'.format(anki_add_window_id)) # activate Anki Add window
    select_note_type()
    add_text_to_card()
