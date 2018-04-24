import pathlib
def cust_open(pathName,title,extension,permissions,content):
	pathlib.Path(pathName).mkdir(parents=False, exist_ok=True)
	file = open(pathName + title + extension, permissions)
	file.write(content)
	file.close()
