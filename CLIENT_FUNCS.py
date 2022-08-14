import mmap
import os
import threading
import time
import socket
import sys

class ComandsFormatng:
    
    def __init__(self):
        self.socket_server_ip=''
        self.socket_port = 0
        self.clint_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.check_socket()
        self.current_file_open = '/#'

    def check_socket(self):
        while True:
            # self.socket_server_ip = input("Enter The Server IP  : ")
            # self.socket_port = int(input("Enter The Port Number  : "))
            # server_name = socket.gethostname()
            # self.socket_server_ip = socket.gethostbyname(server_name)
            self.socket_server_ip='192.168.137.1'
            self.socket_port = 95
            
            result_of_check = self.clint_socket.connect_ex((self.socket_server_ip,self.socket_port))
            if result_of_check == 0:
                print("Server connected")
                break
            else:
                print("Unable to connect!")
                check = input("Do You Want To exit?(Yes to exit)    ")
                if check.lower() == 'yes' :
                    break
        self.close_connection_to_server()

    def connect_to_server(self):
        continuty_check = 0
        while True:
            if continuty_check == 10:
                print('...10 UNSUCESSFULL ATTEMPTS...\n...EXITING PROGRAM IN 5...')
                time.sleep(5)
                sys.exit()
            try:
                self.clint_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.clint_socket.connect((self.socket_server_ip,self.socket_port))
                continuty_check = 0
            except socket.error as err:
                continuty_check+=5
                print('Error:',err,'\nWhile connecting with',self.socket_server_ip,'\n...RETYRING IN',continuty_check,'SECENDS...')
            if continuty_check == 0:
                break
            time.sleep(continuty_check)

    def close_connection_to_server(self):
        self.clint_socket.close()

    def get_command(self):
        command=''
        command = input()
        if ('mv ' not in command )and ('#' in command or '/' in command or ',' in command):
            print("File/Folder name can not contain \'#\', \'/\' or \',\'")
            return ''
        command_list = command.split(' ') 
        return command_list

    def check_if_file_exist(self, file_name):
        self.connect_to_server()
        command = 'file_check '+file_name
        self.clint_socket.send(command.encode())
        startus_str = self.clint_socket.recv(10)
        startus_str = startus_str.decode()
        self.close_connection_to_server()
        if 'true' in startus_str:
           return True
        else:
           return False

    def create_file(self, file_name,):
        if '/#' in self.current_file_open:
            if '/#' == self.current_file_open:
                file_name = self.current_file_open.replace('/#','')+file_name
            else:
                file_name = self.current_file_open.replace('#','')+file_name
            if(self.check_if_file_exist(file_name)):
                print("FILE/FOLDER ALREADY EXISTS!")
            else:
            # if 0 == 0:
                command = 'mk '+file_name
                self.connect_to_server()
                self.clint_socket.send(command.encode())
                if 'Done' in self.clint_socket.recv(5).decode():
                    print('...File Created successfully...')
                else:
                    print('...File Creating Error...')
                self.close_connection_to_server()
        else:
            print('Seems Like some other file already open!\n\t...CLOSE FILE TO CREATE NEW...')

    def delete_file(self):
        if '/#' in self.current_file_open:
            print("Open file to delete")
        else:
            self.connect_to_server()
            command = 'delete '+self.current_file_open
            self.clint_socket.send(command.encode())
            check_returned = self.get_server_response()
            if 'Done' in check_returned:
                print('...File Deleted successfully...')
            else:
                print('...File Deleting Error...')
            self.close_connection_to_server()
            self.close_file()
    
    def open_file(self,file_name):
        if '/#' == self.current_file_open:
            self.current_file_open = ''
            if(self.check_if_file_exist(file_name)):
                self.current_file_open = file_name
            else:
                if '/#' in file_name:
                    print("FOLDER DOSE NOT EXISTS!")
                else:
                    print("FILE DOSE NOT EXISTS IN MAIN!")
                self.current_file_open = self.current_file_open+'/#'
        elif '/#' in self.current_file_open:
            self.current_file_open = self.current_file_open.replace('#','')
            if(self.check_if_file_exist(self.current_file_open+file_name)):
                self.current_file_open = self.current_file_open+file_name
            else:
                if '/#' in file_name:
                    print("FOLDER DOSE NOT EXISTS!")
                else:
                    print("FILE DOSE NOT EXISTS!")
                self.current_file_open = self.current_file_open+'#'
        else:
            print("Some Other File Already Open!")

    def close_file(self):
        if '/#' == self.current_file_open:
            print("No File/Folder currently open")
        else:
            self.current_file_open=self.current_file_open.replace('/#','')
            path=self.current_file_open.split('/')
            new_path=''
            for x in range(len(path)-1):
                new_path += path[x] + '/'
            self.current_file_open =  new_path[0:-1]+'/#'
            
    def read_file(self):
        if '/#' in self.current_file_open:
            print("No File Open to read. Please open file to read it")
        else:
            self.connect_to_server()
            command = 'read '+self.current_file_open
            self.clint_socket.send(command.encode())
            data_to_print=''
            while True:
                incoming = self.clint_socket.recv(10000)
                incoming = incoming.decode()
                if incoming == '#TIEWCFSTOCTTTWFS#':
                    print('Server is busy performing some other action on file PLEASE WAIT!')
                    continue
                elif incoming == '#OBKKDPPGYFTTEK#':
                    print('Server says I am trapped with some crazy dude on this file\n...Maybe You should try again later...') 
                    return
                elif incoming == '#TIEECFTDOFSBS#':
                    break
                else:
                    data_to_print += incoming
            self.close_connection_to_server()
            print(data_to_print)

    def write_file(self, fWriteMode):
        if '/#' in self.current_file_open:
            print("No File Open to read. Please open file to read it")
        else:
            
            # mode = input("Select mode (\"a\" to apend or \"w\" to overwrite): ")
            
            if fWriteMode.lower()=="w" or fWriteMode.lower()=="a":
            
                server_response = ''
                data = ''
                input_mode = input('Do you want to read data from file? (Enter yes to read from file): ')
                if input_mode.lower() == 'yes':
                    file_name = input('Enter file name:').strip('\n')
                    if (os.path.isfile(file_name)):
                        with open(file_name, mode="r", encoding="utf8") as file_obj:
                            data = file_obj.read()
                    else:
                        print('File Dose Not Exist! May be try File_Name.txt')
                        return
                else:
                    data = input("Enter the data to write\n\t->")
            
                command = 'write ' + self.current_file_open + ' ' + fWriteMode
                
                self.connect_to_server()
                
                print('...Sending Data To Server...')
                # start_time = time.time()
            
                self.clint_socket.send(command.encode())
                time.sleep(1)
                self.clint_socket.send(data.encode())
                time.sleep(1)
                self.clint_socket.send('#EODFTFSFC#'.encode())
                
                print('...Data Sent To Server...')
                
                server_response = self.get_server_response()
                
                self.close_connection_to_server()
                
                if 'Done' in server_response:
                    print('...Data writed successfully...')
                else:
                    print('...Data writing Error...')

                # print("Write execution time was",time.time() - start_time)
            else:
                print("INVALID MODE!")
    
    def list_files_and_folders_in_current(self):
        command = 'ls ' + self.current_file_open
        data_to_print = ''

        self.connect_to_server()
        self.clint_socket.send(command.encode())
        data_to_print += self.clint_socket.recv(1000).decode()
        if 'Fail' == data_to_print:
            print('...Files Linsting Error...')
        else:
            print(data_to_print)
        self.close_connection_to_server()

    def show_mmap(self):
        command = 'lsall'
        data_to_print = ''

        self.connect_to_server()
        self.clint_socket.send(command.encode())
        data_to_print += self.clint_socket.recv(10000).decode()
        if 'Fail' == data_to_print:
            print('...Files Linsting Error...')
        else:
            print(data_to_print)
        self.close_connection_to_server()
        
    def create_dir(self,file_name):
        self.create_file(file_name+'/#')
    
    def open_dir(self,file_name):
       self.open_file(file_name+'/#')
                
    def move_file(self,file_name,source,destination):
        if source == '/#':
            source=file_name
        else:
            source+='/'+file_name
        if destination == '/#':
            destination=file_name
        else:
            if self.check_if_file_exist(destination+'/#'):
                print(destination)
                destination+='/'+file_name
            else:
                print("Unknown Destination")
                return
        if self.check_if_file_exist(source):
            if self.check_if_file_exist(destination):
                print("File aready present at source")
            else:
                if source == self.current_file_open:
                    self.close_file()
                command = 'mv ' + source + ' ' + destination
                self.connect_to_server()
                self.clint_socket.send(command.encode())
                server_response = self.get_server_response()
                if 'Done' in server_response:
                    print('...File Moved successfully...')
                else:
                    print('...File Moving Error...')
                self.close_connection_to_server()
        else:
            print("Invalid Source!")
            
    def move_data(self,startStr,sizeStr,targetStr):
        if '/#' in self.current_file_open:
            print("No File Open")
        else:
            command = 'mvdata ' + self.current_file_open + ' ' + startStr + ' ' + sizeStr + ' ' + targetStr
            self.connect_to_server()
            self.clint_socket.send(command.encode())
            server_response = self.get_server_response()
            print(server_response)
            self.close_connection_to_server()
    
    def truncate_data(self,sizeStr):
        if '/#' in self.current_file_open:
            print("No File Open")
        else:
            command = 'trdata ' + self.current_file_open + ' ' + sizeStr
            self.connect_to_server()
            self.clint_socket.send(command.encode())
            server_response = self.get_server_response()
            print(server_response)
            self.close_connection_to_server()

    def get_server_response(self):
        while True:
            check_returned = check_returned = self.clint_socket.recv(100).decode()
            x = -1
            if check_returned == '#TIEWCFSTOCTTTWFS#':
                if x == -1:
                    print('Server is busy performing some other action on file PLEASE WAIT!')
                    x *= -1
            elif check_returned == '#OBKKDPPGYFTTEK#':
                print('Server says I am trapped with some crazy dude on this file!\n...Maybe You should try again later...')
                return 'Fail'
            elif check_returned == 'Done':
                return 'Done'
            elif check_returned == 'Fail':
                return 'Fail'
            else:
                return check_returned

# END