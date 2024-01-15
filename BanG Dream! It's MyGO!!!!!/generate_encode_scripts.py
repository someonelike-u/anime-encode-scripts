templates = [
	{
		'EPISODE_NUMBER': '01', 'OPENING_START_FRAME': 'None', 'ENDING_RANGE': '(31769, 33926)'
	},
	{
		'EPISODE_NUMBER': '02', 'OPENING_START_FRAME': '1344', 'ENDING_RANGE': '(31528, 33685)'
	},
	{
		'EPISODE_NUMBER': '03', 'OPENING_START_FRAME': '0', 'ENDING_RANGE': '(31527, 33684)'
	},
	{
		'EPISODE_NUMBER': '04', 'OPENING_START_FRAME': '2038', 'ENDING_RANGE': '(30164, 32322)'
	},
	{
		'EPISODE_NUMBER': '05', 'OPENING_START_FRAME': '1846', 'ENDING_RANGE': '(31529, 33686)'
	},
	{
		'EPISODE_NUMBER': '06', 'OPENING_START_FRAME': '3381', 'ENDING_RANGE': '(31529, 33686)'
	},
	{
		'EPISODE_NUMBER': '07', 'OPENING_START_FRAME': '2830', 'ENDING_RANGE': '(30186, 32344)'
	},
	{
		'EPISODE_NUMBER': '08', 'OPENING_START_FRAME': '792', 'ENDING_RANGE': '(31527, 33684)'
	},
	{
		'EPISODE_NUMBER': '09', 'OPENING_START_FRAME': '9182', 'ENDING_RANGE': '(31530, 33687)'
	},
	{
		'EPISODE_NUMBER': '10', 'OPENING_START_FRAME': 'None', 'ENDING_RANGE': '(31529, 33686)'
	},
	{
		'EPISODE_NUMBER': '11', 'OPENING_START_FRAME': '2614', 'ENDING_RANGE': '(31528, 33685)'
	},
	{
		'EPISODE_NUMBER': '12', 'OPENING_START_FRAME': '1296', 'ENDING_RANGE': '(31527, 33684)'
	},
	{
		'EPISODE_NUMBER': '13', 'OPENING_START_FRAME': '1582', 'ENDING_RANGE': ''
	}
]

for template in templates:
	with open('mygo_template.py', 'r') as templateFile:
		content = templateFile.read()

	newContent = content.replace('EPISODE_NUMBER', template['EPISODE_NUMBER'])
	newContent = newContent.replace('OPENING_START_FRAME', template['OPENING_START_FRAME'])
	newContent = newContent.replace('ENDING_RANGE', template['ENDING_RANGE'])
	number = template['EPISODE_NUMBER']
	newFileName = f"mygo_{template['EPISODE_NUMBER']}.vpy"

	with open(newFileName, 'w') as newFile:
		newFile.write(newContent)

	print(f'Script generated: {newFileName}')