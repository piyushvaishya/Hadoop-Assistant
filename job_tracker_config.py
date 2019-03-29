#!/usr/bin/python36

#importing lib
import os
from subprocess import getoutput
import java_config



def job_tracker_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip):
	print("Configuring Job_tracker...")
	print("\t1. Installation...")
	
	#transfering files
	print("\t\tTransfering files...")
	os.system(f"scp /root/jdk-8u171-linux-x64.rpm {job_tracker_ip}:/root/")
	os.system(f"scp /root/hadoop-1.2.1-1.x86_64.rpm {job_tracker_ip}:/root/")
	
	#installing java
	print("\t\tJava installation...")
	java_config.java_configuration(job_tracker_ip)

	#installing hadoop
	print("\n\t\tChecking if HADOOP PROGRAM is already installed...")
	x = getoutput(f"ssh {job_tracker_ip} hadoop version")
	if 'Hadoop 1.2.1' in x:		
		print("\t\tHadoop program already installed...")
	else:
		print("\t\tNot installed...")
		print("\t\tInstalling Hadoop program...")		
		getoutput(f"ssh {job_tracker_ip} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force")
		x = getoutput(f"ssh {job_tracker_ip} hadoop version")
		if 'Hadoop 1.2.1' in x:		
			print("\t\tHadoop installation successful...\n")
		else:
			print("\t\tSystem Error...")
			print("\t\tCheck your system and try again...\n")

	
	#setting up Job_Tracker
	print("\t2. Setting up Job_Tracker...")
	
	#host file entry
	print("\t\tWriting host file...")
	getoutput(f"scp /etc/hosts {job_tracker_ip}:/etc/")

	#set hostname
	print("\t\tSetting up host-name...")
	getoutput(f"ssh {job_tracker_ip} hostnamectl set-hostname jt.{domain_name}")

	#writing configuration file
	print("\t\tWriting configuration files...")
	getoutput(f"scp /root/auto_project/job_tracker_conf_files/core-site.xml {job_tracker_ip}:/etc/hadoop/")
	getoutput(f"scp /root/auto_project/job_tracker_conf_files/mapred-site.xml {job_tracker_ip}:/etc/hadoop/")
	#turn firewall off
	getoutput(f"ssh {job_tracker_ip} iptables -F")

	
	#Writing rc.local file
	getoutput(f"ssh {job_tracker_ip} 'echo iptables -F >> /etc/rc.d/rc.local' ")
	getoutput(f"ssh {job_tracker_ip} 'echo hadoop-daemon.sh start jobtracker >> /etc/rc.d/rc.local' ")
	getoutput(f"ssh {job_tracker_ip} chmod +x /etc/rc.d/rc.local")

	
	#starting job_tracker service	
	print("\t\tStarting Job tracker's service...")
	getoutput(f"ssh {job_tracker_ip} hadoop-daemon.sh start jobtracker")
	x = getoutput(f"ssh {job_tracker_ip} jps")	
	if 'JobTracker' in x:	
			print("\t\tJobtracker services started...\n")
	else:
		print("\t\tSystem Err...")
		print("\t\tCheck your system and try again...\n")
