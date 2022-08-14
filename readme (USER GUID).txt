		...(USER GUID)...
ABOUT_SYSTEM:
	The system can be run on limitless no of computers only if they are connected with  router...(COMPUTERS MUST BE IN SAME NETWORK).
	If you wish to run server over www then you need to create a web server with static ip.
	RUN server on any computer and then your system run clints on any computer. For more details follow ABOUT_FILES section.

ABOUT_FILES:
	"SERVER"
		--- This file is used to run the server and all client commands. Handling is being done here and use "SERVER_FUNCS" to interact with "core logic"
	"SERVER_FUNCS"
		--- This file has all the functionality related to FILE HANDLING (INTERACTION WITH MMAP)
	"CLIENT"
		--- This file is used to interact with user and take commands and use "CLIENT_FUNCS" to interact with server
	"CLIENT_FUNCS"
		--- This file has functionality related to interaction with server

STARTING PROGRAM:
	""" RUNS ON SAME NETWORK """
	"FOR SERVER"
		- Place "SERVER" and "SERVER_FUNCS" in same Folder/Location(Make sure no other file with name MMAP exist there)
		-- Run "SERVER" (MMAP file is not needed, but it if does not exist it will be created)
		--- Enter Port No. for the socket
		""" ...SERVER IS UP AND RUNNING... will be displayed if succesfull"""
		""" Other wise Error will be displayed """
	"FOR CLIENT"
		""" Once the server runs it will show the IP Address for server. Get that IP Address from server operator"""
		""" Make sure server is running before you run client """
		- Place "CLIENT" and "CLIENT_FUNCS" in same Folder/Location.
		-- Run "CLIENT"
		""" It will ask for Port and IP Address for the server socket """
		""" ...Server connected... will be displade if succesfull"""
		""" Other wise Error will be displayed """

		EXTRAS 	""" If you dont want to enter IP and Port again again do as following """
			" Runing client and server on same machine and client get ip automatically "
				""" In "CLIENT_FUNCS" """
				- Commented lines (18,22)
				-- Uncomment (20,21)
			" Client Using Permanent Port "
				""" In "CLIENT_FUNCS" """
				- Commented lines (19)
				-- Uncomment (23 with user specified port as integer)
			" Client Using Permanent Server IP "
				""" In "CLIENT_FUNCS" """
				- Commented lines (18,20,21)
				-- Uncomment (22 with user specified IP in commas as string)
			" Server Using Permenent Port "
				""" In "SERVER" """
				- Commented lines (96)
				-- Uncomment (99 with user specified port as integer)

CLEINT COMMAND/PROTOCOL:
	- Built in help function is given """ RUN "CLIENT" and enter 'help' """
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