'''
Custom Scripts made by Matheus
Intended to work with autokey
'''

def executeScript(scriptName):
    logFunction(scriptName)
    eval(f'{scriptName}()')

def logFunction(scriptName):
    from os.path import abspath, join
    from datetime import datetime
    normalizePath()
    stats = []
    n = datetime.now()
    stats.append(n.strftime('%s')) # get time
    stats.append(scriptName) # name of the script
    stats.append(getActiveWindow())
    callsFile = abspath(join('..', 'data', 'calls.csv'))
    with open(callsFile, 'a') as file:
        from csv import writer
        w = writer(file)
        w.writerow(stats)

def normalizePath():
    from os import chdir
    from os.path import abspath, join, realpath
    chdir(realpath(abspath(join(getHome(), 'src'))))

def getPrintPath():
    from os.path import abspath, join
    from shelve import open as op
    normalizePath()
    data = op(abspath(join('..', 'data', 'config')))
    printPath = data['printPath']
    data.close()
    return printPath

def getData(key, returnString=True):
    from os.path import abspath, expanduser, join
    from shelve import open as op
    data = op(abspath(join('..', 'data', 'config')))
    dataNeeded = data[key]
    data.close()
    if returnString:
        return str(dataNeeded)
    else:
        return dataNeeded

def data_get(key='', list_keys=False, isFileOrFolder=False, needTostartWithHome=False):
    from os.path import abspath, expanduser, join, sep, exists, relpath
    from os import chdir, getcwd
    from shelve import open as op
    normalizePath()
    with op(abspath(join('..', 'data', 'config'))) as f:

        if key:
            value = f[key]
            if sep in value:
                if isFileOrFolder:
                    if needTostartWithHome:
                        if value.startswith(getHome()):
                            if exists(value):
                                pass
                            else:
                                raise LookupError
                        else:
                            value = value.split(sep)
                            value = f'{getHome()}{sep.join(value)}'
                        return value
                    else:
                        return value
            return value, sep

        if list_keys:
            return list(f.items())

def saveData(key, value):
    from os.path import abspath, expanduser, join
    normalizePath()
    from shelve import open as op
    data = op(abspath(join('..', 'data', 'config')))
    data[key] = value
    dataSaved = data[key]
    data.close()
    return dataSaved

def removeData(key):
    from os.path import abspath, expanduser, join
    from os import chdir, getcwd
    pwd = getcwd()
    home = expanduser('~')
    rootFolderForScripts = data_get('rootFolderForScripts', isFileOrFolder=True, needTostartWithHome=True)
    chdir(rootFolderForScripts)
    from shelve import open as op
    data = op(abspath(join('..', 'data', 'config')))
    valueRemoved = data[key]
    data.pop(key)
    data.close()
    chdir(pwd)
    return valueRemoved



def getListOfWindows():
    from os import popen
    windows = popen('wmctrl -lG').read().strip('\n')
    windows = windows.splitlines()

    return windows


def getActiveWindow():
    from os import popen
    active = popen('xdotool getactivewindow getwindowname').read().strip('\n')

    return active


def isWindowActive(pattern):
    isWindowActive = False
    for window in getListOfWindows():
        if pattern in window:
            isWindowActive = True
    return isWindowActive

def getHome():
    from os.path import expanduser
    home = expanduser('~')

    return home

def getSelection(cleanString=False, removeCharacters=((), ' ')):
    from os import popen
    if cleanString:
        selection = popen('xclip -selection primary -o').read().replace('\n', ' ').strip()
        charactersToRemove = ['.',',',':',';','\n','\r','&']
        [selection.replace(character, ' ') for character in charactersToRemove]
    else:
        selection = popen('xclip -selection primary -o').read().strip('\n')
    if removeCharacters and cleanString == False:
        for character in removeCharacters[0]:
            selection.replace(character, removeCharacters[1])


    return selection

def getWindowInfo(windowPattern, moreInfo=False, exactMatch=False):
    import re
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
    from os import system
    window = getWindowInfo(windowPattern, moreInfo=True)
    system(f'wmctrl -ia {window[1][1]}')


def gthumbCopyAndPaste(typeOfCopy='removePrevious'):

    if getActiveWindow() == 'gThumb':
        import pyautogui
        from time import sleep
        pyautogui.PAUSE = 0.1

        if 'Add' in getWindowInfo('Add'):
            sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            activateWindow('Add')
            sleep(0.5)
            pyautogui.hotkey('ctrl', 'shift', 't')
            for f in range(12):
                pyautogui.hotkey('tab')
                # sleep(0.1)

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
            exit()
    else:
        exit()

def gthumbCopyImageWithMouse():
    if getActiveWindow() == 'gThumb':
        pass
    else:
        try:
            activateWindow('gThumb')
        except:
            print('ERROR: gThumb is not active window')
            raise NameError

    import pyautogui
    pyPause = pyautogui.PAUSE
    # pyautogui.PAUSE = 0.3
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
    import pyperclip
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

    import pyautogui
    pyPause = pyautogui.PAUSE
    # pyautogui.PAUSE = 0.3
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.PAUSE = pyPause
    copiedImage = pyperclip.paste()
    if restoreClipboard:
        pyperclip.copy(oldClipboard)
    if onlyBasename:
        from os.path import basename
        copiedImage = basename(copiedImage)
    return copiedImage


def waitUntilWindowActivate(pattern):
    from time import sleep
    for f in range(3):
        for window in getListOfWindows():
            if pattern in window:
                while not pattern in getActiveWindow():
                    sleep(0.3)
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
                import pyautogui
                pyautogui.hotkey('ctrl', 'shift', 'x')
                waitUntilWindowActivate('HTML Editor')
            if windowExist('Add') == False:
                from pyautogui import alert
                alert(title='Anki ERROR', text="'Add' is closed!\nPlease, open it first.", button='OK!')



def anki_add_htmlEditor_write(text, mode='write', isImage=False, isDiferentDesktop=False):
    import pyautogui
    # from pyautogui import hotkey, typewrite, press
    # from time import sleep
    # print(isDiferentDesktop)
    # sleep(7)
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
        from pyautogui import alert
        alert(title='Anki ERROR', text="'Add' and/or 'gThumb' are closed!\nPlease, open it first.", button='OK!')
        from sys import exit
        exit(1)


def anki_add_print(mode='onlyPaste'):
    if getActiveWindow() == 'gThumb':
        if isWindowActive('Add'):
            from pyautogui import PAUSE, hotkey
            PAUSE = 0.3
            from time import sleep
            sleep(0.6)
            hotkey('ctrl', 'c')
            waitUntilWindowActivate('Add')
            [hotkey('tab') for g in range(2)]
            if mode == 'onlyPaste':
                hotkey('ctrl', 'end')
                hotkey('ctrl', 'shift', 'v')
            elif mode == 'removePrevious':
                hotkey('ctrl', 'end')
                hotkey('backspace')
                hotkey('ctrl', 'shift', 'v')
            elif mode == 'removeAll':
                hotkey('ctrl', 'a')
                hotkey('backspace')
                [hotkey('backspace') for r in range(3)]
                hotkey('ctrl', 'shift', 'v')
            else:
                pass
            [hotkey('shift', 'tab') for f in range(2)]
            [hotkey('pageup') for i in range(3)]
            hotkey('ctrl', 'end')
            PAUSE = 0.1

        else:
            from pyautogui import alert
            alert(title='Anki ERROR', text="'Add' is closed!\nPlease, open it first.", button='OK!')
    else:
        pass

def anki_screenshot_notification(dirPath, nOfWeeks=4, orderPerNumberOfPendingPics=True, countAllCards=False):
    from subprocess import getoutput
    from subprocess import sys
    plataform = sys.platform

    if plataform == 'linux':
        flavor, version = getoutput('lsb_release -d').split(':')[-1].strip().lower().split()
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
        files = getoutput(fd).splitlines()

        filesPerDirectory = {}
        import os
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
        tg_bot(data_get('tg_bots_mike_token'), data_get('tg_bots_chatID_mcs'), text)

        return text
    else:
        raise SystemError


############
##Telegram##
############

def tg_bot(bot_token, chatID, message):
    import requests

    baseUrl = f'https://api.telegram.org/bot{bot_token[0]}/sendMessage?chat_id={chatID[0]}&parse_mode=HTML&text='
    sendMessage = f'{baseUrl}{message}'
    response = requests.get(sendMessage)

    return response.json()




def writeText(text):
    from pyautogui import typewrite
    from time import sleep
    sleep(0.2)
    typewrite(text)

def writeText_screenshot_currentDirectory():
    from pyautogui import typewrite
    from time import sleep
    text = str(data_get('printPath', isFileOrFolder=True))
    sleep(0.5)
    typewrite(text)

def getAndWriteText(key):
    writeText(getData(key))

def runBrowser(url, mode='general', translator=False):
    from collections import defaultdict
    browserPreferences = defaultdict(dict)
    browserPreferences['browser'] = {'brave-browser': {'command': 'brave-browser','pattern': '- Brave','preference': 9},'firefox': {'command': 'firefox','pattern': '- Mozilla Firefox','preference': 10}}
    browserPreferences['mode']['study'] = {}
    browserPreferences['mode']['study']['browser'] = browserPreferences["browser"]["brave-browser"]["command"]
    if mode == 'study':
        from os import system
        system(f"{browserPreferences['mode']['study']['browser']} {url}")

    else:
        preferedBrowsers = [('firefox', '- Mozilla Firefox', 10), ('brave-browser', '- Brave', 9)]
        useDefaltBrowser = True
        useThisBrowser = ''
        for browser in preferedBrowsers:
            if isWindowActive(browser[1]):
                useDefaltBrowser = False
                if useThisBrowser:
                    if useThisBrowser[2] < browser[2]:
                        useThisBrowser = browser
                else:
                    useThisBrowser = browser

        if useDefaltBrowser:
            from webbrowser import open as op
            op(url)

        else:
            from os import system
            if translator:
                system(f"{useThisBrowser[0]} \"{url}\"")

            else:
                system(f"{useThisBrowser[0]} {url}")

def runBrowserStudy(url):
    runBrowser(url, mode='study')

def ppress(key):
    from pyautogui import press
    press(key)

def runScript(scriptName):
    from os import chdir, system, getcwd
    from os.path import abspath
    normalizePath()
    chdir(abspath(f'{getcwd()}/src/autokey/'))
    system(f'python {scriptName}')

def runCommand(command):
    from os import system
    system(command)

def translate(translator='deepl'):
    '''Abre uma página no navegador com a definição do texto selecionado com o cursor'''

    from os import popen
    from os.path import abspath, join
    from csv import writer
    from datetime import datetime
    translators = {
                    'deepl': 'https://www.deepl.com/translator#en/pt/',
                    'linguee': 'https://www.linguee.com/english-portuguese/translation/',
                    'cambridge': 'https://dictionary.cambridge.org/dictionary/english/',
                    'googleAutoPt': 'https://translate.google.com.br/?source=osdd#auto|pt|',
                    'googlePtEn': 'https://translate.google.com.br/?source=osdd#pt|en|'
                }
    translatorsOnlyOneWord = ['linguee', 'cambridge']

    normalizePath()
    with open(abspath(join('..', 'data', 'translations.csv')), 'a') as file:
        reader = writer(file)
        line = []
        text = getSelection(removeCharacters=(('\n', '\r'), ' '))
        n = datetime.now()
        line.append(n.strftime('%s')) # get time
        line.append(text)
        line.append(getActiveWindow())
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
            from os import system
            from sys import exit
            system('zenity --notification  --window-icon=error --text "Select just one word"')
            exit(1)
        if translator == 'linguee':
            searchUrl = base + phrase + '.html'
    runBrowser(searchUrl, translator=True)

def browseMap(mapProvider='googleMaps'):
    from webbrowser import open as op
    maps = {
            'googleMaps': 'https://www.google.com.br/maps/search/',
            'openStreet': 'https://www.openstreetmap.org/search?query='
        }
    address = getSelection(cleanString=True)
    searchUrl = maps[mapProvider] + address
    op(searchUrl)

def browseSearch(searchProvider='ddg'):
    from webbrowser import open as op
    searchProviders = {
                        'ddg': 'https://duckduckgo.com/?q=',
                        'google': ''
    }

    search = getSelection(cleanString=True)
    searchUrl = searchProviders[searchProvider] + search
    op(searchUrl)

def browseOpenUrl():
    from webbrowser import open as op
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    url = getSelection()
    if regex.search(url) is not None:
        op(url)
    else:
        import pyperclip
        url = pyperclip.paste()
        if regex.search(url) is not None:
            op(url)
        else:
            from os import system
            system('zenity --notification  --window-icon=error --text "Select a valid URL"')

def takeScreenshot(playSound=False, program='maim', mode='region'):
    from os import system, chdir
    chdir(getPrintPath())
    if program == 'maim':
        if mode == 'region':
            command = "maim -s --hidecursor $(date +%Y-%m-%d_%H-%M-%S_%s)_maim.png"
        elif mode == 'active':
            pass
        system(f"sleep 0.2 ; {command}")
    if program == 'flameshot':
        if mode == 'region':
            command = f'flameshot gui -p {getPrintPath()}'
        elif mode == 'active':
            pass
        system(command)
    if program == 'scrot':
        if mode == 'activeWinow':
            command = f"scrot -u '%Y-%m-%d_%H-%M-%S_%s_scrot.png'"
            system(f"sleep 0.2 ; {command}")
    if playSound:
        soundPath = data_get('cameraSound', isFileOrFolder=True, needTostartWithHome=True)
        soundCommand = 'audacious -qH'
        system(f'{soundCommand} {soundPath}')

def setPrintPath():
    from os import popen, chdir
    chdir(data_get('path_root_pendingFlashcards', isFileOrFolder=True, needTostartWithHome=True))
    windowGeometry = '--maximized'
    path = popen(f'yad --file --directory {windowGeometry} --title="Anki - Choose Folder to Save Prints"').read().strip()
    saveData('printPath', path)
    return f'{path+"/"}'

def browser_copyLink():
    if isWindowActive('- Mozilla Firefox'):
        waitUntilWindowActivate('- Mozilla Firefox')
        from pyautogui import hotkey, press
        hotkey('ctrl', 'l')
        hotkey('ctrl', 'c')
        [press('tab') for f in range(3)]
    else:
        pass

def browser_download_image():
    from os import chdir, system, popen
    from datetime import datetime
    from pyperclip import paste
    chdir(data_get('path_anki_prints_organize', isFileOrFolder=True, needTostartWithHome=True))
    try:
        url = paste()
        name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%s_wget.png')
        result = popen(f"wget -t 5 --https-only \'{url}\' --output-document={name}").read()
        system(f'notify-send -i firefox -t 1000 "image downloaded" "{result}"')
        system(f'feh {name}')
    except:
        system(f'notify-send -i error -t 3000 "error while downloading image"')

##############
# call scripts
##############


def anki_add_print_removeAll():
    anki_add_print('removeAll')

def anki_add_print_onlyPaste():
    anki_add_print('onlyPaste')

def anki_add_print_removePrevious():
    anki_add_print('removePrevious')


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
    from datetime import datetime
    typewrite(f"{datetime.now().strftime('%Y-%m-%d')}-")

def writeText_cep():
    getAndWriteText('cep')

def writeText_phone():
    getAndWriteText('phone')

def writeText_matricula():
    getAndWriteText('matricula')

def writeText_code_enterTODO():
    writeText('# TODO: ')

def writeText_cpf():
    getAndWriteText('cpf')

def writeText_rg():
    getAndWriteText('rg')

def writeText_rgPontuation():
    getAndWriteText('rgPontuation')

def anki_add_imgOcl_run():
    runScript('anki_add_imgOcl.py')

def runBrowser_ulogme_logView():
    runScript('run_ulogme_logView.py')

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

def run_webgrafia():
    runScript('run_webgrafia.py')

def run_program_anki():
    runCommand("anki -p 'study'")

def run_program_browser():
    runCommand("firefox")

def run_program_gthumb_currentDirectory():
    runCommand(f"gthumb -f {getPrintPath()}")

def run_program_feh_currentDirectory():
    runCommand(f'feh --reverse --sort mtime {getPrintPath()}')

def run_program_fsearch():
    runCommand("fsearch")

def run_program_xkill():
    runCommand("xkill")

def run_program_sublime():
    runCommand("subl")

def run_program_pdfsam():
    runCommand("pdfsam")

def run_program_joplin():
    runCommand(data_get('path_programs_joplin', isFileOrFolder=True, needTostartWithHome=True))

def run_program_telegram():
    runCommand(data_get('path_programs_telegram', isFileOrFolder=True, needTostartWithHome=True))

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
    browseOpenUrl()

def screenshot_maim_region():
    takeScreenshot(program='maim', mode='region')

def screenshot_flameshot_region():
    takeScreenshot(program='flameshot', mode='region')

def screenshot_scrot_activeWindow():
    takeScreenshot(program='scrot', mode='activeWinow', playSound=True)

def screenshot_selectPrintDirectory():
    setPrintPath()

# set correct directory path
normalizePath()
