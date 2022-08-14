import SERVER_FUNCS
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
fFuncs = SERVER_FUNCS.FileHandling()
files_being_processed = []
server_thread_kill = False

# Start part of changes for last lab

clint_working_on_file = []
clints_list_working_on_file = []
no_of_clints_reading_file = []

# End part of changes for last lab

def join_threads():
    print('\n\t...Please wait till we complete clints requests...\n')
    n = len(thread_list)
    for x in thread_list:
        print('Left:',n)
        x.join()
        n-1

def server_control():
    while True:
        inp = input()
        if inp == 'check':
            print(getThreadsAlive())
        elif inp == 'exit':
            closeServer()
            break

def getThreadsAlive():
    return threading.active_count()

def closeServer():
    global server_thread_kill
    server_thread_kill = True
    temp_clint_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    temp_clint_socket.connect_ex((server_ip,server_port))
    temp_clint_socket.close()

def function_calls(command,clint):
    # Start part of changes for last lab
    wait_check = 0
    read_type_command = False
    
    index = 0
    if command[0] != 'file_check' and command[0] != 'mk' and command[0] != 'lsall' and command[0] != 'ls' :
        lock.acquire()
        if command[1] not in clint_working_on_file:
            clint_working_on_file.append(command[1])
            clints_list_working_on_file.append([])
            no_of_clints_reading_file.append(0)
        
        index = clint_working_on_file.index(command[1])
        clints_list_working_on_file[index].append(clint)
        lock.release()

        while True:
            lock.acquire()
            if command[1] not in files_being_processed and clint == clints_list_working_on_file[index][0]:
                
                if command[0] == 'read':
                    clints_list_working_on_file[index].pop(0)
                    no_of_clints_reading_file[index] = no_of_clints_reading_file[index] + 1
                    lock.release()
                    break
                elif no_of_clints_reading_file[index] == 0:
                    clints_list_working_on_file[index].pop(0)
                    files_being_processed.append(command[1])
                    lock.release()
                    break
            
            lock.release()
            
            if wait_check == 10:
                clint.send('#OBKKDPPGYFTTEK#'.encode())
                return
            clint.send('#TIEWCFSTOCTTTWFS#'.encode())
            
            time.sleep(2)
            wait_check += 1
            
    # End part of changes for last lab
            
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
        clint.send(fFuncs.read_file(command[1]).encode())
        clint.send('#TIEECFTDOFSBS#'.encode())
    elif command[0] == 'write':
        try:
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
        if fFuncs.check_if_file_exist(command[1]):
            clint.send('true'.encode())
        else:
            clint.send('false'.encode())
    
    # Start part of changes for last lab
    if  command[0] != 'file_check' and command[0] != 'mk' and command[0] != 'read' and command[0] != 'lsall' and command[0] != 'ls' :
        lock.acquire()
        files_being_processed.remove(command[1])
        lock.release()
        
    if command[0] == 'read':
        no_of_clints_reading_file[index] = no_of_clints_reading_file[index] - 1
    # End part of changes for last lab

def server_func():
    global server_port
    global server_ip 
    global server_thread_kill
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
                if server_thread_kill == True:
                    return
                
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

if __name__ == "__main__":
    t1 = threading.Thread(target=server_func)
    t2 = threading.Thread(target=server_control)
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    t3 = threading.Thread(target= join_threads)
    t3.start()
    t3.join()
#END