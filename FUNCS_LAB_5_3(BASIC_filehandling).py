import mmap
import os


class FileHandling:
    def __init__(self):
        file = open('MMAP.txt', 'r+')
        self.mmap_object = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_WRITE)
        os.SEEK_SET = 0
        self.current_file_open = '/#'
        self.next_p_start=2

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        try:
            pass
        except Exception as e:
            pass

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
                location_to_write=str(self.mmap_object.size())
                location_to_write=location_to_write.strip().zfill(9)
                self.mmap_object.seek(our_desired_location)
                self.mmap_object.write(str(location_to_write).encode())
                self.mmap_object.seek(self.mmap_object.tell()+1)
                break
            else:
                next_p=int(mmap_list[2])
        #...END OF WHILE LOOP...
        
    def get_lists_for_mmap(self,position):
        file = open('MMAP.txt', 'r+')
        mmap_object_r = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ)
        
        mmap_object_r.seek(position)
        lines = mmap_object_r.readline().decode('utf-8')
        # utf8_line = lines.split(str.encode(','))
        # utf8_line = lines.rstrip(str.encode('\r'))
        
        # string_list = [x.decode('utf-8') for x in utf8_line]
        # sting_list=[filname,starting_pointer,next_location]
        current = mmap_object_r.tell()
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

    def create_file(self,file_name):
        if '/#' in self.current_file_open:
            if '/#' == self.current_file_open:
                file_name = self.current_file_open.replace('/#','')+file_name
            else:
                file_name = self.current_file_open.replace('#','')+file_name
            if(self.check_if_file_exist(file_name)):
                print("FILE/FOLDER ALREADY EXISTS!")
            else:
                self.set_pointer_for_new_file()
                present_location=self.mmap_object.size()
                mmapWriteforFile = file_name + "," + "#########" + "," + "#########" + "\n"
                size_of_mmapWriteforFile = len(mmapWriteforFile)
                self.create_room_in_mmap(self.mmap_object.size()+size_of_mmapWriteforFile)
                self.mmap_object.seek(present_location)
                self.mmap_object.write(str(mmapWriteforFile).encode())
        else:
            print('Seems Like some other filr already open!\n\t...CLOSE FILE TO CREATE NEW...')

    def delete_file(self):
        if '/#' in self.current_file_open:
            print("Open file to delete")
        else:
            next_p=self.next_p_start
            next_file_pointer=''
            ToBeChanged_file_pointer=''
            while True:
                mmap_list,null=self.get_lists_for_mmap(next_p)
                if self.current_file_open in mmap_list[0]:
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
                    self.mmap_object.seek(our_desired_location)
                    self.mmap_object.write(str(next_file_pointer).encode())
                    self.mmap_object.seek(self.mmap_object.tell()+1)
                    break
                else:
                    next_p=int(mmap_list[2])
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
                    print("FILE DOSE NOT EXISTS!")
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
                new_path=path[x]
            self.current_file_open = new_path+'/#'
            
    def read_file(self):
        if '/#' in self.current_file_open:
            print("No File Open to read. Please open file to read it")
        else:
            desired_list,null=self.mmap_for_specific_file(self.current_file_open)
            if "#########" == desired_list[1]:
                print('NO DATA IN THIS FILE!')
            else:
                file_data_pointer = desired_list[1]
                while True:
                    self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    print(lines[0:len(lines)-10])
                    file_data_pointer = lines[-10:-1]
                    if file_data_pointer == "#########":
                        break
                
                # next_file_point=int(desired_list[2])
                # ourpoint=next_file_point-10
                # self.mmap_object.seek(ourpoint)
                # pointer=self.mmap_object[ourpoint:ourpoint+9]
                # pointer=pointer.decode()
                # start_address=int(desired_list[1])
                # print(start_address,ourpoint)
                # if pointer == "#########":
                #     data=self.mmap_object[start_address:ourpoint]
                #     print(data)

    def write_file(self):
        if '/#' in self.current_file_open:
            print("No File Open to read. Please open file to read it")
        else:
            fWriteMode = 'w'
            desired_list,current=self.mmap_for_specific_file(self.current_file_open)
            if "#########" in desired_list[1]:
                pass
            else:
                fWriteMode = input("Select mode (\"a\" to apend or \"w\" to overwrite): ")
            if fWriteMode.lower()=="w":
                location_to_write=str(self.mmap_object.size())
                location_to_write=location_to_write.strip().zfill(9)
                self.mmap_object.seek(current-20)
                self.mmap_object.write(str(location_to_write).encode())
                data = input("Enter data to write:\n\t->") + "#########\n"
                self.create_room_in_mmap(self.mmap_object.size()+len(data))
                self.mmap_object.seek(int(location_to_write))
                self.mmap_object.write(data.encode())
            elif fWriteMode.lower()=="a":
                file_data_pointer = desired_list[1]
                current_data_pointer = ''
                while True:
                    self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    current_data_pointer = file_data_pointer
                    file_data_pointer = lines[-10:-1]
                    if file_data_pointer == "#########":
                        location_to_write=str(self.mmap_object.size())
                        location_to_write=location_to_write.strip().zfill(9)
                        self.mmap_object.seek(int(current_data_pointer)+len(lines)-10)
                        self.mmap_object.write(str(location_to_write).encode())
                        data = input("Enter data to write:\n\t->") + "#########\n"
                        self.create_room_in_mmap(self.mmap_object.size()+len(data))
                        self.mmap_object.seek(int(location_to_write))
                        self.mmap_object.write(data.encode())  
                        break
            else:
                print("INVALID ENTRY!")

    def list_files_and_folders_in_current(self):
        next_p=2
        if self.mmap_object.size() == 2:
            print("Nothng Yet to show")
            return
        if '/#' in self.current_file_open:
            while True:
                mmap_list,current_position=self.get_lists_for_mmap(next_p)
                if len(mmap_list) == 1:
                    continue

                file_and_path=[]
                mmap_list[2] = mmap_list[2].rstrip('\n\r')
                current_folder = self.current_file_open.replace('/#','')
                if current_folder in mmap_list[0]:
                    file_ahead = mmap_list[0]
                    file_ahead = file_ahead.replace(current_folder+'/','')
                    file_and_path = file_ahead.split('/')
                    if file_and_path[0] == '#':
                        pass
                    elif '/#' in mmap_list[0]:
                        print('Folder: '+file_and_path[0])
                    else:
                        print('File: '+file_and_path[0])
                if "#########" == mmap_list[2]:
                    break
                else:
                    next_p=int(mmap_list[2])
        else:
            print("No folder Open!Maybe Try closing file")

    def show_mmap(self):
        next_pointer=self.next_p_start
        mmap_files = []
        while True:
            mmap_list,null = self.get_lists_for_mmap(next_pointer)
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
                    self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    file_data_pointer = lines[-10:-1]
                    data+=lines[0:len(lines)-10]
                    if file_data_pointer == "#########":
                        break
                
                print('\nFile Name:'+file_name+'\tFile Path:'+path+'\tFile Data Length: ',len(data),'bytes')
            if "#########" in mmap_list[2]:
                break
            
            next_pointer = int(mmap_list[2])
        
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
                self.create_room_in_mmap(self.mmap_object.size()+size_of_mmapWriteforFile)
                self.mmap_object.seek(present_location)
                self.mmap_object.write(str(mmapWriteforFile).encode())
                temp=self.current_file_open
                self.current_file_open = source
                self.delete_file()
                self.current_file_open = temp
        else:
            print("Invalid Source!")
            
    def move_data(self,startStr,sizeStr,targetStr):
        if '/#' in self.current_file_open:
            print("No File Open")
        else:
            desired_list,current=self.mmap_for_specific_file(self.current_file_open)
            if "#########" == desired_list[1]:
                print('NO DATA IN THIS FILE!')
            else:
                start=int(startStr)
                size=int(sizeStr)
                target=int(targetStr)
                data=''
                data_pointers=[]
                data_size=[]
                file_data_pointer = desired_list[1]
                while True:
                    print(file_data_pointer)
                    data_pointers.append(int(file_data_pointer))
                    self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    data+=lines[0:len(lines)-10]
                    data_size.append(len(lines)-10)
                    file_data_pointer = lines[-10:-1]
                    if file_data_pointer == "#########":
                        break
                
                if len(data)<start+size-1:
                    print("Data Location Out of Range")
                elif len(data)<target+size-1:
                    print("Target Out Of Range")
                else:
                    length=len(data)
                    data_to_move=data[start-1:start+size-1]
                    print("data_to_move",data_to_move)
                    data= data.replace(data_to_move,'')
                    print("data",data)
                    if target == 1:
                        data_after_move = data_to_move + data
                    elif target-size ==len(data)-size:
                        data_after_move = data + data_to_move
                    else:
                        data_after_move = data[0:target-1] + data_to_move + data[target-1:]
                    
                    location_to_write_at_location=current-20
                    location_to_write=str(self.mmap_object.size())
                    location_to_write=location_to_write.strip().zfill(9)
                    
                    self.mmap_object.seek(location_to_write_at_location)
                    self.mmap_object.write(str(location_to_write).encode())
                    self.create_room_in_mmap(self.mmap_object.size()+len(data_after_move)+10)
                    self.mmap_object.seek(int(location_to_write))
                    self.mmap_object.write(str(data_after_move+'#########\n').encode())
                    
    def truncate_data(self,sizeStr):
        if '/#' in self.current_file_open:
            print("No File Open")
        else:
            desired_list,current=self.mmap_for_specific_file(self.current_file_open)
            if "#########" == desired_list[1]:
                print('NO DATA IN THIS FILE!')
            else:
                size=int(sizeStr)
                data=''
                data_pointers=[]
                data_at_pointer_size=[]
                data_at_pointer=[]
                file_data_pointer = desired_list[1]
                while True:
                    data_pointers.append(int(file_data_pointer))
                    self.mmap_object.seek(int(file_data_pointer))
                    lines = self.mmap_object.readline().decode()
                    file_data_pointer = lines[-10:-1]
                    lines=lines[0:len(lines)-10]
                    data+=lines
                    data_at_pointer.append(lines)
                    data_at_pointer_size.append(len(lines))
                    if file_data_pointer == "#########":
                        break
                data_size=len(data)
                if data_size<size:
                    print("Truncate size Out of Range")
                elif data_size==size:
                    self.mmap_object.seek(current-20)
                    self.mmap_object.write("#########")
                else:
                    data_size_after_truncate=data_size-size
                    i=0
                    while True:
                        if data_size_after_truncate < data_at_pointer_size[i]:
                            break
                        data_size_after_truncate-=data_at_pointer_size[i]
                        i+=1
                    location_to_write_at_location=''
                    if i < 2:
                        location_to_write_at_location=current-20
                    else:
                        location_to_write_at_location=data_pointers[i-1]+data_at_pointer_size[i-1]
                    if data_size_after_truncate==0:
                        location_to_write='#########'
                        self.mmap_object.seek(location_to_write_at_location)
                        self.mmap_object.write(str(location_to_write).encode())
                    else:
                        data_to_write=data_at_pointer[i]
                        data_to_write=data_to_write[:data_size_after_truncate]+'#########\n'
                        location_to_write=str(self.mmap_object.size())
                        location_to_write=location_to_write.strip().zfill(9)
                        self.mmap_object.seek(location_to_write_at_location)
                        self.mmap_object.write(str(location_to_write).encode())
                        self.create_room_in_mmap(self.mmap_object.size()+len(data_to_write))
                        self.mmap_object.seek(int(location_to_write))
                        self.mmap_object.write(data_to_write.encode())  
                    
                
# with FileHandling() as fh:
        # fh.create_file('my1file')
        # fh.create_file('my2file')
        # fh.create_file('my3file')
        # fh.create_file('my4file')
        # fh.create_file('my5file')
        # fh.delete_file('my6file')
        # fh.create_file('my6file')
        # fh.open_file('my5file')
        # fh.read_file()
        # fh.write_file()