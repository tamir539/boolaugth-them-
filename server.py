from my_AES import AESCipher
from my_RSA import RSAClass
import socket
import threading
from DBlogin import DB
import select
import hashlib
import random
import string
import time

global  votes_for_bullshit
votes_for_bullshit = 0
global votes_for_laugh
votes_for_laugh = 0

global started
started = False

global answers
answers = {}    #socket -->> his answer

vote_by_socket = {} #socket --> vote
open_clients = {}  # client-socket : ip
key_by_soc = {}    # socket -> client AES key
username_by_soc = {}    # socket -> client username
readys = []     #all the sockets that ready now

checking = False
connecting_now = [] #sockets that now CONECTING

def swich_keys():
    '''

    :param soc: client socket
    :return: send the AES key safely to the client with RSA
    '''
    while True:
        try:
            for soc in open_clients.keys():
                if soc not in key_by_soc.keys() and soc not in username_by_soc.keys():
                    client_key = get_public_key(soc)
                    k = set_key(soc)
                    soc.send(myRsa.encrypt_msg(k, client_key))
                    key_by_soc[soc] = k
        except Exception as e:
            print('swiche keys' , str(e))

def get_public_key(soc):
    '''

    :param soc: client socket
    :return: get the public key of the client
    '''
    try:
        k = soc.recv(1024)
    except Exception as e:
        print('get pub key', str(e))
        close_client(soc)

    return k

def set_key(soc):
    '''

    :param soc: client socket
    :return: create for the client AES key
    '''
    #create a random key
    s = string.ascii_lowercase
    s = ''.join(random.sample(s, len(s)))
    while s in key_by_soc.values():
        s = string.ascii_lowercase
        s = ''.join(random.sample(s, len(s)))


    return s

def fromAes(soc, sen):
    '''

    :param sen: encoded sentens
    :return: the sentens after decoding
    '''
    key = AESCipher(key_by_soc[soc])
    msg = key.decrypt(sen)
    return msg

def hash_password(password):
    '''

    :param password:
    :return: the password after hashing
    '''
    pas = hashlib.md5(password.encode())
    return pas.hexdigest()

def delete_client(soc):
    del open_clients[soc]
    del key_by_soc[soc]
    del username_by_soc[soc]
    del vote_by_socket[soc]

#enter - client socket to close
#exit - remove the client socket and remove it from all lists
def close_client(client_soc):
    global votes_for_laugh
    global votes_for_bullshit

    print("in close soc ",client_soc)


    notice_someone_left(client_soc)
    if client_soc in vote_by_socket.keys():
        if vote_by_socket[client_soc] == 'bullshit':
            votes_for_bullshit = votes_for_bullshit - 1
        else:
            votes_for_laugh = votes_for_laugh - 1
    if client_soc in open_clients.keys():
        print(f"{open_clients[client_soc]} - disconnected")
        del open_clients[client_soc]
        client_soc.close()
    if client_soc in username_by_soc.keys():
        del username_by_soc[client_soc]
    if client_soc in key_by_soc.keys():
        del key_by_soc[client_soc]

def send_to_all(msg):
    '''

    :param msg: msg
    :return: send the msg to all the client
    '''
    for s in open_clients.keys():
        try:
            s.send(msg.encode())
        except:
            close_client(s)

def check_start():
    global votes_for_laugh
    global votes_for_bullshit
    global started

    if len(username_by_soc.keys()) < 2:
        start = False
    else:
        start = True
        for s in username_by_soc.keys():
            if s not in readys:
                start = False
    if start:
        #start the game
        send_to_all('start')
        print('starting!!!!!')
        print(votes_for_bullshit)
        print(votes_for_laugh)
        if votes_for_bullshit > votes_for_laugh:
            print('starting bulshit!!!!')
        else:
            print('starting laugh!!!')
        started = True
        game()


def game():
    quest = "What is Obama's last name?"
    send_to_all(quest)
    print(quest)


def get_ready(soc, sen):
    '''

    :param soc: client socket
    :param sen: sentems
    :return: check if the client sent ready or unready
    '''
    global votes_for_laugh
    global votes_for_bullshit

    sen = sen[1:]

    mode = sen.split(',')[1]
    is_ready = sen.split(',')[0]
    print('is ready -- >', is_ready)
    print('mode!!!!', mode)
    if is_ready == 'ready':
        print('inn ready!!')
        readys.append(soc)
        if mode == 'bullshit':
            vote_by_socket[soc] = 'bullshit'
            votes_for_bullshit = votes_for_bullshit + 1
        elif mode == 'laugh':
            vote_by_socket[soc] = 'laugh'
            votes_for_laugh = votes_for_laugh + 1
    elif is_ready == 'unready':
        if vote_by_socket[soc] == 'bullshit':
            votes_for_bullshit = votes_for_bullshit - 1
        else:
            votes_for_laugh = votes_for_laugh - 1
        readys.remove(soc)

def getAnswer(soc,sen):
    global answers
    sen = sen[1:]
    print(sen)
    answers[soc] = sen
    if len(answers.keys()) == len(username_by_soc.keys()):  #means that everyone answerd
        print(','.join(answers.values()))
        send_to_all(','.join(answers.values()))




def get_msg(soc):
    '''

    :param soc: client socket
    :return: get msg from the client and take care the request
    '''
    global votes_for_laugh
    global votes_for_bullshit
    try:
        if soc in key_by_soc.keys() and soc in username_by_soc.keys():
            msg = soc.recv(1024)
            sen = fromAes(soc, msg)

    except Exception as e:
        print('get msg ->>>>>> ', str(e))
        close_client(soc)
    else:
        print('sen --> ', sen)
        func_by_com[sen[0]](soc, sen)

def send_who_in(soc):
    for name in username_by_soc.values():
        print(name)
        soc.send(name.encode())

def notice_someone_joined(soc):
    name = username_by_soc[soc]
    for s in username_by_soc.keys():
        if s != soc:
            s.send(name.encode())

def notice_someone_left(soc):
    if soc in username_by_soc.keys():
        name = username_by_soc[soc]
    for s in username_by_soc.keys():
        if s != soc:
            name = '!'+ name
            try:
                s.send(name.encode())
            except:
                close_client(s)

def get_username_password(soc):
    '''

        :param soc: client socket
        :return: get msg from the client and take care the request
        '''
    username = ''
    password = ''
    try:
        if soc in key_by_soc.keys():
            msg = soc.recv(1024)
            sen = fromAes(soc, msg)
            username = sen.split(',')[0]
            password = sen.split(',')[1]
    except Exception as e:
        pass

    return username, password

def check_new_usernames():
    '''

    :param soc: socket of the client
    :param username: username
    :param password:
    :return: add the client to the data base by his username and password
    '''

    myDB = DB("logins")
    while True:
        for soc in list(open_clients):
            if soc not in username_by_soc.keys() and soc in key_by_soc.keys() and soc not in connecting_now:
                connecting_now.append(soc)
                threading.Thread(target = check_username, args = (soc,)).start()

def check_username(soc):
    global  started

    myDB = DB("logins")
    username, password = get_username_password(soc)
    if username != '':
        if not started:
            pas = hash_password(password)
            check = myDB.add_user(username, pas)
            if check:
                soc.send('ok'.encode())
                username_by_soc[soc] = username
                send_who_in(soc)
                notice_someone_joined(soc)
            else:
                print(check)
                soc.send('no'.encode())
        else:
            soc.send('os'.encode())     #notice the client that the game has allready started
    connecting_now.remove(soc)


func_by_com = {'1': get_ready, '2': getAnswer}
myRsa = RSAClass()
public_key = myRsa.get_public_key_pem()

server_soc = socket.socket()
server_soc.bind(('0.0.0.0',1011))
server_soc.listen(3)

print('ready')

threading.Thread(target = swich_keys, args = ()).start()
threading.Thread(target = check_new_usernames, args = ()).start()

while True:
    rlist, wlist, xlist = select.select(list(open_clients.keys())+[server_soc],list(open_clients.keys()),[],0.3)
    for current_socket in rlist:
        if current_socket is server_soc:
            # new client
            client, address = server_soc.accept()
            print(f'{address[1]} - connected')
            open_clients[client] = address[1]
        else:
            # receive data from exist client
            try:
                ##if the client havent AES key yet, give him one
                if current_socket not in key_by_soc.keys() or current_socket not in username_by_soc.keys() :
                    pass
                else:
                    #pass
                    get_msg(current_socket)
            except Exception as e:
                print('ggggggg', str(e))
                close_client(current_socket)
    if not started:
        check_start()




server_soc.close()