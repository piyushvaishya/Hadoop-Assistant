#!/usr/bin/python36

#importing lib
import getpass
import os
import sys
import main_menu


os.system('clear')
print("\t\t\t\tWelcome to my tool")
print("\t\t\t\t------------------")


#password verification

actual_password = "root"
print("Authenticate Youself...")
password_input = getpass.getpass()
if password_input != actual_password:
        print("Authentication Failed...")
        print("System aborting...")
        sys.exit(1)
else:
	print("Authentication successful...")
	while True:
		main_menu.menu()
