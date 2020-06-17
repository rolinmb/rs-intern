# rs-intern
This repository contains web-srapers implemented in Python and JavaScript.
<ul>
<li>The main goal of this project was to accept a list of NDC Codes, format and perform a query
on www.ndclist.com, then parse the response html for necessary data to build items on Relia-Source's website.</li>
<li>The scraped data would be formatted and built into .xlsx files which are then able to be uploaded to Relia-Source's live database.</li>
</ul>

# /python
Contains the most complete python implementations for the NDC Web-Scraping project.
The python implementation uses 'import_temp.csv' as the template and uses pandas to create 'new_import.xlsx' as the target import file.<br />
<ul>
	<li><b>scrape_ndc.py</b>
		<ul>
			<li>Accepts a single NDC code, formats query, scrapes data, then creates single row in 'new_import.xlsx' with required data.</li>
			<li><i>Dependencies</i>: BeautifulSoup, Pandas</li>
		</ul>
	</li>
	<li><b>build_import.py</b>
		<ul>
			<li>Accepts a multitude of NDC codes as individual lines in 'codes.txt', formats a query for each code, scrapes data, 
				and builds a row for each code in 'new_import.xlsx' with required data</li>
			<li><i>Dependencies</i>: BeautifulSoup, Pandas</li>
		</ul>
	</li>
</ul>


# /node
Contains incomplete node.js implementaiton of the NDC Web-Scraping project. 
This implementation uses 'import_tempxl.xlsx' as the template and 'new_import.xlsx' as the target import file.<br />
<ul>
	<li><b>js_scrape.js</b>
		<ul>
			<li>Incomplete web-scraping script for single NDC code. Formats query and recieves, then parses HTML for required data.</li>
			<li>Does not build 'new_import.xlsx' with data as code stands currently.</li>
			<li><i>Dependencies</i>: axios.js, cheerio.js, xlsx(sheetJS)</li>
		</ul>
	</li>
	<li><b>app.js</b>
		<ul>
			<li>Incomplete web-application that operates on localhost, serves a HTML form where user can input NDC codes.</li>
			<li>Does not build 'new_import.xlsx' with data as code stands currently.</li>
			<li><i>Dependencies</i>: axios.js, cheerio.js, express.js, mime, xlsx(sheetJS)</li>
		</ul>
	</li>
</ul>
