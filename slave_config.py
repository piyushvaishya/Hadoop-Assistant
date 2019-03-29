#!/usr/bin/python36

#importing lib
import os
from subprocess import getoutput
import java_config

def slave_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip):
	i=1
	for x in slaves_ip:
		print(f"Configuring Slave-{i}...")
		print("\t1. Installation...")
		
		#transfering files
		print("\t\tTransfering files...")
		os.system(f"scp /root/jdk-8u171-linux-x64.rpm {x}:/root/")
		os.system(f"scp /root/hadoop-1.2.1-1.x86_64.rpm {x}:/root/")
		
		#installing java
		print("\t\tJava installation...")
		java_config.java_configuration(x)
		
		#installing hadoop
		print("\n\t\tChecking if HADOOP PROGRAM is already installed...")
		x = getoutput(f"ssh {x} hadoop version")
		if 'Hadoop 1.2.1' in x:		
			print("\t\tHadoop program already installed...")
		else:
			print("\t\tNot installed...")
			print("\t\tInstalling Hadoop program...")		
			getoutput(f"ssh {x} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force")
			x = getoutput(f"ssh {x} hadoop version")
			if 'Hadoop 1.2.1' in x:		
				print("\t\tHadoop installation successful...\n")
			else:
				print("\t\tSystem Error...")
				print("\t\tCheck your system and try again...\n")

		#setting up Job_Tracker
		print(f"\t2. Setting up Slave-{i}...")
	
		#host file entry
		print("\t\tWriting host file...")
		getoutput(f"scp /etc/hosts {x}:/etc/")

		#set hostname
		print("\t\tSetting up host-name...")
		getoutput(f"ssh {x} hostnamectl set-hostname st{i}.{domain_name}")

		#writing configuration file
		print("\t\tWriting configuration files...")

		getoutput(f"scp /root/auto_project/slave_conf_files/hdfs-site.xml {x}:/etc/hadoop/")
		getoutput(f"scp /root/auto_project/slave_conf_files/core-site.xml {x}:/etc/hadoop/")
		getoutput(f"scp /root/auto_project/slave_conf_files/mapred-site.xml {x}:/etc/hadoop/")

		#creating folder
		print("\t\tCreating folder for datanode...")
		getoutput(f"ssh {x} mkdir /data")

		#turn firewall off
		getoutput(f"ssh {x} iptables -F")

	
		#Writing rc.local file
		getoutput(f"ssh {x} 'echo iptables -F >> /etc/rc.d/rc.local' ")
		getoutput(f"ssh {x} 'echo hadoop-daemon.sh start datanode >> /etc/rc.d/rc.local' ")
		getoutput(f"ssh {x} 'echo hadoop-daemon.sh start tasktracker >> /etc/rc.d/rc.local' ")
		getoutput(f"ssh {x} chmod +x /etc/rc.d/rc.local")

	
		#starting slave service	
		print(f"\t\tStarting Slave-{i} services...")
		getoutput(f" ssh {x} hadoop-daemon.sh start datanode")
		getoutput(f" ssh {x} hadoop-daemon.sh start tasktracker")
		x = getoutput(f"ssh {x} jps")
		if 'DataNode' in x:	
			print("\t\tDatanode configuration successful...")
			print("\t\tDatanode services started...")
		if 'TaskTracker' in x:	
			print("\t\tTasktracker configuration successful...")
			print("\t\tTasktracker services started...")
		else:
			print("\t\tSystem Err...")
			print("\t\tCheck your system and try again...\n")

