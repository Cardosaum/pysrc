import platform
import os
output = ""
output += "Platform: " + platform.platform() + "\n"
output += "Browser: " + os.popen("chromium-browser --version").read()
output += "Browser: " + os.popen("firefox --version").read()
output += "Date Tested :" + system.exec_command("date")
keyboard.send_keys(output)