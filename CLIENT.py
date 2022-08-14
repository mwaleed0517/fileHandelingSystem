import CLIENT_FUNCS
import threading
import os.path
import time

def function_calls(fFuncs):
    while True:
        print("Main "+fFuncs.current_file_open.replace('/#','')+'-> $ ', end = '')
        command = fFuncs.get_command()
        no_of_args=len(command)
        if no_of_args==0:
            continue
        # start_time = time.time()
        if command[0] == 'mk':
            if no_of_args == 2:
                fFuncs.create_file(command[1])
            else:
                print("mk takes only 2 arguments while",no_of_args,"were given")
        elif command[0] == 'delete':
            fFuncs.delete_file()
        elif command[0] == 'open':
            if no_of_args == 2:
                fFuncs.open_file(command [1])
            else:
                print("open takes only 2 arguments while",no_of_args,"were given")
        elif command[0] == 'close':
            fFuncs.close_file()
        elif command[0] == 'read':
            fFuncs.read_file()
        elif command[0] == 'write':
            if no_of_args == 2:
                fFuncs.write_file(command[1])
            else:
                print("write takes only 1 arguments while", no_of_args - 1, "were given")
        elif command[0] == 'ls':
            fFuncs.list_files_and_folders_in_current()
        elif command[0] == 'lsall':
            fFuncs.show_mmap()
        elif command[0] == 'opendir':
            if no_of_args == 2:
                fFuncs.open_dir(command[1])
            else:
                print("opendir takes only 1 arguments while",no_of_args-1,"were given")
        elif command[0] == 'mkdir':
            if no_of_args == 2:
                fFuncs.create_dir(command[1])
            else:
                print("mkdir takes only 1 arguments while",no_of_args-1,"were given")
        elif command[0] == 'mv':
            if no_of_args == 4:
                fFuncs.move_file(command[1],command[2],command[3])
            else:
                print("mv takes only 3 arguments while",no_of_args-1,"were given")
        elif command[0] == 'mvdata':
            if no_of_args == 4:
                fFuncs.move_data(command[1],command[2],command[3])
            else:
                print("mvdata takes only 3 arguments while",no_of_args-1,"were given")
        elif command[0] == 'trdata':
            if no_of_args == 2:
                fFuncs.truncate_data(command[1])
            else:
                print("trdata takes only 1 arguments while",no_of_args-1,"were given")
        elif command[0].lower() == 'help':
            print('COMMANDS:\n\tmk fileName\t\t\tTo create a file')
            print('\tmkdir folderName\t\tTo crete a folder')
            print('\topen fileName\t\t\tTo open a file')
            print('\topendir folderName\t\tTo open a folder')
            print('\tclose\t\t\t\tTo close current File/Folder open')
            print('\tdelete\t\t\t\tTo delete current File open (Folder cannot be deleted)')
            print('\tread\t\t\t\tTo read data in current File open')
            print('\twrite mode(a/w)\t\t\tTo write data in current File open')
            print('\tmv fileName Source Destination\n\t\t-> To move file from Soucer folder to destination folder(Notice: For main folder, use \'/#\' as source or destination)')
            print('\tmvdata Start Size target\tTo move data of given size from start to target location in file')
            print('\ttrdata Size\t\t\tTo truncate data of given size from file')
            print('\tls\t\t\t\tTo show files and Folder in current folder')
            print('\tlsall\t\t\t\tTo show all files and their locations along with data length')
            print('\texit\t\t\t\tTo Close Program')
            print('RULES:\n\tCommands tobe seperated from Names and paths with blanck spaces')
            print('\tCommands are case sensitive exept \'help\'')
            print('\tName can not contain blank space \' \', comma \',\', slash \'/\' or hash \'#\'')
        elif command[0] == 'exit':
            print("\n\t...Exiting...\n")
            break
        else:
            print("Invalid Entry!\n\t...ENTER HELP FOR DETAILS...")
        # print("Execution time was",time.time() - start_time)
   
if __name__ == "__main__": 
    function_calls(CLIENT_FUNCS.ComandsFormatng())