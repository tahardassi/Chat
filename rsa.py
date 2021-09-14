from Crypto.Util.number import getPrime
from Crypto.Util.number import inverse
from math import gcd
import sys
import hashlib



class Rsa:
	def __init__(self, bits):
		self.bits = bits
	def gen_rsa_key_pair(self) :
		p = getPrime(int(self.bits/2))
		q = getPrime(int(self.bits/2))
		n = p * q
		phi_n = (p-1)*(q-1)
		e = 65537
		assert(gcd(e, phi_n) == 1)
		d = inverse(e, phi_n)
		return ((e,n) , (d,n))

	def rsa(self, clear, key) :
		return pow(clear, key[0], key[1])

	def rsa_enc(self, clear, key):
		byte = int.from_bytes(clear.encode('utf-8'),'big')
		return self.rsa(byte, key)

	def rsa_dec(self, encrypted, key):
		clear = self.rsa(encrypted, key)
		return clear.to_bytes((clear.bit_length() + 7) // 8, 'big').decode('utf-8')


	def h(self,nb):
		byte = nb.to_bytes ((nb.bit_length() + 7) // 8, 'big')
		hash_ = hashlib.sha256()
		hash_.update(byte)
		return int.from_bytes(hash_.digest(), 'big')

	def rsa_sign(self, message, key) :
		b = int.from_bytes(message.encode('utf-8'),'big')
		return (pow(self.h(b), key[0], key[1]))

	def rsa_verify(self, message, signed, key) :
		b = int.from_bytes(message.encode('utf-8'),'big')
		hash_ = pow(signed, key[0], key[1])
		if self.h(b) == hash_:
			return True 
		return False


if __name__ == "__main__":
	rsa = Rsa(512)
	public, prive = rsa.gen_rsa_key_pair()
	c = rsa.rsa_enc("salut les nuls", public)
	print(c)
	m = rsa.rsa_dec(c, prive)
	print(m)
	s = rsa.rsa_sign(str(c), prive)
	print(rsa.rsa_verify(str(c), s, public))


