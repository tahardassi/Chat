import wx
import socket
import sys
import time
import threading
import rsa
import re




class MyPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self.hote = "localhost"
		self.port = 12800
		self.rsa = rsa.Rsa(512)
		self.public_key, self.prive_key = self.rsa.gen_rsa_key_pair()
		self.key_server = None


		#création du socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((self.hote, self.port))
		print("Connexion établie avec le serveur sur le port {}".format(self.port))


		self.logger = wx.TextCtrl(self, pos=(0,0), size=(400,500), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RIGHT)
		self.getText = wx.TextCtrl(self, pos=(20,520), size=(240,-1))
		self.sendButton = wx.Button(self, label="Envoyer", pos=(280 ,520))
		#self.Bind(wx.EVT_TEXT, self.Ontest)
		self.Bind(wx.EVT_BUTTON, self.send, self.sendButton)



	
		self.thread = threading.Thread(target=self.rec)
		self.thread.start()


	def Print(self, text):
		wx.CallAfter(self.logger.AppendText, (text + "\n"))



		
	
	def send(self,e):
		texte = self.getText.GetValue()
		if self.key_server:
			msg = self.rsa.rsa_enc(texte, self.key_server)#str(texte).encode('utf-8')
			self.client_socket.send(str(msg).encode('utf-8'))
		else:
			print("ERROR")
		
		self.Print(texte)
		self.getText.Clear()

		
	def rec(self):
		msg_recu = ""
		while 1:
			msg_recu = self.client_socket.recv(1024)
			msg_recu = str(msg_recu.decode('utf-8'))
			if re.search(r"^KEY", msg_recu):
				self.client_socket.send((str(self.public_key[0])+" "+str(self.public_key[1])).encode('utf-8'))
				print("cle client envoyé au serveur", self.public_key)
				print("cle de serveur recu", msg_recu)
				l = msg_recu.split(" ")
				self.key_server = (int(l[1]), int(l[2]))
				continue
			print(msg_recu)
			#déchifrer le message reçu
			msg_recu = self.rsa.rsa_dec(int(msg_recu), self.prive_key)
			self.Print(msg_recu)
			time.sleep(0.05)
