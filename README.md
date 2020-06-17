# rs-intern
This repository contains web-srapers implemented in Python and JavaScript(Node.js)
<ul>
<li>The main goal of this project was to accept a list of NDC Codes, format and perform a query
on www.ndclist.com, then parse the response html for necessary data to build items on Relia-Source's website.</li>
<li>The scraped data would be formatted and built into .xlsx files which are then able to be uploaded to Relia-Source's live database.</li>
</ul>

# /python
Contains the most complete python implementation for the NDC Web-Scraping project.
The python implementation uses 'import_temp.csv' as the template and uses pandas to create 'new_import.xlsx' as the target import file.<br />
<ul>
	<li><b>scrape_ndc.py</b>
		<ul>
			<li>Description of scrape_ndc.py</li>
			<li>Dependencies: </li>
		</ul>
	</li>
	<li><b>build_import.py</b>
		<ul>
			<li>Description of build_import.py</li>
			<li>Dependencies: </li>
		</ul>
	</li>
</ul>


# /node
Contains incomplete node.js implementaiton of the NDC Web-Scraping project. 
This implementation uses 'import_tempxl.xlsx' as the template and 'new_import.xlsx' as the target import file.<br />
<ul>
	<li><b>js_scrape.js</b>
		<ul>
			<li>Description of js_scrape.js</li>
			<li>Dependencies: </li>
		</ul>
	</li>
	<li><b>app.js</b>
		<ul>
			<li>Description of app.js</li>
			<li>Dependencies: </li>
		</ul>
	</li>
</ul>
