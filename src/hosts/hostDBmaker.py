import sqlite3

# sourceConn = sqlite3.connect('fakeIDs.db')
# destConn = sqlite3.connect(

s = sourceConn.cursor()

# columnList is a list of tuples where each 
# tuple consists of first the column name from
# the original dB name and the second is the
# new desired column name
def makeSubDb(origFile, origTable, newFile, newTable, columns, primKey = None):
	origConn = sqlite3.connect(origFile)
	origConn.row_factory = sqlite3.Row
	origMetadata = ( origConn.execute("PRAGMA table_info({})".format(origTable)) ).fetchall()
	origCursor = origConn.execute('SELECT * FROM {}'.format(origTable))
	
	newConn = sqlite3.connect(newFile)
	
	createCommand = "CREATE TABLE {}(\n"
	
	origColumns = [m[1] for m in origMetadata]	
	newMetadata = [origMetadata[origColumns.index(m)] for m in columnList]
	createCommand += ", ".join([m[1] + ' ' + m[2] for m in newMetadata])
	
	if primKey != None:
		createCommand += ', PRIMARY KEY ({})'.format(primKey)
	createCommand += '\n);\n'
	
	newConn.execute(createCommand)
	
	for col in cloumns:
		
		
	"""
CREATE TABLE My_table(
 my_field1 INT,
 my_field2 VARCHAR(50),
 my_field3 DATE NOT NULL,
 PRIMARY KEY (my_field1, my_field2)
);
"""
	
	
	newConn = sqlite3.connect(origDb[0])
	# find how to get types from orig
	# get types fromnewConn
	
	
