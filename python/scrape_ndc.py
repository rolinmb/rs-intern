from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os

#Delete all tooltips (<span>)
def deleteSpans(table):
	for tr in table.findAll('tr'):
		for span in tr('span'):
			span.decompose()

#Parse tables into readable form
def parseTable(table):
	new_table = []
	for tr in table.findAll('tr'):
		columns = tr.findAll('td')
		output_row = []
		for col in columns:
			output_row.append(col.text)
		new_table.append(output_row)
	return new_table

#Function to match data from html page to the .csv file, loaded into a dataframe
def buildXlsx(filename,t1_rows,t2_rows):
	df = pd.read_csv(filename)
	#Create initially empty list for the row
	df.loc[0] = [None]*54
	#Match data from webpage to ccoulmns in import sheet
	df.loc[0][2] = t2_rows[1][0] 					 #NDC 11-digit code
	df.loc[0][14] = t2_rows[1][1] 				     #HCPCS code
	df.loc[0][12] = t1_rows[2][1] 				     #Package description
	df.loc[0][33] = t2_rows[1][3] 				     #Billable unit description
	df.loc[0][16] = ''.join([i for i in df.loc[0][33]#Base UoM from billable unit description
						if not i.isdigit()])
	df.loc[0][27] = df.loc[0][16]					 #Billable UoM 
	df.loc[0][28] = ''.join([i for i in df.loc[0][33]#Billable Unity Qty
						if i.isdigit()])	
	df.loc[0][5] = ' '.join(t1_rows[8][1].split())   #Labeler/Manufacturer name
	df.loc[0][6] = t1_rows[3][1]					 #Proprietary name (omitting extra text)
	df.loc[0][7] = t1_rows[4][1]					 #Non-Proprietary name (omitting extra text)
	df.loc[0][10] = df.loc[0][7]               		 #Substance Name is same as Non-Proprietary
	
	return df
	
if __name__ == '__main__':
	print('NOTE: use NDC codes with dropped zeros')  
	print('    Ex; 50242-0040-62 => 50242-040-62') #this is Xolair's NDC
	#ndc = input("Enter a NDC Code to search: ")
	ndc = '68982-840-02'
	#URL of webpage of interest
	#    => URL MUST LOOK LIKE: 'http://ndclist.com/ndc/NDCHERE/package/NDCHERE'
	url = 'http://ndclist.com/ndc/' + ndc + '/package/' + ndc
	#Creating a http request, avoid 403 error with user-agent specification
	req = urllib.request.Request(url,headers={'User-Agent' : "Magic Browser"})
	#get the response from the request
	response = urllib.request.urlopen(req)
	html = response.read()
	soup = BeautifulSoup(html,'html.parser')
	table1 = soup.find('table', {'class':'table table-hover table-striped'})
	table2 = soup.find('table', {'class':'table table-striped'})
	deleteSpans(table1)
	deleteSpans(table2)
	output_rows1 = parseTable(table1) #Populating list to represent the first table (18 rows, output_rows1[0] = [empty])
	output_rows2 = parseTable(table2) #Populating list to represent the second table (2 rows, output_rows2[0] = [empty])
	# Lookin at data after formatting functions
	print("\n Number of Rows in Table 1: ", len(output_rows1))
	for row in output_rows1:
		print(row)

	print("\n Number of Rows in Table 2: ", len(output_rows2))
	for row in output_rows2:
		print(row)
		
	#Call fucntion to build the import sheet from the html tables/rows
	import_frame = buildXlsx("import_temp.csv",output_rows1,output_rows2)
	#Save written dataframe as "new_import.xlsx"
	import_frame.to_excel("new_import.xlsx",index=False)
	print("\nFile-Path: new_import.xlsx Has been updated")