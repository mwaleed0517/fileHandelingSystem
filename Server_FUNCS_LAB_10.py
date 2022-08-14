import mmap
import os
import threading
import time

class FileHandling:
    def __init__(self):
        self.file_empty = False
        self.create_MMAP_if_dont_exist()
        file = open('MMAP.txt', 'r+')
        self.mmap_object = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_WRITE)
        os.SEEK_SET = 0
        self.next_p_start=2
        self.createFuncLock = threading.Lock()
        self.lock = threading.Lock()
        if self.file_empty == True:
            self.create_file('#')

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

    def create_file(self, file_name):
                """ Crete lock is built to make sure that
                only one file gets created at a time
                so other create comands dont mess up and
                pointer dont mess while one file is being created otherwise
                file will be created with no existance 
                """
                self.createFuncLock.acquire()
                
                self.set_pointer_for_new_file()
                
                # appending empty pointers with file name
                mmapWriteforFile = file_name + "," + "#########" + "," + "#########" + "\n"
                # creating memory block
                size_of_mmapWriteforFile = len(mmapWriteforFile)
                
                # write file name with empty pointers
                self.lock.acquire()
                present_location = self.mmap_object.size()
                self.create_room_in_mmap(present_location+size_of_mmapWriteforFile)
                self.set_data_at(present_location,mmapWriteforFile)
                self.lock.release()
                self.createFuncLock.release()
                
    def delete_file(self,file_name):
        next_p=self.next_p_start
        next_file_pointer=''
        ToBeChanged_file_pointer=''
        while True:
            mmap_list,null=self.get_lists_for_mmap(next_p)
            if file_name == mmap_list[0]:
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

    def read_file(self,file_name):
        desired_list,null=self.mmap_for_specific_file(file_name)
        # check data pointer
        if "#########" == desired_list[1]:
            return 'NO DATA IN THIS FILE!'
        else:
            data_to_print = ''
            file_data_pointer = desired_list[1]
            lock_status = True
            while True:
                if lock_status:
                    self.lock.acquire()
                    lock_status=False
                if file_data_pointer != '':
                    self.mmap_object.seek(int(file_data_pointer))
                lines = self.mmap_object.readline().decode()
                # if last line of data block the move to next block
                if 'POPDATA#TEECFDIMMAPF' not in lines:
                    data_to_print += lines
                    file_data_pointer = ''
                else:
                    self.lock.release()
                    lock_status = True
                    data_to_print += lines[0:len(lines)-30]+'\n'
                    file_data_pointer = lines[-10:-1]
                # once reached end of last data block then exit reading
                if file_data_pointer == "#########":
                    break
            # return the data read
            return data_to_print

    def write_file(self,file_name,fWriteMode,data):
        desired_list,current=self.mmap_for_specific_file(file_name)
        # writing in write mode
        if fWriteMode.lower()=="w":
            self.lock.acquire()
            
            # setting pointer
            location_to_write=str(self.mmap_object.size())
            location_to_write=location_to_write.strip().zfill(9)
            self.set_data_at(current-20,location_to_write)
            
            # Writing data
            data = data  + "POPDATA#TEECFDIMMAPF#########\n"
            self.create_room_in_mmap(self.mmap_object.size()+len(data))
            self.set_data_at(int(location_to_write),data)
            
            self.lock.release()
        
        # writing in append mode
        elif fWriteMode.lower()=="a":
            
            file_data_pointer = desired_list[1]
            current_data_pointer = ''
            
            if file_data_pointer == "#########":
                self.write_file(file_name,'w',data)
                return
            
            while True:
                current_data_pointer = file_data_pointer
                
                self.lock.acquire()
                self.mmap_object.seek(int(file_data_pointer))
                lines = self.mmap_object.readline().decode()
                file_data_pointer = self.mmap_object.tell()
                self.lock.release()
                
                # if line is last in data block then get pointer for next block
                if 'POPDATA#TEECFDIMMAPF' in lines:
                    file_data_pointer = lines[-10:-1]
                    
                # If hashes at pointer then mean this is last block so set pointer here
                if file_data_pointer == "#########":
                    self.lock.acquire()
                    
                    # set pointer
                    location_to_write=str(self.mmap_object.size())
                    location_to_write=location_to_write.strip().zfill(9)
                    self.set_data_at(int(current_data_pointer)+len(lines)-10,str(location_to_write))
                    
                    # set data
                    data = data  + "POPDATA#TEECFDIMMAPF#########\n"
                    self.create_room_in_mmap(self.mmap_object.size()+len(data))
                    self.set_data_at(int(location_to_write),data)
                    
                    self.lock.release()  
                    break
    
    def list_files_and_folders_in_current(self,file_name):
        next_p=2
        if self.mmap_object.size() == 2:
            return "Nothng Yet to show"
        if '/#' in file_name:
            data_to_return = ''
            while True:
                mmap_list,current_position=self.get_lists_for_mmap(next_p)
                if len(mmap_list) == 1:
                    continue
                
                mmap_list[2] = mmap_list[2].rstrip('\n\r')
                current_folder = file_name.replace('/#','')
                if current_folder in mmap_list[0]:
                    file = mmap_list[0]
                    if len(current_folder) == 0:
                        file = file[len(current_folder):]
                    else:
                        file = file[len(current_folder)+1:]
                    file_and_path = file.split('/')
                    if file_and_path[0] == '#':
                        pass
                    elif len(file_and_path) == 2  and'#' in file_and_path[1]:
                        data_to_return += 'Folder: '+file_and_path[0] + '\n'
                    elif len(file_and_path)==1:
                        data_to_return += 'File: '+file_and_path[0] + '\n'
                if "#########" == mmap_list[2]:
                    break
                else:
                    next_p=int(mmap_list[2])
            if data_to_return == '':
                return 'Empty Folder'
            return data_to_return

    def show_mmap(self):
        next_pointer = self.next_p_start
        mmap_files = []
        data_to_return = ''
        while True:
            mmap_list, null = self.get_lists_for_mmap(next_pointer)
            if '#' == mmap_list[0]:
                if "#########" in mmap_list[2]:
                    break
                else:
                    next_pointer = int(mmap_list[2])
                    continue
            
            if '/#' in mmap_list[0]:
                pass
            else:
                file_name = ''
                path = ''
                file_name_with_path = mmap_list[0].split('/')
                for x in file_name_with_path:
                    path += x+'/'
                    file_name = x
                path = path[0:-1]
                file_data_pointer = mmap_list[1]
                data = ''
                
                if "#########" in mmap_list[1]:
                    data_to_return += '\nFile Name:' + file_name + '\tFile Path:' + path + '\tFile Data Length: ' + 'No Data In File'
                else:
                    current_data_pointer = ''
                    while True:
                        current_data_pointer = file_data_pointer
                        self.lock.acquire()
                        self.mmap_object.seek(int(file_data_pointer))
                        lines = self.mmap_object.readline().decode()
                        file_data_pointer = self.mmap_object.tell()
                        self.lock.release()
                        
                        if 'POPDATA#TEECFDIMMAPF' not in lines:
                            data += lines
                        else:
                            data += lines[0:len(lines) - 30]
                            file_data_pointer = lines[-10:-1]
                        if file_data_pointer == "#########":
                            break
                    data_to_return += '\nFile Name:' + file_name + '\tFile Path:' + path + '\tFile Data Length: ' + str(len(data)) + 'bytes'
            if "#########" in mmap_list[2]:
                break

            next_pointer = int(mmap_list[2])
        
        if data_to_return == '':
            return 'Nothing Have Been Created'
        return data_to_return

    def move_file(self,source,destination):
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
            
    def move_data(self,file_name,startStr,sizeStr,targetStr):
        desired_list,current=self.mmap_for_specific_file(file_name)
        if "#########" == desired_list[1]:
            return 'No Data In File'
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
            
            if len(data)<start+size-1:
                return "Data Location Out of Range"
            elif len(data)<target+size-1:
                return "Target Out Of Range"
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
                
                return 'Data Moved Successfully'
    
    def truncate_data(self,file_name,sizeStr):
        desired_list,current=self.mmap_for_specific_file(file_name)
        if "#########" == desired_list[1]:
            return 'NO DATA IN THIS FILE!'
        else:
            size=int(sizeStr)
            data=''
            data_block_end_pointers = []
            data_block_at_pointer_size=[]
            file_data_pointer = desired_list[1]
            x=0
            while True:
                if file_data_pointer != '':
                    self.lock.acquire()
                    self.mmap_object.seek(int(file_data_pointer))
                
                lines = self.mmap_object.readline().decode()
                
                if 'POPDATA#TEECFDIMMAPF' not in lines:
                    lines = lines
                    x+=len(lines)
                    file_data_pointer = ''
                else:
                    self.lock.release()
                    file_data_pointer = lines[-10:-1]
                    lines = lines[0:len(lines) - 30]
                    x+=len(lines)
                    data_block_end_pointers.append(self.mmap_object.tell())
                    data_block_at_pointer_size.append(x)
                    x=0
                data += lines
                if file_data_pointer == "#########":
                    break
                
            data_size=len(data)
            if data_size<size:
                return "Truncate size Out of Range"
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
                    return 'Data Truncated Successfully'
                else:
                    if x == y:
                        location_to_write_at_location=data_block_end_pointers[i]-10
                        location_to_write = '#########'
                        self.lock.acquire()
                        self.set_data_at(location_to_write_at_location,location_to_write)
                        self.lock.release()
                        return 'Data Truncated Successfully'
                    else:
                        location_to_write_at_location=data_block_end_pointers[i-1]-10
                        z=len(data_to_write)
                        data_to_write = data_to_write[z-y:]
                        self.lock.acquire()
                        location_to_write = str(self.mmap_object.size())
                        location_to_write=location_to_write.strip().zfill(9)
                        self.set_data_at(location_to_write_at_location,location_to_write)
                        self.create_room_in_mmap(self.mmap_object.size()+len(data_to_write)+30)
                        self.set_data_at(int(location_to_write),data_to_write+'POPDATA#TEECFDIMMAPF#########\n')
                        self.lock.release()
                    
                        return 'Data Truncated Successfully'
                           
    def create_MMAP_if_dont_exist(self):
        if (os.path.isfile("MMAP.txt")):
            pass
        else:
            f = open("MMAP.txt", "w")
            f.write("\n")
            f.close
            self.file_empty = True
# END