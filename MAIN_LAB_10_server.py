import Server_FUNCS_LAB_10
import os.path
import threading
import mmap
import time
import socket
import sys

lock = threading.Lock()
port = 12345
server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)
clint_addresses =[]
clint_data = []
thread_list = []
fFuncs = Server_FUNCS_LAB_10.FileHandling()
files_being_processed = []

def function_calls(command,clint):
        lock.acquire()
        files_being_processed.append(command[1])
        lock.release()

        if command[0] == 'mk':
            fFuncs.create_file(command[1])
        elif command[0] == 'delete':
            fFuncs.delete_file(command[1])
        elif command[0] == 'read':
            data_returned = fFuncs.read_file(command[1])
            len_data_recived = len(data_recived)
            x = 99000
            while x < data_recived:
                clint.send(data_returned[0,99000])
                data_returned = data_returned[99000:]
                x+=99000
            if len(data_returned) != 0:
                clint.send(data_returned[x:])          
        elif command[0] == 'write':
            fFuncs.write_file(command[1], command[2], command[3])
        elif command[0] == 'ls':
            clint.send(fFuncs.list_files_and_folders_in_current(command[1]).encode())
        elif command[0] == 'lsall':
            clint.send(fFuncs.show_mmap().encode())
        elif command[0] == 'mv':
            fFuncs.move_file(command[1], command[2], command[3])
        elif command[0] == 'mvdata':
            fFuncs.move_data(command[1], command[2], command[3], command[4])
        elif command[0] == 'trdata':
            fFuncs.truncate_data(command[1], command[2])
        elif command[0] == 'file_check':
            if fFuncs.check_if_file_exist(clint_commands[1]):
                clint.send('true'.encode())
            else:
                clint.send('false'.encode())
                        
def write_command_handler(commands,data_recived,clint_add,clint):
    if commands[1] == 'data_continue':
        if clint_add in clint_addresses:
            data_index = clint_addresses.index(clint_add)
            clint_data[data_index] = clint_data[data_index] + data_recived
        else:
            clint_addresses.append(clint_add)
            clint_data.append(data_recived)
    elif commands[1] == 'final':
        if clint_add in clint_addresses:
            data_recived = clint_data[data_index] + data_recived
            data_index = clint_addresses.index(clint_add)
            clint_data.pop(data_index)
            clint_addresses.pop(data_index)
        commands[1]=data_recived
        thread = threading.Thread(target=function_calls, args=(clint_commands,clint,))
        thread_list.append(thread)
        thread.start()

if __name__ == "__main__":
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_socket.bind((server_ip,port))
            server_socket.listen(5)
            print('...SOCKET UP AND RUNNING...')
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
                clint_commands = clint_command.split(' ') 
                if clint_commands[0] == 'write':
                    data_recived = clint.recv(10000).decode()
                    thread = threading.Thread(target=write_command_handler, args=(clint_commands,data_recived,clint_add,))
                    thread_list.append(thread)
                    thread.start()
                else:
                    thread = threading.Thread(target=function_calls, args=(clint_commands,clint,))
                    thread_list.append(thread)
                    thread.start()
        time.sleep(continuty_check)
    
    for thread in thread_list:
        thread.join()