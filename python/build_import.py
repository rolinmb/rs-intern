from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os

#Function for formatting tabular data to tremove tooltips
def deleteSpans(table):
	for tr in table.find_all('tr'):
		for span in tr('span'):
			span.decompose()

#Function to parse tables from bs4 into list data
def parseTable(table):
	new_table = []
	for tr in table.find_all('tr'):
		columns = tr.find_all('td')
		output_row = []
		for col in columns:
			output_row.append(col.text)
		new_table.append(output_row)
	return new_table			

#Function to match data from html page to the .csv file, loaded into a dataframe
# Same as buildXlsx from scrape_ndc.py, but for individual rows
def buildRow(df,row,t1_rows,t2_rows):
	#Initialize the row to be empty
	df.loc[row] = [None]*54
	#Match data from webpage to coulmns in dataframe for importing
	df.loc[row][2] = t2_rows[1][0] 					     #NDC 11-digit code
	df.loc[row][14] = t2_rows[1][1] 				     #HCPCS code
	df.loc[row][12] = t1_rows[2][1] 				     #Package description
	df.loc[row][33] = t2_rows[1][3] 				     #Billable unit description
	df.loc[row][16] = ''.join([i for i in df.loc[row][33]#Base UoM from billable unit description
						if i.isalpha()])
	df.loc[row][27] = df.loc[0][16]					     #Billable UoM 
	df.loc[row][28] = ''.join([i for i in df.loc[row][33]#Billable Unity Qty
						if i.isdigit()])	
	df.loc[row][5] = ' '.join(t1_rows[8][1].split())   	 #Labeler/Manufacturer name (eliminating whitespace)
	df.loc[row][6] = t1_rows[3][1]					 	 #Proprietary name (omitting extra text)
	df.loc[row][7] = t1_rows[4][1]					 	 #Non-Proprietary name (omitting extra text)
	df.loc[row][10] = df.loc[row][7]               		 #Substance Name is same as Non-Proprietary
	df.loc[row][8] = t1_rows[9][1].split('-')[0]         #Dosage Form Name
	df.loc[row][9] = t1_rows[10][1].split('-')[0]        #Route Name
	return df

#Function to open .txt file containing codes for use in next script callable
def getCodes():
	codes = []	
	f = open("codes.txt","r")
	for line in f:
		#Eliminate whitespace/newlines 
		line = line.strip()
		codes.append(line)
	f.close()
	return codes

#EXECUTION STARTS HERE;	
#Scaled version of scrape_ndc.py; takes multiple ndc codes as inputs and outputs a file populated with information 
#for each individual ndc input
if __name__ == '__main__':
	print('NOTE: use NDC codes with dropped zeros')  
	print('    Ex => 50242-0040-62 => 50242-040-62\n')
	ndc_codes = getCodes()
	print("Captured NDC's: ", ndc_codes, "\n")
	import_frame = pd.read_csv("import_temp.csv")
	#For each code, preform a search and get the tabular data and parse into the import sheet
	cur_row = 0
	for code in ndc_codes:
		#Create the url for searching the item on NDCList.com
		url = 'http://ndclist.com/ndc/' + code + '/package/' + code
		req = urllib.request.Request(url,headers={'User-Agent' : "Magic Browser"})
		response = urllib.request.urlopen(req)
		html = response.read()
		soup = BeautifulSoup(html,'html.parser')
		table1 = soup.find('table', {'class':'table table-hover table-striped'})
		table2 = soup.find('table', {'class':'table table-striped'})
		deleteSpans(table1)
		deleteSpans(table2)
		#Parse html_tables into list of rows representation
		output_rows1 = parseTable(table1)
		output_rows2 = parseTable(table2)
		#Build and append the row for the current ndc code, builds driectly into frame (no returning)
		import_frame = buildRow(import_frame,cur_row,output_rows1,output_rows2)
		#Increment current row marker before next iteration
		cur_row += 1
		print("Finished with NDC: " + code)

	#print(import_frame)	
	#The import_frame should now contain populated data for all ndc codes
	#Finally conver the frame to xlsx sheet
	import_frame.to_excel("new_import.xlsx",index=False)
	print("\nFile-Path: new_import.xlsx Has been updated")