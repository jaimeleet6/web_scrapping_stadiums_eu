print(" - table_1 = 80k\n - table_2 = 70-80k\n - table_3 = 60-70k\n - table_4 = 50-60k\n - table_5 = 40-50k\n - table_6 = 30-40k\n - table_7 = 25-30k")
stadiumTable = input("Pick a stadium table: ")

def scrape_stadium_csv(stadTable, idx=False):
	
	"""hay que decirle la tabla que se quiera sacar el csv (over 80k, 70-80k...) 
	   y si se quieren o no conservar los indices.
	    - table_1 = 80k
	    - table_2 = 70-80k
	    - table_3 = 60-70k
	    - table_4 = 50-60k
	    - table_5 = 40-50k
	    - table_6 = 30-40k
	    - table_7 = 25-30k"""

	from bs4 import BeautifulSoup
	import requests
	import pandas as pd

	# abrir el archivo html
	with open('stadiums.html', encoding='utf-8') as html_file:
		soup = BeautifulSoup(html_file, 'lxml')

	# guardamos todas las tablas por separado como se dice en el comentario
	tables = {}
	i = 1
	for table in soup.findAll('table', class_='wikitable sortable')[:-1]:
		tables["table_{}".format(i)] = table
		i += 1

	# nombre para cada archivo
	headlines = {}
	count = 1
	for head in soup.findAll('span', class_='mw-headline', id=lambda x: x and x.startswith("Capacity")):
		headlines["headl_{}".format(count)] = head.get('id').replace(",000", "k").replace("_–", "")
		count += 1


	# guardamos los nombres de las columnas que para todas son los mismos
	columns = tables["table_1"].find('tr')
	col_names = [th.text.strip() for th in columns.findAll('th')]

	# crear las tablas y guardarlas en csv
	foo = True
	while foo:
		if stadTable in tables.keys():
			stadRow = []
			for row in tables[stadTable].findAll('tr')[1:]:
				stadRow.append([td.text.strip() for td in row.findAll(('th','td'))])
				# hacer el dataframe
				df = pd.DataFrame(stadRow)
				df.columns = col_names
				csv = df.to_csv(r'./' + list(headlines.values())[list(tables.keys()).index(stadTable)] + '.csv', index=idx)

			print("Done! Check your directory")
			foo = False
			break

		else:
			print("Write table name like: {}".format(list(tables.keys())))
			stadTable = input("Pick a stadium table: ")




scrape_stadium_csv(stadiumTable)
