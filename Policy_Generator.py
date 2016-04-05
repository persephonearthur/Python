# -*- coding: utf-8 -*-

'Firewall Policy Generator'

__author__ = 'persephonearthur'

# --------------------

from time import clock
tstart = clock()

# --------------------
# Config
# --------------------

BREAK = '0'             # Source/Destination/Application 입력 종료용

SRCNAME = 'New_'		# 신규 추가 Source 이름, 예: New_1.1.1.1
DESNAME = 'New_'		# 신규 추가 Destination 이름, 예: New_1.1.1.1
APPNAME = 'tcp'			# 신규 추가 Application 이름, 예: tcp-111

MSRC = []				# Source/Destination/Application 에서,
MDES = []				# 입력 IP 가 많을 때, []안에 ['ip1','ip2','ip3']로 입력,
MAPP = []				# 예: ['1.1.1.1','1.1.1.2','1.1.1.3']

SERIAL = raw_input('Serial number like <20160101-001>: ')
AFTER = raw_input('After number like <20151231-001>: ')
UNTIL = raw_input('Available Until like <20171231>: ')
ANNOTATE = raw_input('Annotate like <A_to_B>: ')

# --------------------
# Source
# --------------------

def srccheck(inputip):
	try:
		ipa, ipb, ipc, ipd = map(int, inputip.split('.'))
		if 0 < ipa < 255 and 0 < ipb < 255 and -1 < ipc < 255 and -1 < ipd < 255:
			return inputip
		else:
			return srccheck(raw_input('Bad Input, Source: '))
	except:
		return srccheck(raw_input('Bad Input, Source: '))
		
# --------------------

unthost = []
untip = []
f = file('FW_untrust.asm', 'r')
for line in f.readlines():
	unthost.append(line.split(' ')[0])
	untip.append(line.split(' ')[1].split('/')[0])
f.close()

srclist = []
srchost = []
srcip = []
while True:
	source = raw_input('Source: ')
	if source == BREAK:
		break;
	else:
		source = srccheck(source)
		srclist.append(source)
srclist = list(set(srclist))
if len(MSRC):
	srclist = MSRC
else:
	pass
# print srclist

srchostnew = []
srcipnew = []
srcipnewtail = []
for element in srclist:
	if element in untip:
		srchost.append(unthost[untip.index(element)])
		srcip.append(element)
	else:
		srchostnew.append(SRCNAME + element)
		srcipnew.append(element)
# print srchost, srcip
# print srchostnew, srcipnew

for index, element in enumerate(srcipnew):
	ipa, ipb, ipc, ipd = map(int, element.split('.'))
	if ipc == 0 and ipd == 0:
		srcipnewtail.append('16')
	elif ipd == 0:
		srcipnewtail.append('24')
	else:
		srcipnewtail.append('32')

# --------------------

fout = file(SERIAL + '.asm', 'w+')
if len(srcipnew) > 0:
	for index, element in enumerate(srcipnew):
		fout.write('set security zones security-zone untrust address-book address ' + srchostnew[index] + ' ' + element + '/' + srcipnewtail[index] + '\n')
	fout.write('\n')
else:
	pass

# --------------------
# Destination
# --------------------

def descheck(inputip):
	try:
		ipa, ipb, ipc, ipd = map(int, inputip.split('.'))
		if 0 < ipa < 255 and 0 < ipb < 255 and -1 < ipc < 255 and -1 < ipd < 255:
			if ipa == 10 and ipb == 52:
				if ipc == 0 or ipc == 1 or ipc == 2 or ipc == 11 or ipc == 13 or ipc == 14 or ipc == 16 or ipc == 19 or ipc == 21 or ipc == 22 or ipc == 23 or ipc == 26 or ipc == 204:
					return inputip
				else:
					return descheck(raw_input('Bad Input, Destination: '))
			elif ipa == 10 and ipb == 55 and ipc == 227:
				return inputip
			elif ipa == 10 and ipb == 83 and ipc == 1:
				return inputip
			elif ipa == 10 and ipb == 246 and ipc == 52:
				return inputip
			elif ipa == 210 and ipb == 93 and ipc == 153:
				return inputip
			else:
				return descheck(raw_input('Bad Input, Destination: '))
			# return inputip
		else:
			return descheck(raw_input('Bad Input, Destination: '))
	except:
		return descheck(raw_input('Bad Input, Destination: '))
		
# --------------------

truhost = []
truip = []
f = file('FW_trust.asm', 'r')
for line in f.readlines():
	truhost.append(line.split(' ')[0])
	truip.append(line.split(' ')[1].split('/')[0])
f.close()

deslist = []
deshost = []
desip = []
while True:
	destination = raw_input('Destination: ')
	if destination == BREAK:
		break;
	else:
		destination = descheck(destination)
		deslist.append(destination)
deslist = list(set(deslist))
if len(MDES):
	deslist = MDES
else:
	pass
# print deslist

deshostnew = []
desipnew = []
desipnewtail = []
for element in deslist:
	if element in truip:
		deshost.append(truhost[truip.index(element)])
		desip.append(element)
	else:
		deshostnew.append(DESNAME + element)
		desipnew.append(element)
# print deshost, desip
# print deshostnew, desipnew

for index, element in enumerate(desipnew):
	ipa, ipb, ipc, ipd = map(int, element.split('.'))
	if ipc == 0 and ipd == 0:
		desipnewtail.append('16')
	elif ipd == 0:
		desipnewtail.append('24')
	else:
		desipnewtail.append('32')

# --------------------
if len(desipnew) > 0:
	for index, element in enumerate(desipnew):
		fout.write('set security zones security-zone trust address-book address ' + deshostnew[index] + ' ' + element + '/' + desipnewtail[index] + '\n')
	fout.write('\n')
else:
	pass

# --------------------
# Application
# --------------------

def appcheck(app):
	try:
		if 0 < int(app) < 65535:
			return app
		else:
			return appcheck(raw_input('Bad Input, Application: '))
	except:
		return appcheck(raw_input('Bad Input, Application: '))
		
# --------------------

porthost = []
portip = []
f = file('FW_app.asm', 'r')
for line in f.readlines():
	porthost.append(line.split(' ')[0])
	portip.append(line.split(' ')[1].strip())
f.close()

applist = []
apphost = []
appip = []
while True:
	app = raw_input('Application: ')
	if app == BREAK:
		break;
	else:
		app = appcheck(app)
		applist.append(app)
applist = list(set(applist))
if len(MAPP):
	applist = MAPP
else:
	pass
# print applist

apphostnew = []
appipnew = []
for element in applist:
	if element in portip:
		apphost.append(porthost[portip.index(element)])
		appip.append(element)
	else:
		apphostnew.append(APPNAME + '-' + element)
		appipnew.append(element)
# print apphost, appip
# print apphostnew, appipnew

# --------------------

if len(appipnew) > 0:
	for index, element in enumerate(appipnew):
		fout.write('set applications application ' + apphostnew[index] + ' protocol tcp' + '\n')
		fout.write('set applications application ' + apphostnew[index] + ' source-port 0-65535' + '\n')
		fout.write('set applications application ' + apphostnew[index] + ' destination-port ' + element + '\n')
		fout.write('\n')
else:
	pass
	
# --------------------
# Print
# --------------------

for element in srchostnew:
    fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' match source-address ' + element + '\n')
for element in srchost:
    fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' match source-address ' + element + '\n')
fout.write('\n')

for element in deshostnew:
    fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' match destination-address ' + element + '\n')
for element in deshost:
    fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' match destination-address ' + element + '\n')
fout.write('\n')

for element in apphostnew:
    fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' match application ' + element + '\n')
for element in apphost:
    fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' match application ' + element + '\n')
fout.write('\n')

fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' then permit\n')
fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' then log session-init\n')
fout.write('set security policies from-zone untrust to-zone trust policy ' + SERIAL + ' then log session-close\n')
fout.write('\n')

fout.write('insert security policies from-zone untrust to-zone trust policy ' + SERIAL + ' after policy ' + AFTER + '\n')
fout.write('\n')
fout.write('edit security policies from-zone untrust to-zone trust policy ' + SERIAL + '\n')
fout.write('annotate then \"##' + SERIAL + '_' + UNTIL + '_' + ANNOTATE + '##\"\n')
fout.write('\n')

fout.write('exit\n')
fout.write('show | compare\n')
fout.write('show | display set | match \n')
fout.write('commit\n')
fout.write('\n\n\n')

for element in srchostnew:
    fout.write(element + '\n')
for element in srchost:
    fout.write(element + '\n')
fout.write('\n')

for element in deshostnew:
    fout.write(element + '\n')
for element in deshost:
    fout.write(element + '\n')
fout.write('\n')

for element in apphostnew:
    fout.write(element + '\n')
for element in apphost:
    fout.write(element + '\n')
fout.close()

# --------------------

tfinish = clock()
print tfinish - tstart
os.system("pause")