import random

alpha = list("abcdefghijklmnopqrstuvwxyz")
Alpha = list("abcdefghijklmnopqrstuvwxyz".upper())
numer = list("0123456789")
symbo = list("~`!@#$%^&*()_-+=")

# Character table for override
override = list("".join(alpha) + "".join(Alpha) + "".join(numer) + "".join(symbo))

# Clean the user's input
def cleanInput(strInput):
	clnInput = ""
	
	for i in list(strInput):
		if (i in numer):
			clnInput += i

	if (len(clnInput) == 0):
		clnInput = numer[random.randint(0, len(numer)-1)]
			
	return clnInput
	
def keyMap(dataToRecord):
	keyM = open("keys.txt", "a+")
	
	keyM.write("\n" + dataToRecord)
	
	keyM.close()
	
# Generate key
def newKey(seed):
	random.seed(seed)
	
	# Head section
	head = "".join([Alpha[random.randint(0, len(Alpha)-1)] for x in range(2)])
	sub = alpha[random.randint(0, len(alpha)-1)]
	hNum = numer[random.randint(0, len(numer)-1)]
	# Mid section
	sym = symbo[random.randint(0, len(symbo)-1)]
	# Tail section
	tailHead = alpha[random.randint(0, len(alpha)-1)]
	tailCap = Alpha[random.randint(0, len(Alpha)-1)]
	tailNums = "".join([numer[random.randint(0, len(numer)-1)] for x in range(2)])
	tailEnd = Alpha[random.randint(0, len(Alpha)-1)]
	
	# Compile
	finalKey = head+sub+hNum+sym+tailHead+tailCap+tailNums+tailEnd
	
	return finalKey
