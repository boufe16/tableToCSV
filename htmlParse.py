
import urllib.request

url = 'urlhere.com'

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
   the_page = response.read()
newSTR = the_page.decode()
tablePos = newSTR.find('<table')
newSTR = newSTR[tablePos:]
tableEnd = newSTR.find('</table>')
table = newSTR[:tableEnd+8]

csvElements =[]; #Array of strings 
count =0
column =0
headerIdx = table.find('<thead')
header = table[headerIdx:]
headerIdx = header.find('>')
headerEnd = header.find('</thead')
header = header[headerIdx:headerEnd]


while True:
	idx = header.find('<th') #this will count the number of columns HOWEVER, the th tag is not required, this only works if the table has a header with TH tags
	if(idx <0):#can't find a <th tag
		break
	else:
		column+=1
	header = header[idx+1:]

headerIdx = table.find(header)
table = table[headerIdx:]# take the header off the table 
while True: 
	entryStart = table.find('<td')# returns -1 on failure
	entryStartTH = table.find('<th')
	if(entryStartTH > -1) :
		if (entryStartTH < entryStart): 
			entryStart = entryStartTH
	table = table[entryStart+4:]
	if(entryStart <0):
		break
	
	tagend = table.find('>')#end of td tag
	entryEnd = table.find('</td>')
	entryEndTH = table.find('</th')# returns -1 on failure
	if(entryEndTH > -1) :
		if (entryEndTH < entryEnd): 
			entryEnd = entryEndTH
	entry = table[tagend+1:entryEnd]
	
	if(len(entry) > 0):
		if(entry[0] == '<'):
			ftag = entry.find('>')
			etag = entry.find('</')
			entry = entry[ftag+1:etag]
			
	csvElements.append(entry)	
	table = table[entryEnd:]
	
f= open('output.csv', 'w')	
for i in range(0, len(csvElements)):
	f.write(csvElements[i])
	if(i % column == column-1): #here I hardcode how many columns there are... I could count the <th> tags 
		f.write('\n')
	else:
		f.write(';')
	# write a comma after the first value
		


