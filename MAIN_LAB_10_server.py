import Server_FUNCS_LAB_10
import os.path
import threading
import mmap
import time
import socket
import sys

lock = threading.Lock()
server_port = 0
server_ip = ''
thread_list = []
fFuncs = Server_FUNCS_LAB_10.FileHandling()
files_being_processed = []

def function_calls(command,clint):
    # print(command)
    wait_check = 0
    if  command[0] != 'file_check' and command[0] != 'mk':
        while True:
            lock.acquire()
            if command[1] in files_being_processed:
                lock.release()
                time.sleep(2)
            else:
                files_being_processed.append(command[1])
                lock.release()
                break
            if wait_check == 10:
                clint.send('#OBKKDPPGYFTTEK#'.encode())
                return
            clint.send('#TIEWCFSTOCTTTWFS#'.encode())
            wait_check += 1
            
    if command[0] == 'mk':
        try:
            fFuncs.create_file(command[1])
            clint.send('Done'.encode())
        except:
            clint.send('Fail'.encode())
    elif command[0] == 'delete':
        try:
            fFuncs.delete_file(command[1])
            clint.send('Done'.encode())
        except:
            clint.send('Fail'.encode())
    elif command[0] == 'read':
        time.sleep(1000)
        clint.send(fFuncs.read_file(command[1]).encode())
        time.sleep(1)
        clint.send('N'.encode())        
    elif command[0] == 'write':
        try:
            time.sleep(10)
            fFuncs.write_file(command[1], command[2], command[3])
            clint.send('Done'.encode())
        except:
            clint.send('Fail'.encode())
    elif command[0] == 'ls':
        try:
            clint.send(fFuncs.list_files_and_folders_in_current(command[1]).encode())
        except:
            clint.send('Fail'.encode())
    elif command[0] == 'lsall':
        try:
            clint.send(fFuncs.show_mmap().encode())
        except:
            clint.send('Fail'.encode())
    elif command[0] == 'mv':
        try:
            fFuncs.move_file(command[1], command[2])
            clint.send('Done'.encode())
        except:
            clint.send('Fail'.encode())
    elif command[0] == 'mvdata':
        try:
            clint.send(fFuncs.move_data(command[1], command[2], command[3], command[4]).encode())
        except:
            clint.send('Unkown Error'.encode())
    elif command[0] == 'trdata':
        try:
            clint.send(fFuncs.truncate_data(command[1], command[2]).encode())
        except:
            clint.send('Unkown Error'.encode())
    elif command[0] == 'file_check':
        if fFuncs.check_if_file_exist(clint_commands[1]):
            clint.send('true'.encode())
        else:
            clint.send('false'.encode())
    
    if  command[0] != 'file_check' and command[0] != 'mk':
        lock.acquire()
        files_being_processed.remove(command[1])
        lock.release()

if __name__ == "__main__":
    server_port = int(input("Enter The Port Number  : "))
    server_name = socket.gethostname()
    server_ip = socket.gethostbyname(server_name)
    # server_port = 95
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_socket.bind((server_ip,server_port))
            server_socket.listen(5)
            print('...SOCKET UP AND RUNNING...')
            print('ip:',server_ip)
            print('port:',server_port)
            continuty_check = 0
        except socket.error as err:
            continuty_check+=5
            print('Error:',err,'\nWhile creating socket at',server_name,'With IP',server_ip,'\n...RETYRING IN',continuty_check,'SECENDS...')
        if continuty_check == 50:
            sys.exit('...10 UNSUCESSFULL ATTEMPTS...\n...EXITING PROGRAM...')
        elif continuty_check == 0:
            while True:
                clint,clint_add = server_socket.accept()
                clint_command = clint.recv(1024)
                clint_command = clint_command.decode()
                if len(clint_command) == 0:
                    continue
        
                clint_commands = clint_command.split(' ') 
                print (clint_commands,clint_add)
                
                if clint_commands[0] == 'write':
                    data_recived = ''
                    while True:
                        incoming =  clint.recv(10000).decode()
                        if incoming == '#EODFTFSFC#':
                            break
                        data_recived += incoming
                    clint_commands.append(data_recived)

                thread = threading.Thread(target=function_calls, args=(clint_commands,clint,))
                thread_list.append(thread)
                thread.start()
        
        time.sleep(continuty_check)
    
    for thread in thread_list:
        thread.join()      
#END