class EndecryAlgo:
	def __init__(self):
		pass
		
	def encryptStr(self,inptstr,let,dire):
		if dire:
			inptstr = let + inptstr
		else:
			inptstr = inptstr + let
		return inptstr

	def decryptStr(self,inptstr, t):
		n = len(inptstr)
		m = n/2
		if t==0:
			if n%2==0:
				m=m-1
		if m<0:
			return "", inptstr
		inptstr = [c for c in inptstr]
		mid = inptstr.pop(m)
		return "".join(inptstr), mid
	
	def encryp(self,data):
		newstr = ""
		c=0
		for aletter in data:
			newstr = self.encryptStr(newstr,aletter,c)
			c = 1-c
		return newstr

	def decryp(self,data):
		decstr = data
		t=0
		if len(decstr)%2==0:
			t=1
		decrypted=""
		for a in range(len(decstr)):
			decstr,mid = self.decryptStr(decstr, t)
			#print "decstr is ",decstr,"mid is",mid
			decrypted=decrypted+mid
		return decrypted
		
if __name__=="__main__":
	e = EndecryAlgo()
	print "encrypted string",e.encryp("sachin123ver456ma")
	d = e.encryp("sachin123ver456ma")
	print "decrypted string",e.decryp(d)