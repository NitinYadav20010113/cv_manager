def split(fullname):
	words = fullname.split(' ')
	if len(words)==1:
		first=words[0]
		middle=''
		last=''
	if len(words)==2:
		first=words[0]
		middle=''
		last=words[1]
	if len(words)>2:
		first=words[0]
		middle=words[1]
		last = ' '.join(words[2:])

	return first,middle,last