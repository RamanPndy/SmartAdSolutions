class CryptAlgo:
	def __init__(self):
		pass
		
	def encrypt_text(self,text):
		encrypt_string = ""
		index_buff = 13
		handled_special_chars = "@._[<>&*+!#$=({)^`-~?|]}"
		for idx, achar in enumerate(text):
			index = idx + index_buff
			small = ord(achar) - ord('a')
			caps = ord(achar)-ord('A')
			num = ord(achar)-ord('0')
			small_alpha = small>=0 and small<=25
			caps_alpha = caps>=0 and caps<=25
			num_alpha = num>=0 and num<=9
			handled_sc = achar in handled_special_chars
			
			newchar = ""
			if small_alpha:
				newchar = chr(ord('a')+((small+index)%26))
			elif caps_alpha:
				newchar = chr(ord('A')+((caps+index)%26))
			elif num_alpha:
				newchar = chr(ord('0')+((num+index)%10))
			else:
				#case of special characters, do nothing right now
				newchar = achar
				
			encrypt_string = encrypt_string + str(newchar)
		return encrypt_string
		
	def decrypt_text(self,text):
		decrypt_string = ""
		index_buff = 13
		handled_special_chars = "@._[<>&*+!#$=({)^`-~?|]}"
		for idx, achar in enumerate(text):
			index = idx + index_buff
			small = ord(achar) - ord('a')
			caps = ord(achar)-ord('A')
			num = ord(achar)-ord('0')
			small_alpha = small>=0 and small<=25
			caps_alpha = caps>=0 and caps<=25
			num_alpha = num>=0 and num<=9
			newchar = ""
			if small_alpha:
				newchar = chr(ord('a')+((small-index+26)%26))
			elif caps_alpha:
				newchar = chr(ord('A')+((caps-index+26)%26))
			elif num_alpha:
				newchar = chr(ord('0')+((num-index+10)%10))
			else:
				#case of special characters, do nothing right now
				newchar = achar
			decrypt_string = decrypt_string+newchar
		return decrypt_string
if __name__ == "__main__":
	a = CryptAlgo()
	s = "raman.pndy@gmail.com"
	print a.encrypt_text(a.decrypt_text(s))
	print a.decrypt_text("eobqe.ihyu@elajn.gts")
	print a.decrypt_text("1111ywefj")
	print a.decrypt_text("o234v1vy1aa2")
	print a.decrypt_text("xzb135")
	print a.decrypt_text(a.decrypt_text("1111ywefjgik024d789k6kn6pp7"))