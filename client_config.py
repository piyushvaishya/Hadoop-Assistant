#!/usr/bin/python36

#importing lib
import os
from subprocess import getoutput
import java_config

def client_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip):
	print("Configuring Client...")
	print("\t1. Installation...")
	
	#transfering files
	print("\t\tTransfering files...")
	os.system(f"scp /root/jdk-8u171-linux-x64.rpm {client_ip}:/root/")
	os.system(f"scp /root/hadoop-1.2.1-1.x86_64.rpm {client_ip}:/root/")
	
	#installing java
	print("\t\tJava installation...")
	java_config.java_configuration(client_ip)

	#installing hadoop
	print("\n\t\tChecking if HADOOP PROGRAM is already installed...")
	x = getoutput(f"ssh {client_ip} hadoop version")
	if 'Hadoop 1.2.1' in x:		
		print("\t\tHadoop program already installed...")
	else:
		print("\t\tNot installed...")
		print("\t\tInstalling Hadoop program...")		
		getoutput(f"ssh {client_ip} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force")
		x = getoutput(f"ssh {client_ip} hadoop version")
		if 'Hadoop 1.2.1' in x:		
			print("\t\tHadoop installation successful...\n")
		else:
			print("\t\tSystem Error...")
			print("\t\tCheck your system and try again...\n")


	#setting up Job_Tracker
	print("\t2. Setting up Client...")
	
	#host file entry
	print("\t\tWriting host file...")
	getoutput(f"scp /etc/hosts {client_ip}:/etc/")

	#set hostname
	print("\t\tSetting up host-name...")
	getoutput(f"ssh {client_ip} hostnamectl set-hostname client.{domain_name}")

	#writing configuration file
	print("\t\tWriting configuration files...")
	getoutput(f"scp /root/auto_project/client_conf_files/core-site.xml {client_ip}:/etc/hadoop/")
	getoutput(f"scp /root/auto_project/client_conf_files/mapred-site.xml {client_ip}:/etc/hadoop/")

	print("\t\tClient configuration successful...\n")
