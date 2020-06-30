from subprocess import call

try:
	call(['pip3', 'install', '-r', 'requirements.txt'])
	
except:
	try:
		call(['python3', '-m','pip', 'install', '-r', 'requirements.txt'])
	except:

		try:
			call(['pip', 'install', '-r', 'requirements.txt'])
		except:
			try: 
				call(['py', '-m','pip', 'install', '-r', 'requirements.txt'])
			except:
				call(['python', '-m','pip', 'install', '-r', 'requirements.txt'])