#
# parses output of give_guids.py and inserts data into a table
# 
# used mainly for mapping guids to names for arboreta
#

#
# create database:
#
# sqlite3 db2.sqlite
# CREATE TABLE samples (guid primary key, project, name, path, other_json);
#

import sys, json, sqlite3

con = sqlite3.connect("db2.sqlite")

json_data = json.loads(open(sys.argv[1]).read())
project = sys.argv[2]

for record in json_data:
	con.execute("insert into samples values (?, ?, ?, ?, ?)",
		(record['guid'], project, record['sample_name'], record['path'], json.dumps(record)))

con.commit()
