import sqlite3
import inspect


def makeSubDb(origFile, origTable, newFile, newTable, columns, primKey = None):
	conn = sqlite3.connect(origFile)
	conn.execute('ATTACH DATABASE "{}" AS newDb'.format(newFile))
	conn.execute('CREATE TABLE newDb.{} AS SELECT {} FROM {}'.format(newTable, ",".join(columns), origTable))
	conn.commit()
	conn.close()

def modifyColumnName(dbFile, table, oldName, newName):
	conn = sqlite3.connect(dbFile)
	conn.execute('pragma writable_schema = 1')
	tblStmt = conn.execute('select SQL from SQLITE_MASTER where name = "{}"'.format(table)).fetchall()
	tblStmt = tblStmt[0][0].replace(oldName, newName)
	conn.execute('UPDATE SQLITE_MASTER SET SQL = "{}" WHERE NAME = "{}"'.format(tblStmt, table))
	conn.execute('pragma writable_schema = 0')
	conn.commit()
	conn.close()

def modifyColumnValue(dbFile, table, column, callback):
	conn = sqlite3.connect(dbFile)
	conn.create_function("userFunc", 1, callback)
	conn.execute('UPDATE {} SET {} =  userFunc({})'.format(table, column, column))
	conn.commit()
	conn.close()

	
if __name__ == '__main__':
	# makeSubDb('fakeIDs.db', 'fakenames', 'mySub', 'people', ['guid', 'givenname', 'surname'])
	# modifyColumnName('mySub', 'people', 'guid', 'userID')
	# modifyColumnValue('mySub', 'people', 'userID', lambda x: x[:8]+x[9:13]+x[14:18])
	makeSubDb('fakeIDs.db', 'fakenames', 'certAuth.db', 'people', ['guid', 'givenname', 'surname', 'birthday'])
	modifyColumnName('certAuth.db', 'people', 'guid', 'userID')
	modifyColumnValue('certAuth.db', 'people', 'userID', lambda x: x[:8]+x[9:13]+x[14:18])
	
	makeSubDb('fakeIDs.db', 'fakenames', 'generalInfo.db', 'people', ['guid', 'givenname', 'surname', 'birthday', 'gender', 'state', 'city', 'streetaddress', 'emailaddress'])
	modifyColumnName('generalInfo.db', 'people', 'guid', 'userID')
	modifyColumnValue('generalInfo.db', 'people', 'userID', lambda x: x[:8]+x[9:13]+x[14:18])
	
	makeSubDb('fakeIDs.db', 'fakenames', 'health.db', 'people', ['guid', 'givenname', 'surname', 'birthday', 'gender', 'bloodtype', 'kilograms', 'centimeters'])
	modifyColumnName('health.db', 'people', 'guid', 'userID')
	modifyColumnValue('health.db', 'people', 'userID', lambda x: x[:8]+x[9:13]+x[14:18])
