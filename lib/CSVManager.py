import re
import csv
import time

class CSVManager:
	def __init__(self):
		self.fn = 'Test.csv'
		self.dt = [['Username', 'Password'],['John Doe', 'Jane Doe']]

	# def CSVWriter(self, data):
	# 	with open('Generated.csv', 'wb') as fp:
	# 		for row in data:
	# 			for column in row:
	# 				fp.write('%s;' % column)
	# 			fp.write('\n')
	# 		fp.close()
	# 		print 'Exported data => Generated.csv!' 
	def CSVWriter(self, data):
		with open('Generated.csv', 'wb') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=';')
			csvwriter.writerows(data)
			print 'Exported data => Generated.csv!'

	def dataToList(self, data):
		somelist = []
		finalist = []
		for k, v in data.items():
			somelist = [str(k), str(v)]
			finalist.append(somelist)
		return finalist

	def CSVReader(self, fileName):
		someCSV= []
		with open(fileName, 'r') as fp:
			for line in fp:
				line = re.sub('\s', '', line)
				someCSV.append(line.split(';'))
		return someCSV

	def plistTidy(self, data):
		#Get items from dictionary to list
		betaList = []
		finalList = []
		formatedList = []
		for k, v in data.items():
			origlist = v
		#append the items to an array list
		for aDict in origlist:
			for k, v in aDict.items():
				betaList = [k, repr(v)]
				finalList.append(betaList)
		#clean up the the list and format it nicely
		for item in finalList:
			if item[0] == "D":
				pass
			else:
				if item[0] == '':
					item[0] = "URL"
				item[1] = re.sub('[\'\[\]]', '', item[1])
				if item[0] == 'lastVisitedDate':
					timeFormat = float(item[1])
					timeFormat = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeFormat))
					item[1] = timeFormat
				formatedList.append(item)
		#return the list
		return formatedList

	def HTMLGenerator(self, data, fileName):
		with open('Generated.html', 'wb') as fp:
			fp.write("<html>")
			fp.write('<head><link rel="stylesheet " href="style.css" type="text/css" /><title>Python Generated</title></head>')
			fp.write("<body>")
			fp.write('<div class="tableStyle">')
			fp.write("<table>")
			fp.write("<tr><th>MetaINFO [%s]</th><th>RESULTS</th></tr>" % fileName)
			for row in data:
				fp.write("<tr>")
				for column in row:
					fp.write("<td>%s</td>" % (column))
				fp.write("</tr>")
			fp.write("</table>")
			fp.write("</div>")
			fp.write("</body>")
			fp.write("</html>")
			fp.close()
		with open('style.css', 'wb') as fp2:
			dataCss = """
table, th, td {
	border: 1px solid green;
}

table {
	border-collapse: collapse;
	width: 50%;
	table-layout:fixed;
	word-break:break-all;

}

th {
	background-color: green;
	color: white;
	height: 50px;
	font-size:20px;
}

td {
	text-align: left;
	padding: 10px;
}
"""
			fp2.write(dataCss)
			fp2.close()
			print 'Exported data => Generated.html!'
