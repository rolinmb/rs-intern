const express = require('express');
const cheerio = require('cheerio');
const axios = require('axios');
const xlsx = require('xlsx');
const path = require('path');
const mime = require('mime');
const fs = require('fs');

//Initialize the express engine
var app = express();
app.use(express.urlencoded());

//Defining constants for Host Port & Address
const HOST_PORT = '8080';
const HOST_ADDR = '127.0.0.1';

//Define the array of ndc codes that will be inputted by the user from form.html
//Will be manipulated in post '/submit-form' route
var ndcList = [];

//Use XLSX Package to open import_tempxl.xlsx file; 
//We are only using the first worksheet
var wb;
var worksheet;

//GET Request/Response Handling
//This page is sent upon the browser traversing to website, and upon completion of download
app.get('/',(request,response) => {
	//To Ensure we are working with a fresh sheet, 
	//Reset wb & worksheet objects, as well as new_import.xlsx upon homepage visit
	wb = xlsx.readFile('import_tempxl.xlsx');
	worksheet = wb.Sheets[wb.SheetNames[0]];
	xlsx.writeFile(wb,'new_import.xlsx');
	
	console.log("GET request to home page recieved from browser: ");
	
	//Use response.sendFile
	response.sendFile(path.join(__dirname + '/form.html'));
	console.log("Server has sent form.html via response. \n");
});


//POST Request/Response Handling
//The form.action attribute is "form-submit" for routing
app.post('/submit',(request,response) => {
	console.log('POST Form request recieved from browser: ');
	//Browser will traverse to a url with /submit-form appended
	
	//Now we can get the data rom the post request by using the html name attribute
	const ndcStr = request.body.ndcList;
	console.log('String value from HTML Form: \n' + ndcStr);
	
	//NOTE that ndcList formats the codes as comma-separated values
	//We must now parse the code srting into a collection of codes to iterate through,
	ndcList = ndcStr.split(' ');
	console.log('List for Scraping: [' + ndcList + ']\n');
	
	//Iterate through our list of codes(NOTE: the last index is empty)
	for(var i = 0; i < ndcList.length - 1; i++){
		var ndc = ndcList[i];
		console.log("Server Working with NDC Code: " + ndc + "\n");
		
		//Scraping individual ndc starts here; format the url for searching ndclist.com
		var url = 'http://ndclist.com/ndc/' + ndc + '/package/' + ndc;
		console.log('At url: ' + url + '\n')
		
		/*Use axios to request the url
		axios.get(url)
			.then(response => {
				//use response.data to get the html content
			})
			.catch(err => {
				console.log(err)
			});
		*/
	}
	
	//Write wb to filename new_import.xlsx to finish
	xlsx.writeFile(wb, 'new_import.xlsx');
	
	//Direct client to download page
	response.sendFile(path.join(__dirname + '/final.html'));
	console.log("Server directing browser to final.html page via response. \n");
});

app.get('/submit/download',(request,response) => {
	console.log('Download has been initiated by client: ');
	//Get Filetype parameters for Response header
	var file = path.join(__dirname + '/new_import.xlsx');
	var fname = path.basename(file);
	var mimetype = mime.lookup(file);
	//Specify headers for file
	response.setHeader('Content-Disposition', 'attachment; filename=' + fname);
	response.setHeader('Content-Type', mimetype);
	//Send the file/trigger download
	response.sendFile(file);
	console.log('Server has sent new_import.xlsx to browser: \n');
	//Now we wait on this page till the user returns to home '/'
});

//call server listen event, cast to a variable to handel s erver events
const server = app.listen(HOST_PORT,HOST_ADDR,() => {
	 //Logging initialization info
     console.log('Server active in directory: ', __filename);
     console.log('Listening on Port/Address: '+ HOST_PORT + ' / ' + HOST_ADDR + '\n');
});