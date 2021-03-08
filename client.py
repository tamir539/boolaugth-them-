from ClientCom import ClientCom
from graphic import screen
import queue
import threading



my_q = queue.Queue()
client = ClientCom('127.0.0.1', 1011, my_q)





def check_server_ans(my_q,screen):
    while True:
        msg = my_q.get()
        if msg == "ok":
            scr.change_state("ok")
        print(msg)



def check_username(username, password):
    client.sendEnc((username+','+password))
    if my_q.get() == 'ok':
        return True
    else:
        return False

def getUsernameAndPassword():
    ok = False
    while not ok:
        try:
            data = scr.getLogin('dog.jpg')

            username = data.split(',')[0]
            password = data.split(',')[1]
            print(username)
            print(password)
            if not check_username(username, password):
                scr.write('this username is already taken! try other one')
            else:
                print(454545)
                if len(password.lstrip().rstrip()) == 0 or len(username.lstrip().rstrip()) == 0:
                    scr.write('enter valid details!')
                else:
                    scr.write(f'welcome {username}!')
                    ok = True
        except Exception as e:
            scr.write('enter valid details!!!!')
    return username , password

client.switch_keys()
print('keys!!!')
scr = screen(client , my_q)

#threading.Thread(target=check_server_ans,args=(my_q,scr,)).start()
''';while True:#client.server_status():
;    if not my_q.empty():
;        msg = my_q.get()
;        print(msg)
;
    username, password = getUsernameAndPassword()
'''