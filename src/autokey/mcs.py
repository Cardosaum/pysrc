'''
Custom Scripts made by Matheus
Intended to work with autokey
'''

import datetime, os, shelve, pyautogui, re, csv, time, pyperclip, webbrowser, collections, requests, subprocess, sys, platform, shutil, keyring, json, pathlib





def executeScript(scriptName):
    logFunction(scriptName)
    eval(f'{scriptName}()')

def logFunction(scriptName):
    normalizePath()
    stats = []
    n = datetime.datetime.now()
    computer_name = platform.uname()[1].strip().replace(" ", "-")
    stats.append(n.strftime('%s')) # get time
    stats.append(scriptName) # name of the script
    stats.append(getActiveWindow()) # name of current window
    stats.append(computer_name)
    callsFile = os.path.abspath(os.path.join('..', 'data', f'calls_{computer_name}.csv'))
    with open(callsFile, 'a') as file:
        w = csv.writer(file)
        w.writerow(stats)

def normalizePath():
    os.chdir(os.path.realpath(os.path.abspath(os.path.join(getHome(), 'src'))))

def getPrintPath():
    printPath = data_get('printPath', isFileOrFolder=True, needTostartWithHome=True)
    # printPath = list(filter(None, printPath))
    # homePath = getHome().split(os.path.sep)
    # homePath = list(filter(None, homePath))
    # finalPath = homePath + printPath
    # finalPath = os.path.sep + os.path.sep.join(finalPath)
    return printPath


def getData(key, returnString=True):
    data = shelve.open(os.path.abspath(os.path.join('..', 'data', 'config')))
    dataNeeded = data[key]
    data.close()
    if returnString:
        return str(dataNeeded)
    else:
        return dataNeeded

def data_get(key='', list_keys=True, isFileOrFolder=False, needTostartWithHome=False, isAut=False):
    normalizePath()
    with shelve.open(os.path.abspath(os.path.join('..', 'data', 'config'))) as f:

        if key:
            value = f[key]
            if isAut:
                data = value.split(',')
                data = keyring.get_password(data[0], data[-1])
                return data

            if isFileOrFolder:
                if needTostartWithHome:
                    if value.startswith(getHome()):
                        if os.path.exists(value):
                            pass
                        else:
                            raise LookupError
                    else:
                        value1 = list(filter(None, getHome().split(os.path.sep)))
                        value2 = list(filter(None, value.split(os.path.sep)))
                        value = value1 + value2
                        value = os.path.sep + os.path.sep.join(value)
                    return value
                else:
                    return value
            return value, os.path.sep

        if list_keys:
            return sorted(list(f.items()))

def saveData(key, value):
    normalizePath()
    data = shelve.open(os.path.abspath(os.path.join('..', 'data', 'config')))
    data[key] = value
    dataSaved = data[key]
    data.close()
    return dataSaved

def removeData(key):
    pwd = os.getcwd()
    home = os.path.expanduser('~')
    rootFolderForScripts = data_get('rootFolderForScripts', isFileOrFolder=True, needTostartWithHome=True)
    os.chdir(rootFolderForScripts)
    data = shelve.open(os.path.abspath(os.path.join('..', 'data', 'config')))
    valueRemoved = data[key]
    data.pop(key)
    data.close()
    os.chdir(pwd)
    return valueRemoved



def getListOfWindows():
    windows = os.popen('wmctrl -lG').read().strip('\n')
    windows = windows.splitlines()

    return windows


def getActiveWindow():
    active = os.popen('xdotool getactivewindow getwindowname').read().strip('\n')

    return active


def isWindowActive(pattern):
    isWindowActive = False
    for window in getListOfWindows():
        if pattern in window:
            isWindowActive = True
    return isWindowActive

def getHome():
    home = os.path.expanduser('~')

    return home

def getSelection(cleanString=False, removeCharacters=((), ' ')):
    if cleanString:
        selection = os.popen('xclip -selection primary -o').read().replace('\n', ' ').strip()
        charactersToRemove = ['.',',',':',';','\n','\r','&']
        [selection.replace(character, ' ') for character in charactersToRemove]
    else:
        selection = os.popen('xclip -selection primary -o').read().strip('\n')
    if removeCharacters and cleanString == False:
        for character in removeCharacters[0]:
            selection.replace(character, removeCharacters[1])


    return selection

def getWindowInfo(windowPattern, moreInfo=False, exactMatch=False):
    resultSimple = 0

    windowRegex = re.compile(r'{}'.format(windowPattern))

    if moreInfo:
        specifcRegex = re.compile(r'''(
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
                                        ([A-Za-z/.-]+)        # owner
                                        \s+
                                        (.+)            # window name
                                     )''', re.VERBOSE)

    for window in getListOfWindows():
        matchWindow = re.search(windowRegex, window)

        if matchWindow:
            if resultSimple == 0:
                match = []
                match.append(window)
            if resultSimple > 0:
                match.append(window)

            resultSimple += 1

            if moreInfo:
                if resultSimple == 1:
                    specifc = []
                    matchSpecifc = re.search(specifcRegex, window)
                    groups = matchSpecifc.groups()
                    specifc.append(groups)
                if resultSimple > 1:
                    matchSpecifc = re.search(specifcRegex, window)
                    specifc.append(matchSpecifc.groups())

    if resultSimple == 1:
        if moreInfo and exactMatch == False:
            return [match[0], specifc[0]]
        if moreInfo and exactMatch == True:
            if specifc[0][8] == windowPattern:
                return [match[0], specifc[0]]
            else:
                return False
        else:
            return match[0]
    if resultSimple > 1:
        if moreInfo:
            return [match, specifc]
        else:
            return match


def windowExist(pattern):
    window = getWindowInfo(pattern, moreInfo=True)
    if window:
        return True
    else:
        return False


def activateWindow(windowPattern):
    window = getWindowInfo(windowPattern, moreInfo=True)
    subprocess.run(f'wmctrl -ia {window[1][1]}', shell=True)

### deprecated ###
def gthumbCopyAndPaste(typeOfCopy='removePrevious', usemouse=True, numberOfField=1):

    if getActiveWindow() == 'gThumb':
        pyautogui.PAUSE = 0.1
        addInfo = getWindowInfo('Add', moreInfo=True, exactMatch=True)
        if 'Add' in addInfo:
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            activateWindow('Add')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'shift', 't')
            if not usemouse:
                for f in range(12):
                    pyautogui.hotkey('tab')
                    # sleep(0.1)
            else:
                for f in range(2):
                    pyautogui.hotkey('shift', 'tab')
                mouse_x = addInfo[1][3] + 100
                mouse_y = addInfo[1][4] + 100
                pyautogui.scroll(50)
                pyautogui.click(x=mouse_x, y=mouse_y)
                if numberOfField > 1:
                    for f in range(numberOfField-1):
                        pyautogui.hotkey('tab')

            if typeOfCopy == 'removePrevious':
                pyautogui.hotkey('ctrl', 'end')
                pyautogui.press('backspace')
            if typeOfCopy == 'removeAll':
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('a')
                pyautogui.press('backspace')
            if typeOfCopy == 'onlyPaste':
                pyautogui.hotkey('ctrl', 'end')
                pyautogui.hotkey('ctrl', 'end')
                pyautogui.hotkey('ctrl', 'end')
                pyautogui.hotkey('ctrl', 'end')

            # sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            for f in range(2):
                pyautogui.hotkey('shift', 'tab')
                # sleep(0.1)
            pyautogui.hotkey('pageup')
            pyautogui.hotkey('pageup')
            pyautogui.hotkey('pageup')
            pyautogui.hotkey('end')
        else:
            pyautogui.alert(title='Anki ERROR', text="'Add' is closed!\nPlease, open it first.", button='OK!')
            sys.exit()
    else:
        sys.exit()


   

def gthumbCopyImageWithMouse():
    if getActiveWindow() == 'gThumb':
        pass
    else:
        try:
            activateWindow('gThumb')
        except:
            print('ERROR: gThumb is not active window')
            raise NameError

    pyPause = pyautogui.PAUSE
    pyautogui.PAUSE = 0.3
    gthumbWindowInfo = getWindowInfo('gThumb', moreInfo=True)
    gthumb_x = float(gthumbWindowInfo[1][3])
    gthumb_y = float(gthumbWindowInfo[1][4])
    gthumb_width = float(gthumbWindowInfo[1][5])
    gthumb_height = float(gthumbWindowInfo[1][6])

    pressMouseIn = (int(gthumb_width/2), int((gthumb_height/2)-(gthumb_height*0.3)))
    pyautogui.moveTo((gthumb_x+pressMouseIn[0], gthumb_y+pressMouseIn[1]))
    pyautogui.rightClick()
    pyautogui.click(((gthumb_x+pressMouseIn[0]+40), (gthumb_y+pressMouseIn[1]+122)))
    pyautogui.PAUSE = pyPause


def gthumbCopyImageWithKeyboard(manipulateCopy=False, restoreClipboard=True, onlyBasename=False):
    if restoreClipboard:
        oldClipboard = pyperclip.paste()
    if getActiveWindow() == 'gThumb':
        pass
    else:
        try:
            activateWindow('gThumb')
        except:
            print('ERROR: gThumb is not active window')
            raise NameError

    pyPause = pyautogui.PAUSE
    # pyautogui.PAUSE = 0.3
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.PAUSE = pyPause
    copiedImage = pyperclip.paste()
    if restoreClipboard:
        pyperclip.copy(oldClipboard)
    if onlyBasename:
        copiedImage = os.path.basename(copiedImage)
    return copiedImage


def waitUntilWindowActivate(pattern):
    for f in range(3):
        for window in getListOfWindows():
            if pattern in window:
                while not pattern in getActiveWindow():
                    time.sleep(0.3)
                    activateWindow(pattern)
            else:
                pass

##########
## Anki ##
##########

def anki_add_htmlEditor_open():
    if getActiveWindow() == 'HTML Editor':
        pass
    else:
        if windowExist('HTML Editor'):
            waitUntilWindowActivate('HTML Editor')
        if windowExist('HTML Editor') == False:
            if windowExist('Add'):
                waitUntilWindowActivate('Add')
                pyautogui.hotkey('ctrl', 'shift', 'x')
                waitUntilWindowActivate('HTML Editor')
            if windowExist('Add') == False:
                pyautogui.alert(title='Anki ERROR', text="'Add' is closed!\nPlease, open it first.", button='OK!')



def anki_add_htmlEditor_write(text, mode='write', isImage=False, isDiferentDesktop=False):
    pyautogui.PAUSE = 0.3
    activateWindow('Add')
    if isDiferentDesktop:
        pyautogui.hotkey('shift', 'tab')
    else:
        pass
    if mode == 'removePrevious':
        pyautogui.press('backspace')
    anki_add_htmlEditor_open()
    if mode == 'write':
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
    elif mode == 'append':
        pyautogui.hotkey('ctrl', 'end')
    elif mode == 'removePrevious':
        pyautogui.hotkey('ctrl', 'end')
    else:
        pass
    if not isImage:
        pyautogui.typewrite(text)
    if isImage:
        pyautogui.typewrite(f'<img src="{text}">')
    pyautogui.press('esc')


def anki_add_htmlEditor_pasteImageFrom_gThumb(mode='write'):
    ok = False
    add = False
    gthumb = False
    currentWindow = False
    for window in getListOfWindows():
        if 'Add' in window:
            add = True
        if 'gThumb' in window:
            gthumb = True
    if add and gthumb:
        ok = True
    if ok:
        gthumbWindowInfo = getWindowInfo('gThumb', moreInfo=True)
        addWindowInfo = getWindowInfo('Add', moreInfo=True)
        activeWindiwInfo = getWindowInfo(getActiveWindow(), moreInfo=True)
        isDiferentDesktop = (not gthumbWindowInfo[1][2] == addWindowInfo[1][2]) or (not addWindowInfo[1][2] == activeWindiwInfo[1][2])
        anki_add_htmlEditor_write(gthumbCopyImageWithKeyboard(onlyBasename=True), isImage=True, isDiferentDesktop=isDiferentDesktop, mode=mode)
    else:
        pyautogui.alert(title='Anki ERROR', text="'Add' and/or 'gThumb' are closed!\nPlease, open it first.", button='OK!')
        sys.exit(1)


def anki_add_print(mode='onlyPaste', usemouse=True, numberOfField=3, simpleMode=True):
    if getActiveWindow() == 'gThumb':
        if isWindowActive('Add'):
            time.sleep(0.6)
            pyautogui.hotkey('ctrl', 'c')
            waitUntilWindowActivate('Add')
            if simpleMode:
                [pyautogui.hotkey('tab') for g in range(numberOfField-1)]
            else:
                addInfo = getWindowInfo('Add', moreInfo=True, exactMatch=True)
                mouse_x = float(addInfo[1][3]) + 100
                mouse_y = float(addInfo[1][4]) + 100
                pyautogui.scroll(50, x=mouse_x, y=mouse_y)
                pyautogui.click()
            if numberOfField > 1:
                [pyautogui.hotkey('tab') for g in range(numberOfField-1)]
            if mode == 'onlyPaste':
                pyautogui.hotkey('ctrl', 'end')
                pyautogui.hotkey('ctrl', 'shift', 'v')
            elif mode == 'removePrevious':
                pyautogui.hotkey('ctrl', 'end')
                pyautogui.hotkey('backspace')
                pyautogui.hotkey('ctrl', 'shift', 'v')
            elif mode == 'removeAll':
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.hotkey('del')
                # [hotkey('backspace') for r in range(3)] # free to remove
                pyautogui.hotkey('ctrl', 'shift', 'v')
            else:
                pass

            # return to first field
            [pyautogui.hotkey('shift', 'tab') for g in range(numberOfField-1)]
            pyautogui.scroll(50, x=(int(addInfo[1][5])-25), y=mouse_y)
            # [hotkey('pageup') for i in range(3)] # free to remove
            pyautogui.hotkey('ctrl', 'end')

        else:
            pyautogui.alert(title='Anki ERROR', text="'Add' is closed!\nPlease, open it first.", button='OK!')
    else:
        pass

def imgs_select(dirPath, fileManager="geeqie"):
    """ Use file manager to select images to merge """

    # save oldClipboard to restore later
    oldClipboard = pyperclip.paste()

    # open fileManager to copy images to clipboard
    runCommand(f'{fileManager} {dirPath}')
    
    # see if clipboard changed
    while pyperclip.paste() == oldClipboard:
        time.sleep(1)
        
    files = pyperclip.paste().splitlines()
    runCommand(f'pkill {fileManager}')

    # restore clipboard
    pyperclip.copy(oldClipboard)
    
    return files

def imgs_merge(imgs:list, outputPath, orientation='vertical'):
    """ Merge selected images"""

    if orientation == 'vertical':
        ori = '-'
    else:
        ori = '+'
        
    imgs = ' '.join(imgs)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%s')
    filename = f'{timestamp}_merged.png'
    outputPath = pathlib.Path(outputPath).resolve()
    outputPath = pathlib.Path.joinpath(outputPath, filename)
    com = f"convert {imgs} {ori}append {outputPath}"
    print(com)
    runCommand(com)

def anki_screenshot_notification(dirPath, nOfWeeks=4, orderPerNumberOfPendingPics=True, countAllCards=False, wait=False, in_line_message=False):
    if wait:
        time.sleep(600)
    plataform = subprocess.sys.platform

    if plataform == 'linux':
        try:
            flavor, version = subprocess.getoutput('lsb_release -d').split(':')[-1].strip().lower().split()
            version = float(version)
            if flavor == 'ubuntu':
                if version >= 19.00:
                    if not countAllCards:
                        fd = f'fdfind --change-newer-than {nOfWeeks}weeks --type file --search-path {dirPath}'
                    else:
                        fd = f'fdfind --type file --search-path {dirPath}'
            else:
                if not countAllCards:
                    fd = f'fd --change-newer-than {nOfWeeks}weeks --type file --search-path {dirPath}'
                else:
                    fd = f'fd --type file --search-path {dirPath}'
        except:
            if not countAllCards:
                fd = f'fd --change-newer-than {nOfWeeks}weeks --type file --search-path {dirPath}'
            else:
                fd = f'fd --type file --search-path {dirPath}'
        files = subprocess.getoutput(fd).splitlines()

        filesPerDirectory = {}
        for file in files:
            dirName, baseName = os.path.split(file)
            dirName = dirName.split(os.path.sep)
            a = dirName.index('pendingFlashcards')
            tempDir = f'{os.path.sep}'.join(dirName[a+1:])
            filesPerDirectory.setdefault(tempDir, 0)
            filesPerDirectory[f'{tempDir}'] = '{:02d}'.format(int(filesPerDirectory[f'{tempDir}'])+1)

        maxLen = 0
        orderPics = []
        for k, v in filesPerDirectory.items():
            if maxLen < len(k):
                maxLen = len(k)
        if orderPerNumberOfPendingPics:
            orderPics = sorted(filesPerDirectory.items(), key=lambda kv: kv[1], reverse=True)
        else:
            orderPics = sorted(filesPerDirectory.items(), key=lambda kv: kv[0], reverse=False)

        sumary = []
        for item in orderPics:
            # sumary.append(str(item[0].ljust(maxLen, '.')+str(item[1]).rjust(5)))
            sumary.append(str(f'<code>{item[1]}</code>. <i>{item[0]}</i>'))

        sumary = '\n'.join(sumary)
        message = f"You have <b>{len(files)}</b> screenshots of the last <b>{nOfWeeks}</b> weeks waiting to become cards!"
        text = f'{message}\n\n{sumary}'
        if in_line_message:
            print('''\
                You have \033[1;32m{}\033[0m screenshots waiting to become cards!
                '''.format(len(files)))
            print(text)
        else:
        	tg_bot(data_get('tg_bots_mike_token'), data_get('tg_bots_chatID_mcs'), text)

        return text
    else:
        raise SystemError


############
##Telegram##
############

def tg_bot(bot_token, chatID, message):

    baseUrl = f'https://api.telegram.org/bot{bot_token[0]}/sendMessage?chat_id={chatID[0]}&parse_mode=HTML&text='
    sendMessage = f'{baseUrl}{message}'
    response = requests.get(sendMessage)

    return response.json()

##########
##Ulogme##
##########/home/matheus/mcs/wo/R0/Thais_29_66/VCL66VHR3_S7_L001_R1_001aafreq.csv

def ulogme_run():
    ulogme_directory = data_get('ulogme_directory', isFileOrFolder=True, needTostartWithHome=True)
    os.chdir(ulogme_directory)
    subprocess.run('/usr/bin/python3 ./export_events.py &', shell=True)
    time.sleep(3)
    subprocess.run('/usr/bin/python3 ./ulogme_serve.py &', shell=True)
    time.sleep(0.2)
    runBrowser('http://localhost:8124')


def writeText(text):
    time.sleep(0.2)
    pyautogui.typewrite(text)


def writeText_screenshot_directory_current_pending():
    text = str(data_get('printPath', isFileOrFolder=True, needTostartWithHome=True))
    time.sleep(0.5)
    pyautogui.typewrite(text)

def writeText_screenshot_directory_current_created():
    text = str(data_get('printPath', isFileOrFolder=True, needTostartWithHome=True))
    text = text.replace('pendingFlashcards', 'createdFlashcards')
    time.sleep(0.5)
    pyautogui.typewrite(text)


def getAndWriteText(key, aut=False, enter=False):
    if aut:
        writeText(data_get(key, isAut=aut))
        if enter:
            time.sleep(0.3)
            pyautogui.press('enter')

    else:
        writeText(getData(key))


def runBrowser(url, mode='general', translator=False, browser_already_open=False):
    ''' Selectvly open browser '''

    # if general, execute default action
    if mode == 'general':
        command = browser_get_open()
        subprocess.run(f'{command} \"{url}\" &', shell=True)

    # if diferent mode, use it
    else:
        command = browserPreferences['mode'][mode]['browser']
        subprocess.run(f'{command} \"{url}\" &', shell=True)


def browser_get_open():
    ''' If browser is already open, use it. Else, select browser by predefined order '''

    browser_open = False
    windows = getListOfWindows()
    for window in windows:
        for k, v in browserPreferences['browser'].items():

            pattern_regex = re.compile(v['pattern'])
            pattern_match = pattern_regex.search(window)

            if pattern_match:
                browser_open = True
                browser_command = v['command']

    if not browser_open:
        browser_command = ''
        browser_preference = 0
        for k, v in browserPreferences['browser'].items():
            if v['preference'] > browser_preference:
                browser_preference = v['preference']
                browser_command = v['command']
    return browser_command

def runBrowserStudy(url):
    runBrowser(url, mode='study')


def ppress(key):
    pyautogui.press(key)


def runScript(scriptName):
    normalizePath()
    os.chdir(os.path.abspath(f'{os.getcwd()}/src/autokey/'))
    subprocess.run(f'python {scriptName} &', shell=True)


def runCommand(command):
    subprocess.run(f"{command} &", shell=True)


def translate(translator='deepl'):
    '''Abre uma página no navegador com a definição do texto selecionado com o cursor'''

    translators = {
                    'deepl': 'https://www.deepl.com/translator#en/pt/',
                    'linguee': 'https://www.linguee.com/english-portuguese/translation/',
                    'cambridge': 'https://dictionary.cambridge.org/dictionary/english/',
                    'googleAutoPt': 'https://translate.google.com.br/?source=osdd#auto|pt|',
                    'googlePtEn': 'https://translate.google.com.br/?source=osdd#pt|en|'
                }
    translatorsOnlyOneWord = ['linguee', 'cambridge']

    normalizePath()
    computer_name = platform.uname()[1].strip().replace(" ", "-")
    with open(os.path.abspath(os.path.join('..', 'data', f'translations_{computer_name}.csv')), 'a') as file:
        reader = csv.writer(file)
        line = []
        text = getSelection(removeCharacters=(('\n', '\r'), ' '))
        n = datetime.datetime.now()
        line.append(n.strftime('%s')) # get time
        line.append(text)
        line.append(getActiveWindow())
        line.append(computer_name)
        reader.writerow(line)

    base = translators[translator]
    phrase = getSelection(cleanString=True)
    charactersToRemove = ['.',',',':',';']
    [phrase.strip(f) for f in charactersToRemove]
    singleWord = False
    if phrase.find(' ') < 0:
        singleWord = True
    if singleWord:
        searchUrl = base + phrase
    else:
        if translator == 'googleAutoPt' or translator == 'googlePtEn':
            phrase = '+'.join(phrase.split())
            searchUrl = base + phrase
        else:
            phrase = ' '.join(phrase.split())
            searchUrl = base + phrase
    if translator in translatorsOnlyOneWord:
        if not singleWord:
            subprocess.run('zenity --notification  --window-icon=error --text "Select just one word" &', shell=True)
            sys.exit(1)
        if translator == 'linguee':
            searchUrl = base + phrase + '.html'
    runBrowser(searchUrl, translator=True)


def browseMap(mapProvider='googleMaps'):
    maps = {
            'googleMaps': 'https://www.google.com.br/maps/search/',
            'openStreet': 'https://www.openstreetmap.org/search?query='
        }
    address = getSelection(cleanString=True)
    searchUrl = maps[mapProvider] + address
    webbrowser.open(searchUrl)

def browseSearch(searchProvider='ddg'):
    searchProviders = {
                        'ddg': 'https://duckduckgo.com/?q=',
                        'google': 'https://www.google.com/search?q='
    }

    search = getSelection(cleanString=True)
    searchUrl = searchProviders[searchProvider] + search
    runBrowser(searchUrl)

# def browseOpenUrl():
#     regex = re.compile(
#         r'^(?:http|ftp)s?://' # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
#         r'localhost|' #localhost...
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
#         r'(?::\d+)?' # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)
#     url = getSelection()
#     if regex.search(url) is not None:
#         webbrowser.open(url)
#     else:
#         url = pyperclip.paste()
#         if regex.search(url) is not None:
#             webbrowser.open(url)
#         else:
#             subprocess.run('zenity --notification  --window-icon=error --text "Select a valid URL"', shell=True)

def takeScreenshot(playSound=False, program='maim', mode='region'):
    os.chdir(getPrintPath())
    if program == 'maim':
        if mode == 'region':
            command = "maim -s --hidecursor $(date +%Y-%m-%d_%H-%M-%S_%s)_maim.png"
        elif mode == 'active':
            pass
        subprocess.run(f"sleep 0.2 ; {command} &", shell=True)
    if program == 'flameshot':
        if mode == 'region':
            command = f'flameshot gui -p {getPrintPath()}'
        elif mode == 'active':
            pass
        subprocess.run(f"{command} &", shell=True)
    if program == 'scrot':
        if mode == 'activeWinow':
            command = f"scrot -u '%Y-%m-%d_%H-%M-%S_%s_scrot.png'"
            subprocess.run(f"sleep 0.2 ; {command} &", shell=True)
    if playSound:
        soundPath = data_get('cameraSound', isFileOrFolder=True, needTostartWithHome=True)
        soundCommand = 'audacious -qH'
        subprocess.run(f'{soundCommand} {soundPath}  &', shell=True)

def setPrintPath():
    os.chdir(data_get('path_root_pendingFlashcards', isFileOrFolder=True, needTostartWithHome=True))
    windowGeometry = '--maximized'
    path = os.popen(f'yad --file --directory {windowGeometry} --title="Choose Folder to Save Prints - Anki"').read().strip()
    if path:
        if getHome() in path:
            path = path.replace(getHome(), '')
        saveData('printPath', path)
        return path
    else:
        pyautogui.alert(title="Choose Folder to Save Prints - Anki", text="Print path didn't changed")

def browser_copyLink():
    if isWindowActive('- Mozilla Firefox'):
        waitUntilWindowActivate('- Mozilla Firefox')
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')
        [pyautogui.press('tab') for f in range(3)]
    else:
        pass

def browser_download_image():
    os.chdir(data_get('path_anki_prints_organize', isFileOrFolder=True, needTostartWithHome=True))
    try:
        url = pyperclip.paste()
        name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%s_wget.png')
        result = os.popen(f"wget -t 5 --https-only \'{url}\' --output-document={name}").read()
        subprocess.run(f'notify-send -i firefox -t 1000 "image downloaded" "{result}" &', shell=True)
        subprocess.run(f'feh {name} &', shell=True)
    except:
        subprocess.run(f'notify-send -i error -t 3000 "error while downloading image" &', shell=True)

def browser_select_by_preference():
    x = 0
    for browser, info in browserPreferences['browser'].items():
        if info['preference'] > x:
            x = info['preference']
            command = info['command']
    return command


def system_application_get_default(mimeType):
    app = subprocess.getoutput(f'xdg-mime query default {mimeType}').replace('.desktop', '')
    if app == 'sublime_text':
        command = 'subl'
    if app == 'sublime_text_3':
        command = 'subl3'
    else:
        command = app
    return command

def workout_done(nOfDays=1, dirDone='done'):

    confirm = pyautogui.confirm(title='One More Day Done - workout', text='Do you want to confirm this day as done?', buttons=['YES', 'NO'])

    if confirm == 'YES':

        path_workout = data_get('path_workout', isFileOrFolder=True, needTostartWithHome=True)
        imgs = sorted(os.listdir(path_workout))
        file1, file2 = [os.path.join(path_workout, imgs[x]) for x in range(2)]

        if os.path.isfile(file1) and os.path.isfile(file2):

            shutil.move(file1, os.path.join(os.path.dirname(file1), dirDone, os.path.basename(file1)))

        else:

            pyautogui.alert(title='No more workout days for this month! - workout', text='You done all exercises days for this month!\n\nI\'ll restart everything!')

            # TODO: move all images from ./done to current folder
            donePath = os.path.join(data_get('path_workout', isFileOrFolder=True, needTostartWithHome=True), dirDone)
            filesDone = os.listdir(donePath)

            for fileDone in filesDone:
                oldPath = os.path.join(donePath, fileDone)
                newPath = os.path.join(path_workout, fileDone)
                shutil.move(oldPath, newPath)

def text_editor_open_file(file):
    default_text_editor = system_application_get_default('text/x-python')
    subprocess.run(f"{default_text_editor} {file} &", shell=True)

def shell_run_list_commands_background(commands):
    for process in commands:
        subprocess.run(f"{process} &", shell=True)

def shell_run_one_command_background(command):
    subprocess.run(f'{command} &', shell=True)


#############
## startup ##
#############

def startup():

    #######
    # Old #
    #######

    # ## DEPRECATED - work in Plasma KDE (but currently I'm using i3wm)
    # # Set Wallpaper:

    # # OBS: wallpaper_command will have a string similar to this:
    # # ' dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript \'string:var Desktops = desktops();for (i=0;i<Desktops.length;i++) {d = Desktops[i];d.wallpaperPlugin = "org.kde.image";d.currentConfigGroup = Array("Wallpaper","org.kde.image","General");d.writeConfig("Image", "file:///PATH/TO/IMAGE.png");}\' '
    # # only replace `file:///PATH/TO/IMAGE.png` with the pretended wallpaper
    # # got this command in this link: https://www.reddit.com/r/kde/comments/65pmhj/change_wallpaper_from_terminal/dgc5qzy?utm_source=share&utm_medium=web2x

    # wallpaper_command = data_get('wallpaper_path')[0]
    # subprocess.run(wallpaper_command, shell=True)


    ###########################
    # Computer configurations #
    ###########################

    # Set touchpad configuration
    touchpad_tapping = 'xinput set-prop "SYNA7DB5:01 06CB:CD41 Touchpad" "libinput Tapping Enabled" 1'
    touchpad_natural_scrolling = 'xinput set-prop "SYNA7DB5:01 06CB:CD41 Touchpad" "libinput Natural Scrolling Enabled" 1'

    # Set keyboard repeat delay
    keyboard_delay = 'xset r rate 300 30'
    # Set keyboard layout
    keyboard_layout = 'setxkbmap -model acer_laptop -layout br'


    ##################
    # Start Programs #
    ##################

    flameshot_command = 'flameshot'
    activitywatch_command = 'aw-qt'
    rsibreak_command = 'rsibreak'
    redshift_command = 'redshift -O 4100 -g 0.8'
    parcellite_command = 'parcellite'
    dunst_command = '/usr/bin/dunst'
    sxhkd_command = f"pkill sxhkd ; sxhkd -c {data_get('file__sxhkd_mcs.txt', isFileOrFolder=True, needTostartWithHome=True)}"

    # Start custom scripts:

    ulogme_command = data_get('startup-ulogme', isFileOrFolder=True, needTostartWithHome=True)
    autokey_command = 'startup_autokey.py'
    wallpapers_command = 'wallpapers_random.py'
    sxhkd_command = 'run_program_sxhkd.py'
    anki_screenshot_notification_command = data_get('startup-anki_screenshot_notification', isFileOrFolder=True, needTostartWithHome=True)

    commands = []
    commands.append(touchpad_tapping)
    commands.append(touchpad_natural_scrolling)
    commands.append(keyboard_delay)
    commands.append(keyboard_layout)
    commands.append(flameshot_command)
    commands.append(activitywatch_command)
    commands.append(rsibreak_command)
    commands.append(redshift_command)
    commands.append(parcellite_command)
    commands.append(dunst_command)
    commands.append(ulogme_command)
    commands.append(autokey_command)
    commands.append(wallpapers_command)
    commands.append(sxhkd_command)
    commands.append(anki_screenshot_notification_command)

    shell_run_list_commands_background(commands)    

def startup_autokey(ui='gtk'):
    autokey_flavor = f'autokey.{ui}ui'
    autokey_path = data_get('autokey_path', isFileOrFolder=True, needTostartWithHome=True)
    os.chdir(os.path.join(autokey_path, 'lib'))
    subprocess.run(f'/usr/bin/python3 -m {autokey_flavor} &', shell=True)


####################
# Personalizations #
####################

def wallpapers_random():
    feh_command = 'feh --randomize --bg-fill /home/matheus/mcs/mat/images/myImages/background/wallpapers/*'
    shell_run_one_command_background(feh_command)



############
### i3wm ###
############

def i3_get_workspaces_names():
    '''
    This function read the content of i3wm configuration file
    and return a list with workspaces' names
    Ex:
    ['1: web',
     '2: term',
     '3: code',
     '4: apps',
     '5',
     '6',
     '7',
     '8',
     '9',
     '10: chats']
    '''
    config_file_path = data_get('file__i3configmcs.txt', isFileOrFolder=True, needTostartWithHome=True)
    with open(config_file_path) as config_file:
        data = config_file.readlines()
        # This regex only works for my configured pattern:
        #  set $ws<number> "<anything>"
        re_workspacenames = re.compile(r"((set)\s*(\$ws\d+)\s*(\".*\"))")
        workspace_names = []
        for line in data:
            workspace_name = re_workspacenames.search(line)
            if workspace_name:
                workspace_names.append(workspace_name.group(4).strip('"'))
    return workspace_names

def i3_get_workspaces_current():
    '''
    This function return the currently state of the activated workspaces
    in this form, for example:
        {'num': 1, 'name': '1: web', 'visible': False, 'focused': False, 'rect': {'x': 0, 'y': 0, 'width': 1366, 'height': 747}, 'output': 'eDP-1', 'urgent': False}
        {'num': 2, 'name': '2: term', 'visible': False, 'focused': False, 'rect': {'x': 0, 'y': 0, 'width': 1366, 'height': 747}, 'output': 'eDP-1', 'urgent': False}
        {'num': 3, 'name': '3: code', 'visible': True, 'focused': True, 'rect': {'x': 0, 'y': 0, 'width': 1366, 'height': 747}, 'output': 'eDP-1', 'urgent': False}
        {'num': 4, 'name': '4: apps', 'visible': False, 'focused': False, 'rect': {'x': 0, 'y': 0, 'width': 1366, 'height': 747}, 'output': 'eDP-1', 'urgent': False}
    '''
    # This function I copied from 
    # http://bhepple.com/doku/doku.php?id=unixscripts
    # file: i3-ws.py
    handle = subprocess.Popen(["i3-msg","-t","get_workspaces"], stdout=subprocess.PIPE)
    output = handle.communicate()[0]
    data = json.loads(output.decode())
    data = sorted(data, key=lambda k: k['name'])
    return data

def i3_get_workspace_current():
    '''
    Return the current active workspace
    in the form, for example:
        {'num': 3, 'name': '3: code', 'visible': True, 'focused': True, 'rect': {'x': 0, 'y': 0, 'width': 1366, 'height': 747}, 'output': 'eDP-1', 'urgent': False}
    '''
    data = i3_get_workspaces_current()
    for workspace in data:
        if workspace['visible'] == True:
            workspace_current = workspace
            break
    return workspace_current

def i3_get_workspace_pretended(which='next'):
    ''' 
    Select the 'next', ('previous' or 'prev') or '(<current_workspace> + <int>)', where <int> is positive (hence, selecting workspace 2 positions ahead the current) or negative (selecting workspace 2 positions before the current)
    Ex:
    i3_select_workspace(which='next')
    move from $ws1 → $ws2 

    i3_select_workspace(which='prev')
    move from $ws1 → $ws10  (assuming we have only 10 workspaces)

    i3_select_workspace(which=5)
    move from $ws1 → $ws6

    i3_select_workspace(which=-4)
    move from $ws1 → $ws7   (assuming we have only 10 workspaces)
    '''
    workspaces = i3_get_workspaces_names()
    workspace_current = i3_get_workspace_current()
    use_next_workspace = False
    num = workspace_current['num']
    tot = len(workspaces)
    if which == 'next':
        modify = 1
    elif which == 'prev' or which == 'previous':
        modify = -1
    else:
        # if `which` isn't 'next' neither 'previous', we'll assume this is an integer (either positive or negative)
        modify = int(which)

    if modify > 0:
        if ((modify + num) // tot) < 1:
            ws = modify + num
        elif ((modify + num) // tot) == 1 and ((modify + num) % tot) == 0:
            ws = modify + num
        else: 
            ws = (modify + num) % tot
    if modify < 0:
        if (num + modify) <= 0:
            ws = tot + (num + modify)
        else:
            ws = (num + modify)
    for workspace in workspaces:
        n = int(re.search(r'\d+', workspace).group())
        if n == ws:
            workspace_pretended = workspace

    return workspace_pretended

def i3_workspace(mode='focus', x='next'):
    ws = i3_get_workspace_pretended(which=x)
    base = 'i3-msg'
    common = 'workspace'
    if mode == 'focus':
        command = f"{base} {common} {ws}"
    if mode == 'move':
        command = f"{base} {mode} {common} {ws}"
    subprocess.run(command, shell=True)

def i3_exit_kill_ulogme():
    process = ['ulogme_data', 'keyfreq', 'logactivewin']
    for p in process:
        subprocess.run(f"pkill {p} &", shell=True)

def i3_exit_session():
    i3_exit_kill_ulogme()
    subprocess.run("i3-msg exit &", shell=True)

#####################
# Keyboard Shortcus #
#####################

def run_program_sxhkd():
    sxhkd_command = f"pkill sxhkd ; sxhkd -c {data_get('file__sxhkd_mcs.txt', isFileOrFolder=True, needTostartWithHome=True)}"
    shell_run_one_command_background(sxhkd_command)


############
## rclone ##
############

def rclone_is_running():
    # TODO:
    pass



####################
# Handle images
####################

def geeqieCopyImage(copy_type:str, default_quoted="ctrl-shift-c", default_unquoted="ctrl-c"):
    """Copy image to clipboard"""

    gq = 'Geeqie'
    quoted = default_quoted.split('-')
    unquoted = default_unquoted.split('-')

    assert copy_type in ['quoted', 'unquoted'], "copy_type must be either 'quoted' or 'unquoted'"
    assert isWindowActive(gq), "Geeqie must be open"

    # we want to preserve clipboard
    oldClipboard = pyperclip.paste()
    waitUntilWindowActivate(gq)
    if copy_type == 'quoted':
        pyautogui.hotkey('ctrl', 'shift', 'c')
    else:
        pyautogui.hotkey('ctrl', 'c')
    subprocess.Popen(f"echo -n 'file://{pyperclip.paste()}' | xclip -selection clipboard -t text/plain", shell=True)

def gqq():
    geeqieCopyImage('unquoted')

##############
# call scripts
##############


def anki_add_print_removeAll():
    anki_add_print('removeAll', simpleMode=False)

def anki_add_print_onlyPaste():
    anki_add_print('onlyPaste', simpleMode=False)

def anki_add_print_removePrevious():
    anki_add_print('removePrevious', simpleMode=False)

def anki_screenshot_notification_startup():
    anki_screenshot_notification('/home/matheus/mcs/study/anki/pics/pendingFlashcards/', wait=True)

def anki_screenshot_notification_oneshot():
    anki_screenshot_notification('/home/matheus/mcs/study/anki/pics/pendingFlashcards/')

def writeText_autokey_without_autohotkey():
    writeText('autokey -autohotkey')

def writeText_automate():
    writeText('Automate The Boring Stuff With Python')

def writeText_automateNoSpace():
    writeText('AutomateTheBoringStuffWithPython')

def writeText_searchKeys_filetype():
    writeText('filetype:')

def writeText_searchKeys_site():
    writeText('site:')

def writeText_searchKeys_site_ask():
    listOfSites = 'askubuntu.com,stackoverflow.com,meta.stackexchange.com,pt.stackoverflow.com,meta.stackoverflow.com'.split(',')
    search = 'site:' + ' OR site:'.join(listOfSites)
    writeText(search)

def writeText_searchKeys_site_reddit():
    writeText('site:reddit.com')

def runBrowser_bce_authorize():
    runBrowserStudy('http://minhabcedigital.bce.unb.br/ValidaAcessoEBSCO.aspx?biblio=minhabiblioteca&isbn=9788582714232')

def runBrowser_study_subject_chemistry_biochemistry_ahern():
    runBrowserStudy('https://oregonstate.edu/instruct/bb450/450material/schedule450s16.html')

def runBrowser_bce_book_alberts():
    runBrowserStudy('https://integrada.minhabiblioteca.com.br/#/books/9788582714065')

def writeText_bce_book_chemistry_organicChemistry_Klein():
    writeText('quimica organica klein')

def writeText_bce_book_chemistry_organicChemistry_McMurry():
    writeText('mcmurry quimica organica')

def runBrowser_bce_book_janeway():
    runBrowserStudy('https://integrada.minhabiblioteca.com.br/#/books/9788582710401')

def runBrowser_bce_book_klein1():
    runBrowserStudy('https://integrada.minhabiblioteca.com.br/#/books/9788521631934/')

def runBrowser_bce_book_klein():
    runBrowserStudy('https://integrada.minhabiblioteca.com.br/#/books/9788521631910')

def runBrowser_bce_book_lehninger():
    runBrowserStudy('https://integrada.minhabiblioteca.com.br/#/books/9788582715345')

def runBrowser_bce_book_stryer():
    runBrowserStudy('https://integrada.minhabiblioteca.com.br/#/books/978-85-277-2388-6')

def runBrowser_bce_book_the_cell():
    runBrowserStudy('https://integrada.minhabiblioteca.com.br/#/books/9788582714232')

def runBrowser_sites_pocket():
    runBrowser('https://getpocket.com/a/queue/list/')

def runBrowser_sites_whatsapp():
    runBrowser('https://web.whatsapp.com')

def runBrowser_sites_youtube():
    runBrowser('https://www.youtube.com/')

def runBrowser_sites_spotify():
    runBrowser('https://open.spotify.com/browse/featured')

def runBrowser_sites_gmail():
    runBrowser('https://mail.google.com/mail/u/0/#inbox')

def runBrowser_sites_protonmail():
    runBrowser('https://mail.protonmail.com/inbox')

def runBrowser_sites_outlook():
    runBrowser('https://outlook.office365.com/')

def writeText_bce_login():
    getAndWriteText('cpf')
    ppress('tab')
    getAndWriteText('bceLogin')
    ppress('tab')
    ppress('enter')

def writeText_bce_shibolet():
    getAndWriteText('emailMatriculaWeb')
    ppress('tab')
    getAndWriteText('passwordMatriculaWeb')
    ppress('enter')

def writeText_date():
    writeText(f"{datetime.datetime.now().strftime('%Y-%m-%d')}-")

def writeText_cep():
    getAndWriteText('cep')

def writeText_phone():
    getAndWriteText('phone')

def writeText_matricula():
    getAndWriteText('matricula')

def writeText_aut_jupyter():
    getAndWriteText('aut_jupyter', aut=True)

def writeText_aut_neptune():
    getAndWriteText('aut_neptune', aut=True)

def writeText_aut_jupyter_now():
    getAndWriteText('aut_jupyter', aut=True, enter=True)

def writeText_code_enterTODO():
    writeText('# TODO: ')

def writeText_cpf():
    getAndWriteText('cpf')

def writeText_ufrj_dre():
    getAndWriteText('ufrj_dre')

def writeText_ufrj_mail_dcc():
    getAndWriteText('ufrj_mail_dcc')

def writeText_rg():
    getAndWriteText('rg')

def writeText_rgPontuation():
    getAndWriteText('rgPontuation')

def anki_add_imgOcl_run():
    runScript('anki_add_imgOcl.py')

def runBrowser_ulogme_logView():
    ulogme_run()
    # runScript('run_ulogme_logView.py')

def writeText_names_jhenyfer():
    writeText('Jhenyfer')

def writeText_names_matheus():
    writeText('Matheus Cardoso de Souza')

def writeText_names_vallim():
    writeText('Vallim')

def writeText_logradouro():
    getAndWriteText('logradouro')

def writeText_gmail():
    getAndWriteText('gmail')

def writeText_email_mcs_protonmail():
    getAndWriteText('email_mcs_protonmail')

def writeText_email_mcs_unb_outlook():
    getAndWriteText('email_mcs_unb_outlook')

def writeText_email_mcs_ufrj_main():
    getAndWriteText('ufrj_mail_main')

def writeText_email_mcs_ufrj_dcc():
    getAndWriteText('ufrj_mail_dcc')

def run_webgrafia():
    runScript('run_webgrafia.py')

def run_program_anki():
    runCommand("anki -p 'study'")

def time_study_interval():
    runCommand("yad --title=interval_mcs")

def run_program_browser():
    runCommand(browser_select_by_preference())

def run_program_gthumb_currentDirectory():
    runCommand(f"gthumb -f {getPrintPath()}")

def run_program_feh_currentDirectory():
    runCommand(f'feh --reverse --sort mtime {getPrintPath()}')

def run_program_feh_workout():
    runCommand(f'feh -F {data_get("path_workout", isFileOrFolder=True, needTostartWithHome=True)}')

def run_program_fsearch():
    runCommand("fsearch")

def run_program_rsibreak_start():
    runCommand("killall rsibreak;rsibreak > /dev/null 2>&1")

def run_program_rsibreak_stop():
    runCommand("killall rsibreak")

def run_program_pomodoro_start_stop():
    runCommand("gnome-pomodoro --start-stop")

def run_program_pomodoro_start():
    runCommand("gnome-pomodoro --start")

def run_program_pomodoro_stop():
    runCommand("gnome-pomodoro --stop")

def run_program_pomodoro_pause_resume():
    runCommand("gnome-pomodoro --pause-resume")

def run_program_pomodoro_pause():
    runCommand("gnome-pomodoro --pause")

def run_program_pomodoro_resume():
    runCommand("gnome-pomodoro --resume")

def run_program_pomodoro_quit():
    runCommand("gnome-pomodoro --quit")

def run_program_xkill():
    runCommand("xkill")

def run_program_default_text_editor():
    runCommand(system_application_get_default('text/x-python'))

def run_program_default_text_editor():
    runCommand(system_application_get_default('text/x-python'))

def run_program_pdfsam():
    runCommand("pdfsam")

def run_program_joplin():
    runCommand(data_get('path_programs_joplin', isFileOrFolder=True, needTostartWithHome=True))

def run_program_telegram():
    runCommand('telegram-desktop')

def run_program_gnome_todo():
    runCommand('gnome-todo')

def run_program_spotify():
    runCommand('spotify')

def run_program_suspend():
    runCommand('sleep 3 && /usr/bin/systemctl suspend')

def runBrowser_translate_linguee():
    translate('linguee')

def runBrowser_translate_googlePtEn():
    translate('googlePtEn')

def runBrowser_translate_googleAutoPt():
    translate('googleAutoPt')

def runBrowser_translate_deepl():
    translate('deepl')

def runBrowser_translate_cambridge():
    translate('cambridge')

def runBrowser_maps_google():
    browseMap('googleMaps')

def runBrowser_maps_openStreet():
    browseMap('openStreet')

def runBrowser_search_ddg():
    browseSearch('ddg')

def runBrowser_openUrl():
    runBrowser(getSelection())

def screenshot_maim_region():
    takeScreenshot(program='maim', mode='region')

def imgs_select_run():
    imgs_select("/home/matheus/trash_mcs")

def imgs_merge_run():
    path = data_get('printPath', isFileOrFolder=True, needTostartWithHome=True)
    imgs_merge(imgs_select(path), path)

def screenshot_flameshot_region():
    takeScreenshot(program='flameshot', mode='region')

def screenshot_scrot_activeWindow():
    takeScreenshot(program='scrot', mode='activeWinow', playSound=True)

def screenshot_selectPrintDirectory():
    setPrintPath()

def text_editor_open_mcs():
    text_editor_open_file(data_get('file__mcs.py', isFileOrFolder=True, needTostartWithHome=True))

def text_editor_open_i3configmcs():
    text_editor_open_file(data_get('file__i3configmcs.txt', isFileOrFolder=True, needTostartWithHome=True))

def text_editor_open_sxhkd_mcs():
    text_editor_open_file(data_get('file__sxhkd_mcs.txt', isFileOrFolder=True, needTostartWithHome=True))

def text_editor_open_zpreztorc():
    text_editor_open_file(data_get('file__zpreztorc', isFileOrFolder=True, needTostartWithHome=True))

def i3_workspace_focus_next():
    i3_workspace(mode='focus', x='next')

def i3_workspace_focus_previous():
    i3_workspace(mode='focus', x='prev')


# set correct directory path
normalizePath()

######################
## global variables ##
######################

browserPreferences = collections.defaultdict(dict)
browserPreferences['browser'] = {
    'brave-browser': {
        'command': 'brave-browser', 'pattern': '- Brave', 'preference': 5
                    },
    'firefox': {
        'command': 'firefox', 'pattern': '- Mozilla Firefox', 'preference': 6
                },
    'vivaldi': {
        'command': 'vivaldi', 'pattern': '- Vivaldi', 'preference': 1
                },
    'vivaldi-stable': {
        'command': 'vivaldi-stable', 'pattern': '- Vivaldi', 'preference': 1
                },
    'min': {
        'command': 'min', 'pattern': '^Min$', 'preference': 3
                },
    'chromium': {
        'command': 'chromium', 'pattern': '- Chromium', 'preference': 4
                },
    'google-chrome': {
        'command': 'google-chrome', 'pattern': '- Google Chrome', 'preference': 2
                }
}
browserPreferences['mode']['study'] = {}
browserPreferences['mode']['study']['browser'] = browserPreferences["browser"][getData('browser_study')]["command"]

######################
######################
######################
