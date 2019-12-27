import os

for file in sorted(os.listdir()):
    if os.path.isfile(file):
        if file.startswith('.'):
            print(os.path.abspath(file))
            # os.remove(os.path.abspath(file))
            # new = file.replace('.py', '')
            new = file.replace('-', '_')
            # print(file)
            # import shutil
            # shutil.move(file, new)
            # print(file.ljust(50), new)
