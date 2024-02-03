for i in range(1, 12):
	with open('yon_nin_template.py', 'r') as templateFile:
		content = templateFile.read()
	number = "{:02d}".format(i)
	newContent = content.replace('EPISODE_NUMBER', number)
	number = number
	newFileName = f"yon_nin_{number}.vpy"

	with open(newFileName, 'w') as newFile:
		newFile.write(newContent)

	print(f'Script generated: {newFileName}')