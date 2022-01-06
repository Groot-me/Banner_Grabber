import socket, time, os, sys, shutil
from Sockets import Scanner

class Grabber:

    # -----------------------------------------------------------------------------------------------------
    # Ouvre le fichier en question et renvoie son contenu, si aucun contenu alors on arrete la
    # -----------------------------------------------------------------------------------------------------
    def open_file_with_open_port(self, Fichier):
        fichier = open(Fichier,"r")

        #test si il ya au moins 1 port
        line = fichier.readline()
        if not line:
            print("Aucun port d'ouvert... Fermeture du programme...")
            sys.exit("Aucun port d'ouvert... Fermeture du programme...")
        else:
            fichier = open(Fichier, "r")
            return fichier

    # -----------------------------------------------------------------------------------------------------
    # Ecris les ports du fichier.txt dans mon tableau de port
    # -----------------------------------------------------------------------------------------------------
    def Write_Open_Port(self):
        fichier = self.open_file_with_open_port("Resultat.txt")

        for line in fichier:
            index1 = line.index('[')
            index2 = line.index(']')
            #Ajout dans mon tableau et transformation des ports en entiers
            self.List_port_open.append(int(line[index1+1:index2]))

    # -----------------------------------------------------------------------------------------------------
    # Init
    # -----------------------------------------------------------------------------------------------------
    def __init__(self, Host):
        self.List_port_open = []
        self.Host = Host
        self.My_Socket = 0
        self.scanner = Scanner.Scanner("Resultat.txt")
        self.scanner.scan_all(Host) # scan d'apres les ports les plus connus
        #self.scanner.scan_range(Host,10,150) #scan sur une range de port

        #Ajout des ports ouvert dans notre tableau
        self.Write_Open_Port()

        # Creation du répertoire pour y ajouter les bannieres
        self.ip_directory = 0
        self.ip_direcory = self.Create_Directory(Host)
        #copie du fichier avec les ports ouverts dans le repertoire x.x.x.x
        os.popen('cp Resultat.txt \\'+ self.ip_direcory)

        #Creation du fichier texte grabber.txt
        self.My_Fic_Grabber = self.Create_grabber_txt(self.ip_direcory)

        #Ecoute sur les ports
        self.listening()

    # -----------------------------------------------------------------------------------------------------
    # Creation de mon repertoire
    # -----------------------------------------------------------------------------------------------------
    def Create_Directory(self, Host):

        #Recuperation de l'addresse ip de l'hote
        ip = socket.gethostbyname(Host)
        try:
            os.mkdir(ip)
        except:
            #supprime le repertoire meme si il n'est pas vide
            shutil.rmtree(ip)
            try:
                os.mkdir(ip)
            except:
                print("impossible de créer le fichier !")
                return 0

        print("Repertoire crée")
        return ip
    # -----------------------------------------------------------------------------------------------------
    # Creation de mon fichier texte qui va contenir les bannieres
    # -----------------------------------------------------------------------------------------------------
    def Create_grabber_txt(self,ip):
        try:
            Fichier = open(ip+"/Grabber.txt",'w+')
        except:
            print("Impossible de créer le fichier !")
            sys.exit("Impossible de créer le fichier !")

        return Fichier
    # -----------------------------------------------------------------------------------------------------
    # Ecris dans le fichier Grabber.txt tt simplemenbt
    # -----------------------------------------------------------------------------------------------------
    def Write_in_fic(self,Data):
        self.My_Fic_Grabber.write(Data+'\n')

    # -----------------------------------------------------------------------------------------------------
    # Se connecte à l'hote pour établir la connection TCP
    # -----------------------------------------------------------------------------------------------------
    def connexion(self, port):
        self.My_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.My_Socket.settimeout(0.5)
        print("Connecting to :",self.Host, "on port :",port)
        try:
            self.My_Socket.connect((self.Host, port))
        except:
            print("impossible de se conecter au port : ",port)

    # -----------------------------------------------------------------------------------------------------
    # Ecoute l'Hote sur le(s) ports actifs
    # -----------------------------------------------------------------------------------------------------
    def listening(self):

        # Send some data to remote server
        message = "a\r\n\r\n"

        for port in self.List_port_open:
            #connexion avec le bon port
            self.connexion(port)
            #ajout d'un message pour savoir a quel port la banniere correspond
            self.Write_in_fic("Banner sur le port : "+ str(port))

            #essaie d'envoyer un msg
            try:
                self.My_Socket.sendall(message.encode('utf-8'))
                print('Message send successfully')
                time.sleep(0.5)

                #reception de la reponse du serveur
                reply = self.My_Socket.recv(4096).decode()

                if not reply:
                    print("Aucune donnée reçu ...")
                    self.My_Socket.close()

                #print(reply)
                #ecriture de la reponse dans notre fichier texte
                self.Write_in_fic(reply)

                #fermeture de la socket
                self.My_Socket.close()

                # Mise en forme du fichier texte
                self.Write_in_fic("-" * 20)
                self.Write_in_fic(" ")

            except socket.error:
                #envoie échoué
                print('Envoie échoué')
                self.Write_in_fic("Connexion au port échoué")
                self.Write_in_fic("-" * 20)
                self.Write_in_fic(" ")
                pass

def main():
    Grabber("10.129.184.37")



if (__name__ == '__main__'):
    main()



