# usage: 
# python makeSchemaReadable.py



import json

jsonSchema = json.loads(open('bigquerySchema.js').read())


schema = dict()

def addToSchema(nameParts, datatype, dictToAddTo):
	part = nameParts.pop(0)
	if part not in dictToAddTo:
		dictToAddTo[part] = dict()

	dictToAddTo = dictToAddTo[part]
	
	if len(nameParts) == 0:
		dictToAddTo['.'] = datatype
	else:
		addToSchema(nameParts, datatype, dictToAddTo)


for item in jsonSchema:
	name = item['name']
	datatype = item['type']
	nameParts = name.split('_')
	addToSchema(nameParts, datatype, schema)


def schemaToString(schema, depth=0):
	outstr = ''
	if '.' in schema:
		outstr += ' : ' + schema['.']
	for key, subSchema in schema.items():
		if key == '.':
			continue
		outstr += '\n' + ' '*depth + key
		outstr += schemaToString(subSchema, depth +len(key)+1)
	return outstr

f = open('readableBigQuerySchema.txt', 'w')
f.write(schemaToString(schema))
f.close()