import socket,time


class Scanner:
    def __init__(self, filepath='/tmp/output.txt'):
        self.Tab_personalised_port = []
        #Initialisation des ports connus
        self.Useful_ports = []
        self.Description_ports = []
        Ports = open("TCP_PORT.txt", 'r')
        for port in Ports:
            port = port.rstrip('\n')
            espace = port.index(' ')
            self.Useful_ports.append(int(port[:espace]))
            self.Description_ports.append(port[espace+1:])
        ## fin initialisation
        self.Filepath = filepath
        Resultat = open(filepath ,'w')
        Resultat.truncate(0)

    # -----------------------------------------------------------------------------------------------------
    # Ajouter un port dans notre liste port à tester
    # -----------------------------------------------------------------------------------------------------
    def add_port(self, port):
        self.Tab_personalised_port.append(port)

    # -----------------------------------------------------------------------------------------------------
    # Scan tous les ports connues
    # -----------------------------------------------------------------------------------------------------
    def scan_all(self, host):
        tab_port = self.Useful_ports
        for port in tab_port:
            My_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            My_Socket.settimeout(0.3)
            result = My_Socket.connect_ex((host, port))
            if(result == 0):
                self.Write(f"PORT [{port}] ouvert -> {self.Description_ports[self.Useful_ports.index(port)]}", self.Filepath)
                #print(f"PORT [{port}] ouvert -> {self.Description_ports[self.Useful_ports.index(port)]}")
                My_Socket.close()

    # -----------------------------------------------------------------------------------------------------
    # Scan les ports ajouter dans notre tableau
    # -----------------------------------------------------------------------------------------------------
    def scan_perso(self, host):
        for port in self.Tab_personalised_port:
            My_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            My_Socket.settimeout(0.5)
            result = My_Socket.connect_ex((host, port))
            time.sleep(0.3)
            if (result == 0):
                self.Write(f"PORT [{port}] ouvert -> {self.Description_ports[self.Useful_ports.index(port)]}", self.Filepath)
                #print(f"PORT [{port}] ouvert ")
                My_Socket.close()

    # -----------------------------------------------------------------------------------------------------
    # Scan les ports dans une range d'entier
    # -----------------------------------------------------------------------------------------------------
    def scan_range(self, host, lowerport, upperport):
        for port in range(lowerport,upperport):
            My_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            My_Socket.settimeout(0.3)
            result = My_Socket.connect_ex((host, port))
            if (result == 0):
                self.Write(f"PORT [{port}] ouvert -> {self.Description_ports[self.Useful_ports.index(port)]}", self.Filepath)
                #print(f"PORT [{port}] ouvert ")
                My_Socket.close()

    # -----------------------------------------------------------------------------------------------------
    # Ecrire dans un fichier de sortie
    # -----------------------------------------------------------------------------------------------------
    def Write(self, string, filepath='/tmp/output.txt'):
        Resultat = open(filepath ,'a')
        Resultat.write(string +"\n")


def main():
    myscan = Scanner("Resultat.txt")
    myscan.add_port(80)
    myscan.add_port(22)

    myscan.scan_perso("scanme.nmap.org")


if (__name__ == '__main__'):
    main()
