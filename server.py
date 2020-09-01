# coding=utf-8
import optparse
import os.path
import pickle
import re
import smtplib
import socket
import sys
import util
from email.mime.text import MIMEText

parser = optparse.OptionParser()
parser.add_option("-a", "--address", action="store", dest="address", default="localhost")
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=1337)
opts = parser.parse_args(sys.argv[1:])[0]

destination = (opts.address, opts.port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(destination)
server_socket.listen(5)
print("Ecoute sur le port " + str(server_socket.getsockname()[1]))
Connectionnb = 0
Disconnectnb = 0

while True:
    (s, address) = server_socket.accept()
    Connectionnb += 1
    print(str(Connectionnb) + "e connexion au serveur")

    option = util.recv_msg(s)

    if option == "1":

        id = util.recv_msg(s)
        mdp = util.recv_msg(s)
        checkUsername = util.Usernamecheck(id)
        util.send_msg(s, checkUsername)
        if checkUsername != "0":
            checkPassw = util.connexion(id, mdp)
            util.send_msg(s, checkPassw)

        while checkUsername != "1" or checkPassw != "1":
            id = util.recv_msg(s)
            mdp = util.recv_msg(s)
            checkUsername = util.Usernamecheck(id)
            util.send_msg(s, checkUsername)
            if checkUsername != "0":
                checkPassw = util.connexion(id, mdp)
                util.send_msg(s, checkPassw)
        if checkPassw == "-1":
            continue


    elif option == "2":
        id = util.recv_msg(s)
        mdp = util.recv_msg(s)
        checkUsername = util.Usernamecheck(id)
        util.send_msg(s, checkUsername)
        if checkUsername != "1":
            checkPassw = util.Passwcheck(mdp)
            util.send_msg(s, checkPassw)
        while checkUsername != "0" or checkPassw != "1":
            id = util.recv_msg(s)
            mdp = util.recv_msg(s)
            checkUsername = util.Usernamecheck(id)
            util.send_msg(s, checkUsername)
            if checkUsername != "1":
                checkPassw = util.Passwcheck(mdp)
                util.send_msg(s, checkPassw)
        checkError = util.createAccount(id, mdp)
        util.send_msg(s, checkError)
        if checkError == "0":
            continue



    while True:
        option = util.recv_msg(s)

        if option == "1":
            emailFrom = util.recv_msg(s)
            emailAddress = util.recv_msg(s)
            while not re.search(r"^[^@]+@[^@]+\.[^@]+$", emailAddress):
                msg = "-1"
                util.send_msg(s, msg)
                emailAddress = util.recv_msg(s)
            msg = "0"
            util.send_msg(s, msg)

            subject = util.recv_msg(s)
            data = util.recv_msg(s)
            courriel = MIMEText(data)
            courriel["From"] = emailFrom
            courriel["To"] = emailAddress
            courriel["Subject"] = subject

            use_smtp_ulaval = False
            if re.match(r"^[^@]+@glo2000\.ca$", emailAddress) == None:
                use_smtp_ulaval = True

            if use_smtp_ulaval == True:

                try:
                    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
                    smtpConnection.sendmail(courriel["From"], courriel["To"], courriel.as_string())
                    smtpConnection.quit()
                    msg = "0"
                    util.send_msg(s, msg)
                except:
                    msg = "-1"
                    util.send_msg(s, msg)
            else:
                folder_path = emailAddress.replace("@glo2000.ca", "")
                check = util.fileOpen(folder_path, courriel['Subject'], courriel.as_string())
                if check != "0":
                    util.mailTrash(courriel['Subject'], courriel.as_string())
                util.send_msg(s, check)

        elif option == "2":
            id = util.recv_msg(s)
            files = os.listdir(id)
            files.remove("config.txt")
            files = util.sortDate(id, files)
            mails = []

            for file in files:
                file = file.replace(".txt", "")
                mails.append(file)

            data_string = pickle.dumps(mails)
            util.send_msg(s, data_string)

            if len(files) == 0:
                util.send_msg(s, "Vous avez aucun courriel\n")
            else:
                email_id = int(util.recv_msg(s)) - 1
                if email_id < len(files) and email_id > 0:
                    email_content = util.mailOpen(id, files[email_id])
                    util.send_msg(s, email_content)
                else:
                    util.send_msg(s, "Aucun mail avec cette id\n")

        elif option == "3":
            id = util.recv_msg(s)
            filesize = util.getSize(id)
            util.send_msg(s, str(filesize))
            files = os.listdir(id)
            files.remove("config.txt")
            files = sorted(files, key=str)
            mails = []

            for file in files:
                file = file.replace(".txt", "")
                print(file)
                mails.append(file)

            data_string = pickle.dumps(mails)
            util.send_msg(s, data_string)

        elif option == "4":
            Disconnectnb += 1
            print(str(Disconnectnb) + "e deconnexion au serveur")
            break