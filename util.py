# coding=utf-8
import os.path
import re
import struct
from hashlib import sha256
from os.path import getsize

def createAccount(id, mdp):
    state = "1"
    try:
        os.makedirs(id)
        file = open(id + "/config.txt", "w")
        file.write(sha256(mdp.encode()).hexdigest())
        file.close()
    except:
        state = "0"
    return state


def Usernamecheck(id):
    state = "0"
    if os.path.exists(id + "/config.txt"):
        state = "1"
    return state


def Passwcheck(mdp):
    state = "0"
    if (re.search(r"^[a-zA-Z0-9]{6,12}$", mdp) and re.search(r".*[0-9].*", mdp) and re.search(r".*[a-zA-Z].*", mdp)):
        state = "1"
    return state


def connexion(id, mdp):
    state = "1"
    try:
        file = open(id + "/config.txt", "r")
        password = file.readline()
        file.close()
        if sha256(mdp.encode()).hexdigest() != password:
            state = "0"
    except:
        state = "-1"

    return state

def fileOpen(id, subject, data):
    state = "0"
    try:
        file = open(id + "/" + subject + ".txt", "w")
        file.write(data)
        file.close()
        state = "0"
    except:
        state = "-1"

    return state


def mailOpen(id, filename):
    try:
        file = open(id + "/" + filename, "r")
        str_content = file.read();
        file.close()
        return str_content
    except:
        print("Fichier introuvable.")


def mailTrash(subject, data):
    try:
        if not os.path.exists("DESTERREUR"):
            os.makedirs("DESTERREUR")
        file = open("DESTERREUR/" + subject + ".txt", "w")
        file.write(data)
        file.close()
    except:
        print("Une erreur c'est produit.")


def getSize(id):
    try:
        size = getsize(id)
        return size
    except:
        print("Mauvais nom de repertoire")


def sortDate(id, liste):
    liste.sort(key=lambda x: os.path.getmtime(id + "/" + x))
    return liste

def recvall(socket, count):
    buf = b""
    while count > 0:
        newbuf = socket.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def send_msg(socket, message):
    message = message.encode()
    socket.sendall(struct.pack('!I', len(message)))
    socket.sendall(message)


def recv_msg(socket):
    length, = struct.unpack('!I', recvall(socket, 4))
    return recvall(socket, length).decode()
