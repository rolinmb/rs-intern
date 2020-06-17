const xlsx = require('xlsx');
const axios = require('axios');
const cheerio = require('cheerio');

//Function that manipulates the html response into the data we want
function getData(html){
	var data = [];
	const $ = cheerio.load(html);
	
	//Get the tables with desired data
	data.push($('table').attr('class','table-hover').html());
	data.push($('table','div[id=no-more-tables]').html());
	
	/* Checking table formatting
		console.log("Table 1: \n");
		console.log(data[0] + '\n');
		console.log("Table 2: \n");
		console.log(data[1]); 		
	*/
	return data; 
}

//Use XLSX Package to open import_tempxl.xlsx file; 
//We are only using the first worksheet
var import_wb = xlsx.readFile('import_tempxl.xlsx');
var worksheet = import_wb.Sheets[import_wb.SheetNames[0]];
xlsx.writeFile(import_wb,'new_import.xlsx');

//Get NDC codes froms serverside html page

//Format url to scrape
const ndc_code = '50242-040-62';
const url = 'http://ndclist.com/ndc/' + ndc_code + '/package/' + ndc_code;

console.log('Working with NDC Code: ' + ndc_code);

//Making request to NDCList.com for seaching desired NDC codes
axios.get(url)
	.then(response => {
		//Call our fuctino to parse html into usable data to write to workbook
		var html_tables = getData(response.data);
		
		for(var i = 0; i < 2; i++){
			console.log('Table ' + (i+1) + ': \n' + html_tables[i] + '\n');
		}
		//console.log("Current State of Worksheet: \n");
		//console.log(worksheet);
		//console.log(html_tables);
	})
	.catch(error => {
		console.log(error);
	})


//Write import_wb to filename new_import.xlsx to finish
xlsx.writeFile(import_wb, 'new_import.xlsx');