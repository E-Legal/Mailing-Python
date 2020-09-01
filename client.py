# coding=utf-8
import getpass
import optparse
import pickle
import socket
import sys
import util

parser = optparse.OptionParser()
parser.add_option("-a", "--address", action="store", dest="address", default="localhost")
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=1337)
opts = parser.parse_args(sys.argv[1:])[0]

destination = (opts.address, opts.port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect(destination)
s.settimeout(None)

while True:
    option = raw_input("Menu de connexion \n1. Se connecter \n2. Creer un compte \n")
    while option != "1" and option != "2":
        option = raw_input("Veuillez saisir une option valide:\n")
    util.send_msg(s, option)

    if option == "1":
        id = raw_input("Veuillez saisir votre identifiant:\n")
        passw = getpass.getpass("Veuillez saisir votre mot de passe:\n")
        util.send_msg(s, id)
        util.send_msg(s, passw)
        idAnswer = util.recv_msg(s)
        if idAnswer != "0":
            passwAnsw = util.recv_msg(s)
        while idAnswer != "1" or passwAnsw != "1":
            if idAnswer != "1":
                id = raw_input("Veuillez saisir un identifiant valide:\n")
                passw = getpass.getpass("Veuillez saisir votre mot de passe:\n")
            elif passwAnsw == "-1":
                print("Desole, un probleme est survenu.")
                continue
            else:
                print("Ce n'est pas le bon mot de passe. Veuillez reessayer.")
                id = raw_input("Veuillez saisir votre identifiant:\n")
                passw = getpass.getpass("Veuillez saisir votre mot de passe:\n")
            util.send_msg(s, id)
            util.send_msg(s, passw)
            idAnswer = util.recv_msg(s)
            if idAnswer != "0":
                passwAnsw = util.recv_msg(s)



    elif option == "2":
        id = raw_input("Veuillez choisir un identifiant:\n")
        passw = getpass.getpass("Veuillez choisir un mot de passe contenant de 6 à 12 carateres, dont au moins une lettre et un chiffre:\n")
        util.send_msg(s, id)
        util.send_msg(s, passw)
        idAnswer = util.recv_msg(s)
        if idAnswer != "1":
            passwAnsw = util.recv_msg(s)
        while idAnswer != "0" or passwAnsw != "1":
            if idAnswer != "0":
                id = raw_input("Cet identifiant est deja pris, veuillez en choisir un autre:\n")
                passw = getpass.getpass("Veuillez saisir votre mot de passe:\n")
            else:
                print("Ce mot de passe ne respecte pas les conditions, veuillez en choisir un autre.")
                id = raw_input("Veuillez saisir votre identifiant a nouveau:\n")
                passw = getpass.getpass("Veuillez saisir votre nouveau mot de passe:\n")
            util.send_msg(s, id)
            util.send_msg(s, passw)
            idAnswer = util.recv_msg(s)
            if idAnswer != "1":
                passwAnsw = util.recv_msg(s)
        accountCreate = util.recv_msg(s)
        if accountCreate == "0":
            print("Desole, un probleme est survenu")
            continue


    while True:
        option = raw_input("\nMenu principale\n1. Envoi de courriels\n2. Consultation de courriels\n3. Statistiques\n4. Quitter\n")
        while option not in  ["1", "2", "3", "4"]:
            option = raw_input("Veuillez saisir une option valide:\n")

        util.send_msg(s, option)

        if option == "1":
            email_from = id + "@glo2000.ca"
            util.send_msg(s, email_from)

            response = "-1"
            while(response == "-1"):
                email_to = raw_input("\nÀ: ")
                util.send_msg(s, email_to)
                response = util.recv_msg(s)

            subject = raw_input("\nSujet: ")
            util.send_msg(s, subject)
            data = raw_input("\nMessage: ")
            util.send_msg(s, data)

            response = util.recv_msg(s)
            if(response == "-1"):
                print("\nErreur lors de l'envoie du courriel.")
                continue
            else:
                print("\nCourriel envoyé avec succès!")
        elif option == "2":
            util.send_msg(s, id)
            data_string = util.recv_msg(s)
            mails = pickle.loads(data_string)

            print("\nListe de vos courriels: \n")

            compteur = 1;
            for mail in mails:
                print("\n" + str(compteur) + ". " + mail)
                compteur += 1
            if compteur == 1:
                error_check = util.recv_msg(s)
                print(error_check)
            else:
                email_id = raw_input("\nQuel courriel souhaitez-vous visionner? \n")
                util.send_msg(s, email_id)
                email_content = util.recv_msg(s)
                print("\n" + email_content)
                raw_input("\nAppuyez sur Enter pour continuer...")
            continue
        elif option == "3":
            util.send_msg(s, id)

            filesize = util.recv_msg(s)

            data_string = util.recv_msg(s)
            mails = pickle.loads(data_string)

            print("\nNombre de messages: " + str(len(mails)) + "\n")
            print("\nTaille du repertoire personnel (en octets): " + filesize + "\n")
            print("\nListe de vos courriels: \n")

            compteur = 1;
            for mail in mails:
                print("\n" + str(compteur) + ". " + mail)
                compteur += 1
            raw_input("\nAppuyez sur Enter pour continuer...")
            continue
        elif option == "4":
            break;
    s.close()
    exit()