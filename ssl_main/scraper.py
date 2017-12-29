import requests
from bs4 import BeautifulSoup
import html
import os

directory = os.path.dirname(os.path.abspath(__file__)) + '/mails'


for filename in os.listdir(directory):
	# print(filename)
	exp = open('mails/'+filename)
	soup = BeautifulSoup(exp, 'lxml')
	text = soup.find('pre')
	text = text.get_text()
	text = text.strip()
	Pos = "Assistant Professor"
	if "promotion" in text or "promoted" in text:
	# print("New promotion")
		if "Professor" in text:
			newPos = "Professor"
			if "Assistant" in text:
				newPos = "Assistant Professor"
			if "Associate" in text:
				newPos = "Associate Professor"
			# if "HOD" in word or "hod" in word or "Head of Department" in word or "Head" in word or "head" in word or "Head" in word or "HoD" in word or "hOd" in word:
                # new_position.append(word)
            # if "Dean" in word or "dean" in word:
                # new_position.append(word)
            # if "Director" in word or "director" in word:
                # new_position.append(word)

			if newPos != Pos:
				Pos = newPos
				print(Pos)

	if "awards" in text or 'award' in text:
		strp = text.split("\n")
		for sss in strp:
			if "Title" in sss:
				print(sss[6:].strip()) 
			if "Award Name" in sss:
				print(sss[12:].strip())


