import subprocess

def get_apps():
    Data = subprocess.check_output(['wmic', 'product', 'get', 'name'])
    a = str(Data)

    try:
	
	# arrange the string
	    for i in range(len(a)):
		    l = a.split("\\r\\r\\n")[6:][i]

    except IndexError as e:
	    pass

    return l

print(get_apps())