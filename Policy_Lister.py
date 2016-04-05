# -*- coding: utf-8 -*-

'Firewall Policy Lister'

__author__ = 'persephonearthur'

# ------------------------------

from time import clock
tstart = clock()
import xlwt

# ------------------------------

f = file('putty.log', 'r')

# ------------------------------

def DataSplit(inlist):
	outlist = []
	for element in inlist:
		ds = []
		if '[' in element:
			ds = element.split('[')[1].strip().split(' ')
			ds.pop()
		else:
			ds.append(element.split(' ')[1])
		outlist.append(ds)
	return outlist

def DataUnite(inlist, index):
	for count, data in enumerate(DataSplit(inlist)[index]):
		if count == 0:
			str = data
		else:
			str = str + '\n' + data
	return str

# ------------------------------

print '<Policy Lister> Start Parsing Log File ......'

inputline = []

for line in f.readlines():
	inputline.append(line.strip().strip(';'))
f.close()
# print inputline

outputlist = []
policylist = []

for line in inputline:
	if 'policy' in line:
		outputlist.append(policylist)
		policylist = []
		policylist.append(line)
	while 'policy' not in line:
		policylist.append(line)
		break
outputlist.append(policylist)
# for index, element in enumerate(outputlist):
	# print index, element

# ------------------------------

name = []
active = []
src = []
des = []
app = []
state = []
log = []

for seq, policy in enumerate(outputlist):
	try:
		flag0 = 0
		flag1 = 0
		flag2 = 0

		for index, element in enumerate(policy):
			if 'policy' in element:
				if 'inactive' not in element:
					name.append(element.split(' ')[1])
					active.append('enable')
				else:
					name.append(element.split(' ')[2])
					active.append('disable')
			
			if 'source' in element:
				flag0 = 1
				if 'destination' not in policy[index + 1]:
					if 'destination' not in policy[index + 2]:
						src.append(element + ' ' + policy[index + 1] + ' ' + policy[index + 2])
					else:
						src.append(element + ' ' + policy[index + 1])
				else:
					src.append(element)

			if 'destination' in element:
				flag0 = 1
				if 'application' not in policy[index + 1]:
					if 'application' not in policy[index + 2]:
						des.append(element + ' ' + policy[index + 1] + ' ' + policy[index + 2])
					else:
						des.append(element + ' ' + policy[index + 1])
				else:
					des.append(element)

			if 'application' in element:
				flag0 = 1
				if '}' not in policy[index + 1]:
					if '}' not in policy[index + 2]:
						app.append(element + ' ' + policy[index + 1] + ' ' + policy[index + 2])
					else:
						app.append(element + ' ' + policy[index + 1])
				else:
					app.append(element)

			if 'permit' in element:
				flag1 = 1
			if 'deny' in element:
				flag1 = 2

			if 'log' in element:
				flag2 = 1

		if flag0 == 0:
			src.append('match -')
			des.append('match -')
			app.append('match -')
		
		if flag1 == 1:
			state.append('permit')
		elif flag1 == 2:
			state.append('deny')
		else:
			state.append('error')

		if flag2 == 1:
			log.append('log')
		else:
			log.append('-')
	except:
		print '------------------------------'
		print seq, policy, index, element
		print '------------------------------'

src = src[1:]
des = des[1:]
app = app[1:]
state = state[1:]
log = log[1:]

# print name
# print active
# print DataSplit(src)
# print DataSplit(des)
# print DataSplit(app)
# print state
# print log
		
# print len(name)
# print len(active)
# print len(DataSplit(src))
# print len(DataSplit(des))
# print len(DataSplit(app))
# print len(state)
# print len(log)

print '<Policy Lister> Finish Parsing Log File'

# ------------------------------

print '<Policy Lister> Start Generating Excel File ......'

w = xlwt.Workbook()
ws = w.add_sheet('Policy')

style = xlwt.easyxf('align: wrap on, vert centre, horiz centre;')

stylered = xlwt.easyxf('align: wrap on, vert centre, horiz centre;')
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
stylered.pattern = pattern

ws.write(0, 0, 'Rull_ID', style)
ws.write(0, 1, 'State', style)
ws.write(0, 2, 'Index', style)
ws.write(0, 3, 'Sequence', style)
ws.write(0, 4, 'Source', style)
ws.write(0, 5, 'Destination', style)
ws.write(0, 6, 'Port', style)
ws.write(0, 7, 'Action', style)
ws.write(0, 8, 'Logging', style)

for index, element in enumerate(active):
	if element == 'enable':
		st = style
	else:
		st = stylered
	
	ws.write(index + 1, 0, name[index], st)
	ws.write(index + 1, 1, element, st)
	ws.write(index + 1, 4, DataUnite(src, index), st)
	ws.write(index + 1, 5, DataUnite(des, index), st)
	ws.write(index + 1, 6, DataUnite(app, index), st)
	ws.write(index + 1, 7, state[index], st)
	ws.write(index + 1, 8, log[index], st)

w.save('Policy Lister.xls')

print '<Policy Lister> Finish Generating Excel File'

# ------------------------------

tfinish = clock()
print '<Policy Lister> List Total ' + str(len(name)) + ' Policies in ' + str(tfinish - tstart) + ' Seconds Successfully'
os.system("pause")