
import os
import sys
import subprocess

goodzones = 0
badzones = []

for entry in os.scandir(os.environ.get("DNS_ZONE_PATH", ".")):
	zonename = None

	if not entry.is_file():
		continue

	if entry.name.endswith('.db'):
		zonename = entry.name.rstrip('.db')

	if entry.name.endswith('.rev'):
		zonename = entry.name.lstrip('db.')
		zonename = zonename.rstrip('.rev')
		zonename = zonename.split('.')
		zonename.reverse()
		zonename.append('in-addr.arpa')
		zonename = ".".join(zonename)

	if zonename == None:
		continue

	s = subprocess.run (['/usr/sbin/named-checkzone', zonename, sys.argv[1] + '/' + entry.name], check=False)
	returncode = s.returncode

	if returncode:
		badzones.append(zonename)
	else:
		goodzones += 1

	print('\n' + str(goodzones) + ' zone files passed validation')
	print('\n' + str(len(badzones)) + ' zone files failed validation')

	for z in badzones:
		print('- ' + z)

	sys.exit(len(badzones))
