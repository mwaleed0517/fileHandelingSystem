import FUNCS_LAB_7
import os.path
import threading
import mmap
import time

lock = threading.Lock()
no_of_threads = 4

def get_file_command():
    command = ''
    command = input()
    if ('mv ' not in command) and ('#' in command or '/' in command or ',' in command):
        print("File/Folder name can not contain \'#\', \'/\' or \',\'")
        return ''
    command_list = command.split(' ')
    return command_list

def create_MMAP_if_dont_exist():
    if (os.path.isfile("MMAP.txt")):
        pass
    else:
        f = open("MMAP.txt", "w")
        f.write("\n")

def get_data(tn):
    data = ''
    file_name = 'file' + tn.replace('thread', '') + 'data.txt'
    with open(file_name, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            return mmap_obj.read().decode()

def get_commands(tn):
    file_name = 'file' + tn.replace('thread', '') + '.txt'
    with open(file_name, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            return mmap_obj.read()

def function_calls(tName, fFuncs):
    current_file_open = '/#'
    command1 = get_commands(tName).decode()
    commands = command1.split('\n')

    for x in commands:
        x = x.strip('\r\n')
        command = x.split(' ')
        lock.acquire()
        print("Main->" + current_file_open.replace('/#', '') + ' $ ', x)
        lock.release()
        no_of_args = len(command)
        if no_of_args == 0:
            continue

        if command[0] == 'mk':
            if no_of_args == 2:
                fFuncs.create_file(command[1], current_file_open)
            else:
                print("mk takes only 2 arguments while", no_of_args, "were given")
        elif command[0] == 'delete':
            current_file_open = fFuncs.delete_file(current_file_open)
        elif command[0] == 'open':
            if no_of_args == 2:
                current_file_open = fFuncs.open_file(command[1], current_file_open)
            else:
                print("open takes only 2 arguments while", no_of_args, "were given")
        elif command[0] == 'close':
            current_file_open = fFuncs.close_file(current_file_open)
        elif command[0] == 'read':
            lock.acquire()
            fFuncs.read_file(current_file_open)
            lock.release()
        elif command[0] == 'write':
            start_time = time.time()
            data = get_data(tName)
            # data = data.split('\n')
            # for y in data:
                # y = y.strip('\r\n')
                # fFuncs.write_file(command[1], y, current_file_open)
                # command[1] = 'a'
            fFuncs.write_file(command[1], data, current_file_open)
            print("--- %s seconds ---" % (time.time() - start_time))
            time.sleep(100)
        elif command[0] == 'ls':
            fFuncs.list_files_and_folders_in_current(current_file_open)
        elif command[0] == 'lsall':
            fFuncs.show_mmap()
        elif command[0] == 'opendir':
            if no_of_args == 2:
                current_file_open = fFuncs.open_dir(command[1], current_file_open)
            else:
                print("opendir takes only 1 arguments while", no_of_args - 1, "were given")
        elif command[0] == 'mkdir':
            if no_of_args == 2:
                fFuncs.create_dir(command[1], current_file_open)
            else:
                print("mkdir takes only 1 arguments while", no_of_args - 1, "were given")
        elif command[0] == 'mv':
            if no_of_args == 4:
                fFuncs.move_file(command[1], command[2], command[3])
            else:
                print("mv takes only 3 arguments while", no_of_args - 1, "were given")
        elif command[0] == 'mvdata':
            if no_of_args == 4:
                fFuncs.move_data(command[1], command[2], command[3], current_file_open)
            else:
                print("mvdata takes only 3 arguments while", no_of_args - 1, "were given")
        elif command[0] == 'trdata':
            if no_of_args == 2:
                fFuncs.truncate_data(command[1], current_file_open)
            else:
                print("trdata takes only 1 arguments while", no_of_args - 1, "were given")
        elif command[0].lower() == 'help':
            print('COMMANDS:\n\tmk filrName\t\t\tcreate a file')
            print('\tmkdir FolderName\t\tcrete a folder')
            print('\topen FileNAme\t\t\tOpen a file')
            print('\topendir FolderName\t\tOpen a folder')
            print('\tclose\t\t\t\tclose current File/Folder open')
            print('\tdelete\t\t\t\tdelete current File/Folder open')
            print('\tread\t\t\t\tRead current File open')
            print('\twrite\t\t\t\twrite current File open')
            print(
                '\tmv fileName Source Destination\tMove file from Soucer folder to destination folder(Notice: For main folder use \'/#\' as source or destination)')
            print('\tmvdata Start Size target\tMove data of given size from start to target location in file')
            print('\tmrdata Size\tTruncate data of given size from file')
            print('\tls\t\t\t\tShows files and Folder in current folder')
            print('\tlsall\t\t\t\tShows all files and their locations along with data length')
            print('\texit\t\t\t\tClose Program')
            print('RULES:\n\tCommands tobe seperated from Names and paths with black spaces')
            print('\tCommands are case sensitive exept \'help\'')
            print('\tName can not contain blank space\' \', comma\',\', slash\'/\' or hash\'#\'')
        elif command[0] == 'exit':
            print("\n\t...Exiting...\n")
            break
        else:
            print("Invalid Entry!\n\t...ENTER HELP FOR DETAILS...")


if __name__ == "__main__":
    create_MMAP_if_dont_exist()
    fFuncs = FUNCS_LAB_7.FileHandling()
    thread_list = []
    for x in range(no_of_threads):
        thread = threading.Thread(target=function_calls, args=('thread' + str(x + 1), fFuncs,))
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()