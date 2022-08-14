import mmap
import os
import threading
import time

class FileHandling:
    def __init__(self):
        file = open('MMAP.txt', 'r+')
        self.mmap_object = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_WRITE)
        os.SEEK_SET = 0
        self.next_p_start=2
        self.createFuncLock = threading.Lock()
        self.lock = threading.Lock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        try:
            pass
        except Exception as e:
            pass

    def set_data_at(self,write_at,to_write):
        self.mmap_object.seek(write_at)
        self.mmap_object.write(str(to_write).encode())

    def set_pointer_for_new_file(self):
        next_p=self.next_p_start
        if self.mmap_object.size() == 2:
            return
        while True:
            mmap_list,current_position=self.get_lists_for_mmap(next_p)
            if len(mmap_list) == 1:
                continue

            mmap_list[2] = mmap_list[2].rstrip('\n\r')
            
            if "#########" == mmap_list[2]:
                our_desired_location=current_position-10
                self.lock.acquire()
                location_to_write=str(self.mmap_object.size())
                location_to_write=location_to_write.strip().zfill(9)
                self.set_data_at(our_desired_location,location_to_write)
                self.lock.release()
                break
            else:
                next_p=int(mmap_list[2])
        #...END OF WHILE LOOP...
        
    def get_lists_for_mmap(self,position):
        file = open('MMAP.txt', 'r+')
        mmap_object_r = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ)
        self.lock.acquire()
        mmap_object_r.seek(position)
        lines = mmap_object_r.readline().decode('utf-8')
        current = mmap_object_r.tell()
        self.lock.release()
        string_list = lines.split(',')
        mmap_object_r.close()
        return string_list,current

    def mmap_for_specific_file(self,filename):
        next_p=self.next_p_start
        while True:
            mmap_list,current_position=self.get_lists_for_mmap(next_p)
            if filename in mmap_list[0]:
                return mmap_list,current_position
            else:
                mmap_list[2] = mmap_list[2].rstrip('\n')
                next_p = int(mmap_list[2])

    def check_if_file_exist(self, file_name):
        next_p=self.next_p_start
        while True:
            mmap_list,null=self.get_lists_for_mmap(next_p)
            if len(mmap_list) == 1:
                return False
            
            mmap_list[2] = mmap_list[2].rstrip('\n')
            if file_name == mmap_list[0]:
                return True
            elif "#########" in mmap_list[2]:
                return False
            else:
                next_p=int(mmap_list[2])

    def create_room_in_mmap(self,count):
        self.mmap_object.resize(count)

    def create_file(self, file_name, current_file_open):
        if '/#' in current_file_open:
            if '/#' == current_file_open:
                file_name = current_file_open.replace('/#','')+file_name
            else:
                file_name = current_file_open.replace('#','')+file_name
            if(self.check_if_file_exist(file_name)):
                print("FILE/FOLDER ALREADY EXISTS!")
            else:
                self.createFuncLock.acquire()
                self.set_pointer_for_new_file()
                present_location=self.mmap_object.size()
                mmapWriteforFile = file_name + "," + "#########" + "," + "#########" + "\n"
                size_of_mmapWriteforFile = len(mmapWriteforFile)
                self.lock.acquire()
                self.create_room_in_mmap(self.mmap_object.size()+size_of_mmapWriteforFile)
                self.set_data_at(present_location,mmapWriteforFile)
                self.lock.release()
                self.createFuncLock.release()
        else:
            print('Seems Like some other filr already open!\n\t...CLOSE FILE TO CREATE NEW...')

    def delete_file(self,current_file_open):
        if '/#' in current_file_open:
            print("Open file to delete")
        else:
            next_p=self.next_p_start
            next_file_pointer=''
            ToBeChanged_file_pointer=''
            while True:
                mmap_list,null=self.get_lists_for_mmap(next_p)
                if current_file_open in mmap_list[0]:
                    next_file_pointer = mmap_list[2]
                    break
                else:
                    ToBeChanged_file_pointer = mmap_list[2]
                    next_p=int(mmap_list[2])
                    
            next_p=self.next_p_start
            while True:
                mmap_list,current_position=self.get_lists_for_mmap(next_p)
                if ToBeChanged_file_pointer in mmap_list[2]:
                    our_desired_location=current_position-10
                    self.lock.acquire()
                    self.set_data_at(our_desired_location,next_file_pointer)
                    self.lock.release()
                    break
                else:
                    next_p=int(mmap_list[2])
            return self.close_file(current_file_open)
    
    def open_file(self,file_name,current_file_open):
        if '/#' == current_file_open:
            current_file_open = ''
            if(self.check_if_file_exist(file_name)):
                return file_name
            else:
                if '/#' in file_name:
                    print("FOLDER DOSE NOT EXISTS!")
                else:
                    print("FILE DOSE NOT EXISTS IN MAIN!")
                return current_file_open+'/#'
        elif '/#' in current_file_open:
            current_file_open = current_file_open.replace('#','')
            if(self.check_if_file_exist(current_file_open+file_name)):
                return current_file_open+file_name
            else:
                if '/#' in file_name:
                    print("FOLDER DOSE NOT EXISTS!")
                else:
                    print("FILE DOSE NOT EXISTS!")
                return current_file_open+'#'
        else:
            print("Some Other File Already Open!")
        
    def close_file(self,current_file_open):
        if '/#' == current_file_open:
            print("No File/Folder currently open")
        else:
            current_file_open=current_file_open.replace('/#','')
            path=current_file_open.split('/')
            new_path=''
            for x in range(len(path)-1):
                new_path=path[x]
            return new_path+'/#'
            
    def read_file(self,current_file_open):
        if '/#' in current_file_open:
            print("No File Open to read. Please open file to read it")
        else:
            desired_list,null=self.mmap_for_specific_file(current_file_open)
            if "#########" == desired_list[1]:
                print('NO DATA IN THIS FILE!')
            else:
                file_data_pointer = desired_list[1]
                while True:
                    self.lock.acquire()
                    if file_data_pointer != '':
                        self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    self.lock.release()
                    if 'POPDATA#TEECFDIMMAPF' not in lines:
                        print(lines)
                        file_data_pointer = ''
                    else:
                        print(lines[0:len(lines)-30])
                        file_data_pointer = lines[-10:-1]
                    if file_data_pointer == "#########":
                        break

    def write_file(self,mode,data,current_file_open):
        if current_file_open in '/#':
            print("No File Open to read. Please open file to read it")
        else:
            fWriteMode = 'w'
            desired_list,current=self.mmap_for_specific_file(current_file_open)
            if "#########" in desired_list[1]:
                pass
            else:
                fWriteMode = mode # input("Select mode (\"a\" to apend or \"w\" to overwrite): ")
            if fWriteMode.lower()=="w":
                self.lock.acquire()
                location_to_write=str(self.mmap_object.size())
                location_to_write=location_to_write.strip().zfill(9)
                self.set_data_at(current-20,location_to_write)
                # data = input("Enter data to write:\n\t->")
                data = data  + "POPDATA#TEECFDIMMAPF#########\n"
                self.create_room_in_mmap(self.mmap_object.size()+len(data))
                self.set_data_at(int(location_to_write),data)
                self.lock.release()
            elif fWriteMode.lower()=="a":
                file_data_pointer = desired_list[1]
                current_data_pointer = ''
                while True:
                    current_data_pointer = file_data_pointer
                    self.lock.acquire()
                    self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    file_data_pointer = self.mmap_object.tell()
                    self.lock.release()
                    if 'POPDATA#TEECFDIMMAPF' in lines:
                        file_data_pointer = lines[-10:-1]
                    if file_data_pointer == "#########":
                        self.lock.acquire()
                        location_to_write=str(self.mmap_object.size())
                        location_to_write=location_to_write.strip().zfill(9)
                        self.set_data_at(int(current_data_pointer)+len(lines)-10,str(location_to_write))
                        # data = input("Enter data to write:\n\t->")
                        data = data  + "POPDATA#TEECFDIMMAPF#########\n"
                        self.create_room_in_mmap(self.mmap_object.size()+len(data))
                        self.set_data_at(int(location_to_write),data)
                        self.lock.release()  
                        break
            else:
                print("INVALID ENTRY!")
    
    def list_files_and_folders_in_current(self,current_file_open):
        next_p=2
        if self.mmap_object.size() == 2:
            print("Nothng Yet to show")
            return
        if '/#' in current_file_open:
            while True:
                mmap_list,current_position=self.get_lists_for_mmap(next_p)
                if len(mmap_list) == 1:
                    continue
                
                mmap_list[2] = mmap_list[2].rstrip('\n\r')
                current_folder = current_file_open.replace('/#','')
                if current_folder in mmap_list[0]:
                    file = mmap_list[0]
                    file = file.replace(current_folder,'')
                    file_and_path = file.split('/')
                    
                    if file_and_path[0] == '#':
                        pass
                    elif '#' in file_and_path[1]:
                        print('Folder: '+file_and_path[0])
                    elif len(file_and_path)>1:
                        pass
                    else:
                        print('File: '+file_and_path[0])
                if "#########" == mmap_list[2]:
                    break
                else:
                    next_p=int(mmap_list[2])
        else:
            print("No folder Open!Maybe Try closing file")

    def show_mmap(self):
        next_pointer = self.next_p_start
        mmap_files = []
        while True:
            mmap_list, null = self.get_lists_for_mmap(next_pointer)
            if "#########" in mmap_list[1]:
                mmap_list[1] = 'No Data In File'
            elif '/#' in mmap_list[0]:
                pass
            else:
                file_name = ''
                path = ''
                file_name_with_path = mmap_list[0].split('/')
                for x in file_name_with_path:
                    path += x
                    file_name = x

                file_data_pointer = mmap_list[1]
                data = ''
                while True:
                    self.lock.acquire()
                    if file_data_pointer != '':
                        self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    self.lock.release()
                    if 'POPDATA#TEECFDIMMAPF' not in lines:
                        data += lines
                        file_data_pointer = ''
                    else:
                        data += lines[0:len(lines) - 30]
                        file_data_pointer = lines[-10:-1]
                    if file_data_pointer == "#########":
                        break

                print('\nFile Name:' + file_name + '\tFile Path:' + path + '\tFile Data Length: ', len(data), 'bytes')
            if "#########" in mmap_list[2]:
                break

            next_pointer = int(mmap_list[2])
        
    def create_dir(self,file_name,current_file_open):
        self.create_file(file_name+'/#',current_file_open)
    
    def open_dir(self,file_name,current_file_open):
        return self.open_file(file_name+'/#',current_file_open)
                
    def move_file(self,file_name,source,destination,current_file_open):
        if source == '/#':
            source=file_name
        else:
            source+='/'+file_name
        if destination == '/#':
            destination=file_name
        else:
            if self.check_if_file_exist(destination+'/#'):
                destination+='/'+file_name
            else:
                print("Unknown Destination")
        if self.check_if_file_exist(source):
            if self.check_if_file_exist(destination):
                print("File aready present at source")
            else:
                file_data,null=self.mmap_for_specific_file(source)
                self.set_pointer_for_new_file()
                present_location=self.mmap_object.size()
                mmapWriteforFile = destination + "," + file_data[1] + "," + "#########" + "\n"
                size_of_mmapWriteforFile = len(mmapWriteforFile)
                self.lock.acquire()
                self.create_room_in_mmap(self.mmap_object.size()+size_of_mmapWriteforFile)
                self.set_data_at(present_location,mmapWriteforFile)
                self.lock.release()
                self.delete_file(source)
        else:
            print("Invalid Source!")
            
    def move_data(self,startStr,sizeStr,targetStr,current_file_open):
        if '/#' in current_file_open:
            print("No File Open")
        else:
            desired_list,current=self.mmap_for_specific_file(current_file_open)
            if "#########" == desired_list[1]:
                print('NO DATA IN THIS FILE!')
            else:
                start=int(startStr)
                size=int(sizeStr)
                target=int(targetStr)
                data=''
                data_pointers=[]
                data_at_pointer_size=[]
                data_pointers.append(desired_list[1])
                file_data_pointer = desired_list[1]
                self.lock.acquire()
                while True:
                    if file_data_pointer != '':
                        self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    if 'POPDATA#TEECFDIMMAPF' not in lines:
                        lines = lines
                        file_data_pointer = ''
                    else:
                        file_data_pointer = lines[-10:-1]
                        lines = lines[0:len(lines) - 30]
                    data += lines
                    data_at_pointer_size.append(len(lines))
                    if file_data_pointer == "#########":
                        break
                    data_pointers.append(self.mmap_object.tell())
                self.lock.release()

                if len(data)<start+size:
                    print("Data Location Out of Range")
                elif len(data)<target+size:
                    print("Target Out Of Range")
                else:
                    length=len(data)
                    data_to_move=data[start-1:start+size-1]
                    data = data[0:start-1]+data[start+size-1:]
                    if target == 1:
                        data_after_move = data_to_move + data
                    elif target-size ==len(data)-size:
                        data_after_move = data + data_to_move
                    else:
                        data_after_move = data[0:target-1] + data_to_move + data[target-1:]
                    
                    i=0
                    list_size = len(data_at_pointer_size)
                    data_to_write = data_after_move[0:data_at_pointer_size[i]]
                    for x in data_pointers:
                        write_at_location=int(x)
                        self.lock.acquire()
                        self.set_data_at(int(write_at_location),str(data_to_write))
                        self.lock.release()
                        if i+2<list_size:
                            data_to_write = data_after_move[data_at_pointer_size[i]:data_at_pointer_size[i+1]]
                        else:
                            data_to_write = data_after_move[data_at_pointer_size[i]:]
                        i+=1
    
    def truncate_data(self,sizeStr,current_file_open):
        if '/#' in current_file_open:
            print("No File Open")
        else:
            desired_list,current=self.mmap_for_specific_file(current_file_open)
            if "#########" == desired_list[1]:
                print('NO DATA IN THIS FILE!')
            else:
                size=int(sizeStr)
                data=''
                data_block_end_pointers = []
                data_block_at_pointer_size=[]
                file_data_pointer = ''
                x=0
                self.lock.acquire()
                while True:
                    if file_data_pointer != '':
                        self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    if 'POPDATA#TEECFDIMMAPF' not in lines:
                        lines = lines
                        file_data_pointer = ''
                        x+=len(lines)
                    else:
                        file_data_pointer = lines[-10:-1]
                        lines = lines[0:len(lines) - 30]
                        x+=len(lines)
                        data_block_end_pointers.append(self.mmap_object.tell())
                        data_block_at_pointer_size.append(x)
                        x=0
                    data += lines
                    if file_data_pointer == "#########":
                        break
                self.lock.release()

                data_size=len(data)
                if data_size<size:
                    print("Truncate size Out of Range")
                elif data_size==size:
                    self.lock.acquire()
                    self.set_data_at(current-20,"#########")
                    self.lock.release()
                else:
                    data_to_write=data[0:data_size-size]
                    i = 0
                    x = 0
                    y = len(data_to_write)
                    while True:
                        x = data_block_at_pointer_size[i]
                        if y > x:
                            y -= x
                            i+=1
                        else:
                            break
                    
                    if i == 0:
                        location_to_write_at_location=current-20
                        self.lock.acquire()
                        location_to_write=str(self.mmap_object.size())
                        location_to_write=location_to_write.strip().zfill(9)
                        self.set_data_at(location_to_write_at_location,location_to_write)
                        self.create_room_in_mmap(self.mmap_object.size()+len(data_to_write)+30)
                        self.set_data_at(int(location_to_write),data_to_write+'POPDATA#TEECFDIMMAPF#########\n')
                        self.lock.release()
                    else:
                        data_to_write = data_to_write[data_block_at_pointer_size[i]:]
                        location_to_write_at_location=data_block_end_pointers[i-1]-10
                        if x == y:
                            location_to_write = '#########'
                            self.lock.acquire()
                            self.set_data_at(location_to_write_at_location,location_to_write)
                            self.lock.release()
                            return
                        else:
                            self.lock.acquire()
                            location_to_write = str(self.mmap_object.size())
                            location_to_write=location_to_write.strip().zfill(9)
                            self.set_data_at(location_to_write_at_location,location_to_write)
                            self.create_room_in_mmap(self.mmap_object.size()+len(data_to_write)+30)
                            self.set_data_at(int(location_to_write),data_to_write+'POPDATA#TEECFDIMMAPF#########\n')
                            self.lock.release()