#!/usr/bin/python36

#importing lib
import os
from subprocess import getoutput

def java_configuration_self():
	print("\t\tChecking if JAVA PROGRAM is already installed")
	x = getoutput("java -version")
	if 'java version "1.8.0_171"' in x:
		print("\t\tJava program already exits...")
	else:
		print("\t\tNot installed...")		
		print("\t\tInstalling java program...")
		os.system("rpm -ivh /root/jdk-8u171-linux-x64.rpm")
		
		print("\t\tSetting up java path...")
		getoutput("echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/' ")
		getoutput("echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH' ")
		getoutput("echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/' >> /root/.bashrc")
		getoutput("echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH' >> /root/.bashrc")
		
		#os.system("exec bash")
		
		x = getoutput("java -version")
		if 'java version "1.8.0_171"' in x:
			print("\t\tJava successfully installed\n")
		else:
			print("\t\tSystem Err...")
			print("\t\tCheck your system and try again...\n")



def java_configuration(ip_address):
	print("\t\tChecking if already installed")
	x = getoutput(f"ssh {ip_address} java -version")
	if 'java version "1.8.0_171"' in x:
		print("\t\tJava program already exits...")
	else:
		print("\t\tNot installed...")		
		print("\t\tInstalling java program...")
		os.system(f"ssh {ip_address} rpm -ivh /root/jdk-8u171-linux-x64.rpm")
		
		print("\t\tSetting up java path...")
		getoutput(f"ssh {ip_address} echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/'")
		getoutput(f"ssh {ip_address} echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH'")
		getoutput(f"ssh {ip_address} 'echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc' ")
		getoutput(f"ssh {ip_address} 'echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH >> /root/.bashrc' ")
		
		
		x = getoutput(f"ssh {ip_address} java -version")
		if 'java version "1.8.0_171"' in x:
			print("\t\tJava successfully installed\n")
		else:
			print("\t\tSystem Err...")
			print("\t\tCheck your system and try again...\n")
