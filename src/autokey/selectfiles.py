#!/usr/bin/env python3

import sys
import os

os.system('clear')
print(f'Starting {sys.argv[0]}')
print('='*30)

pdir = sys.argv[-1] # Pretended DIRectory
fdir = sorted(os.listdir(pdir)) # Files  in DIRectory
fts = [] # Files To Save
fnts = [] # Files Not To Save

for f in fdir:
	print('='*20)
	f_or_d = '' # File or Directory
	if os.path.isfile(f):
		f_or_d = 'file'
	elif os.path.isdir(f):
		f_or_d = 'directory'
	if not f_or_d:
		f_or_d = 'unknown'
	print(f'{f_or_d}:\t{f}')
	while True:
		save = input('Save? [y/N]\t').strip().lower()
		if save == 'y' or save == 'n' or save == '':
			break
		else:
			print('Please, type only "Y", "<enter>" or "N"')
	if os.path.expanduser('~') in pdir:
		pdir = pdir.replace(os.path.expanduser('~'), '$HOME')
		# print(pdir)

	fappend = f'"{os.path.join(pdir, f)}"'
	if save == 'y':
		fts.append(fappend)

	else:
		fnts.append(fappend)

	print()
	print(f'Current saved files are:\n{set(fts)}')
	print(f'Current not saved files are:\n{set(fnts)}')
	# input('Do you wish to change anyone? ')

	print('='*20)

for f in fts:
	print(f)

print(f'files to save:\n{fts}')
print(f'files not to save:\n{fnts}')