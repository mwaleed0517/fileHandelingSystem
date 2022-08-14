ABOUT_FILES:
	"MAIN_LAB_10_server"
		--- This file is used to run the server and all client commands. Handling is being done here and use "Server_FUNCS_LAB_10" to interact with "core logic"
	"Server_FUNCS_LAB_10"
		--- This file has all the functionality related to FILE HANDLING (INTERACTION WITH MMAP)
	"MAIN_LAB_10_client"
		--- This file is used to interact with user and take commands and use "Client_FUNCS_LAB_10" to interact with server
	"Client_FUNCS_LAB_10"
		--- This file has functionality related to interaction with server

STARTING PROGRAM:
	""" RUNS ON SAME NETWORK """
	"FOR SERVER"
		- Place "MAIN_LAB_10_server" and "Server_FUNCS_LAB_10" in same Folder/Location(Make sure no other file with name MMAP exist there)
		-- Run "MAIN_LAB_10_server" (MMAP file is not needed, but it if does not exist it will be created)
		--- Enter Port No. for the socket
		""" ...SERVER IS UP AND RUNNING... will be displayed if succesfull"""
		""" Other wise Error will be displayed """
	"FOR CLIENT"
		""" Once the server runs it will show the IP Address for server. Get that IP Address from server operator"""
		""" Make sure server is running before you run client """
		- Place "MAIN_LAB_10_client" and "Client_FUNCS_LAB_10" in same Folder/Location.
		-- Run "MAIN_LAB_10_client"
		""" It will ask for Port and IP Address for the server socket """
		""" ...Server connected... will be displade if succesfull"""
		""" Other wise Error will be displayed """

		EXTRAS 	""" If you dont want to enter IP and Port again again do as following """
			" Runing client and server on same machine and client get ip automatically "
				""" In "Client_FUNCS_LAB_10" """
				- Commented lines (18,22)
				-- Uncomment (20,21)
			" Client Using Permanent Port "
				""" In "Client_FUNCS_LAB_10" """
				- Commented lines (19)
				-- Uncomment (23 with user specified port as integer)
			" Client Using Permanent Server IP "
				""" In "Client_FUNCS_LAB_10" """
				- Commented lines (18,20,21)
				-- Uncomment (22 with user specified IP in commas as string)
			" Server Using Permenent Port "
				""" In "MAIN_LAB_10_server" """
				- Commented lines (96)
				-- Uncomment (99 with user specified port as integer)

CLEINT COMMAND/PROTOCOL:
	- Built in help function is given """ RUN "MAIN_LAB_10_client" and enter 'help' """
	-- COMMANDS DETAIL
		mk fileName			""" To create a file """
		tmkdir folderName		""" To crete folder """
		open FileNAme			""" To open a file """
		opendir folderName		""" To open a folder """
		close				""" To close current File/Folder open """
		delete				""" To delete current File open """ (Folder cannot be deleted)
		read				""" To read data in current File open """
		write mode(a/w)			""" To write data in current File open """
		mv fileName Source Destination
			""" Move file from Soucer folder to destination folder(Notice: For main/super folder use /# as source or destination)
		mvdata Start Size target	""" To move data of given size from start to target location in file """
            	mrdata Size			""" To truncate data of given size from file """
            	ls				""" To show files and Folder in current folder open """
            	lsall				""" To show all files and their locations along with data length """
            	exit				""" To Close Program """
	--- RULES:
		""" Commands to be seperated from Names and paths with blanck spaces """
		""" Commands are case sensitive exept 'help' """
            	""" Name can not contain blank space ' ', comma ',', slash '/' or hash '#' """
		""" If space is given in the end of command If will reaise execption """