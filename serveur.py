import socket
import select
import sys
import time
import re
import rsa
from threading import Thread

class Identifier(Thread):
    def __init__(self, clients, keys, key, rsa, connexion):
        Thread.__init__(self)
        self.clients  = clients
        self.connexion = connexion
        self.username = None
        self.keys = keys
        self.public_key = key[0]
        self.prive_key = key[1]
        self.rsa = rsa


    def run(self):
        #envoie de la clé public du serveur
        self.connexion.send(("KEY " + str(self.public_key[0])+" "+str(self.public_key[1])).encode('utf-8'))
        #recevoir la clé public du client
        keyp_client = (self.connexion.recv(1024)).decode('utf-8')
        l = keyp_client.split(' ')
        keyp_client = (int(l[0]),int(l[1]))
        #clé public recu, on peut commencer à chifrer

        msg_envo = "WHO?"
        client_exist = "EXIST"
        msg_envo = self.rsa.rsa_enc(msg_envo, keyp_client)
        client_exist = self.rsa.rsa_enc(client_exist, keyp_client)
        inconito = True
        while(inconito):
            #envoie demande d'identification
            self.connexion.send(str(msg_envo).encode('utf-8'))
            
            #recevoir l'identifiant
            iden = self.connexion.recv(1024)
            iden = iden.decode('utf-8')
            
            #dechifrer le message reçu
            iden = self.rsa.rsa_dec(int(iden), self.prive_key)

            #traitement du message reçu       
            if re.search(r"^IAM [a-z]", iden):
                iden = str(iden[4 :len(iden)])
                if iden in self.clients.keys():
                    #identifiant déjà existant 
                    self.connexion.send(str(client_exist).encode('utf-8'))
                    #self.connexion.close()
                    continue
                #ajout du client avec son identifiant
                self.clients[iden] = self.connexion
                self.username = iden
                inconito = False

        #ajout de la clé public du client    
        self.keys[self.username] = keyp_client
        #affichage des clients et de leurs clés
        print (self.clients)
        print(self.keys)
        return 0

    def getUsername(self):
        return self.username


class Chat(Thread):
    def __init__(self, clients, keys, connexion):
        Thread.__init__(self)
        self.clients = clients
        self.connexion = connexion
        self.keys = keys
        self.rsa = rsa.Rsa(512)
        self.key = self.rsa.gen_rsa_key_pair()


    def run(self):
        iden = Identifier(self.clients, self.keys, self.key, self.rsa, self.connexion)
        iden.start()
        iden.join()
        username = iden.getUsername()
        dest = None
        if not username:
            print("identification non réussite")
            return 0
        msg_recu = None
        
        start = True
        while start:
            msg_envo = ""
            msg_recu = self.connexion.recv(1024)
            msg_recu = msg_recu.decode('utf-8')
            msg_recu = self.rsa.rsa_dec(int(msg_recu), self.key[1])
            print(msg_recu)
            if re.match(r"^OUT$", msg_recu):
                del self.clients[username]
                self.connexion.close()
                print("{} a quitté".format(username))
                start = False
                

            elif re.search(r"^LST$", msg_recu):
                for client in self.clients.keys():
                    msg_envo += str(client+'\n')
                msg_envo = self.rsa.rsa_enc(msg_envo, self.keys[username])
                self.connexion.send(str(msg_envo).encode('utf-8'))

            #for client in self.clients.keys():
            elif re.search(r"^PRV ", msg_recu):
                l = msg_recu.split(' ')
                dest = l[1]
                if dest in self.clients.keys():
                    msg_recu = " ".join(l[2:])
                    msg_envo = username+ " : "+ msg_recu
                    msg_envo = self.rsa.rsa_enc(msg_envo, self.keys[dest])
                    self.clients[dest].send(str(msg_envo).encode('utf-8'))
                else:
                    msg_envo = "NO DEST"
                    msg_envo = self.rsa.rsa_enc(msg_envo, self.keys[username])
                    self.connexion.send(str(msg_envo).encode('utf-8'))
                    continue
            else:
                msg_envo = "NO REQUEST"
                msg_envo = self.rsa.rsa_enc(msg_envo, self.keys[username])
                self.connexion.send(str(msg_envo).encode('utf-8'))
                continue
        return 0

                  

class Server:
    def __init__(self, hote = '', port = 12800):
        self.hote = hote
        self.port = port
        self.start = True
        self.clients = dict()
        self.keys = dict()
        self.to_read = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.hote, self.port))
        self.server_socket.listen(5)
        print("Le serveur écoute sur le port {}".format(self.port))


        while self.start:
            demandes, wlist, xlist = select.select([self.server_socket],[],[], 0.05)
            for connexion in demandes:
                client_soket, client_infos = connexion.accept()
                chat = Chat(self.clients, self.keys, client_soket)
                chat.start()

serveur = Server() 