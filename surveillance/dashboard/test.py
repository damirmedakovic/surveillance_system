




import os


dirs = os.listdir('/home/dmedakovic/development/webdev/surveillance_website/surveillance/surveillance/media/')

diction = {}
for dirr in dirs:
	if dirr == 'client_script.py':
		continue
	else:
		diction[f'{dirr}'] = [file for file in os.listdir(f'/home/dmedakovic/development/webdev/surveillance_website/surveillance/surveillance/media/{dirr}')]

print(diction)


for i in diction:
	print(i)