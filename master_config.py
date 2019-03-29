#!/usr/bin/python36

#importing lib
import os
from subprocess import getoutput
import java_config

def master_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip):
	print("Configuring master...")
	print("\t1. Installation...")
	
	#installing java
	print("\t\tJava installation...")
	java_config.java_configuration_self()

	#installing hadoop
	print("\n\t\tChecking if HADOOP PROGRAM is already installed")
	x = getoutput("hadoop version")
	if 'Hadoop 1.2.1' in x:		
		print("\t\tHadoop program already installed...")
	else:
		print("\t\tNot installed...")
		print("\t\tInstalling Hadoop program...")		
		os.system("rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force")
		x = getoutput("hadoop version")
		if 'Hadoop 1.2.1' in x:			
			print("\t\tHadoop installation successful...\n")
		else:
			print("\tSystem Error...")
			print("\tCheck your system and try again...\n")

	#setting up master
	print("\t2. Setting up Master")
	
	#host file entry
	print("\t\tWriting host file...")
	getoutput(f"echo '{master_ip} master.{domain_name}' >> /etc/hosts")
	getoutput(f"echo '{client_ip} client.{domain_name}' >> /etc/hosts")
	getoutput(f"echo '{job_tracker_ip} jt.{domain_name}' >> /etc/hosts")
	i=1
	for x in slaves_ip:
		getoutput(f"echo '{x} st{i}.{domain_name}' >> /etc/hosts")
		i+=1	

	#set hostname
	print("\t\tSetting up host-name...")
	getoutput(f"hostnamectl set-hostname master.{domain_name}")

	#writing configuration file
	print("\t\tWriting configuration files...")
	
	getoutput("""echo '<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!-- Put site-specific property overrides in this file. -->
<configuration>
<property>
<name>dfs.name.dir</name>
<value>/name</value>
</property>
</configuration>' > /etc/hadoop/hdfs-site.xml""")
	
	getoutput("""echo '<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!-- Put site-specific property overrides in this file. -->
<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://master.{}:9001</value>
</property>
</configuration>' > /etc/hadoop/core-site.xml""".format(domain_name))

	#creating folder
	print("\t\tCreating folder for namenode...")
	getoutput("mkdir /name")

	#format namenode
	print("\t\tFormatting namenode...")
	os.system("hadoop namenode -format")
	
	#turn firewall off
	getoutput("iptables -F")

	#writing rc.local file
	getoutput("echo 'hadoop-daemon.sh start namenode' >> /etc/rc.d/rc.local")
	getoutput("echo 'iptables -F' >> /etc/rc.d/rc.local")
	getoutput("chmod +x /etc/rc.d/rc.local")


	#start namenode service
	print("\t\tStarting Master's service...")
	getoutput("hadoop-daemon.sh start namenode")
	x = getoutput("jps")
	if 'NameNode' in x:	
		print("\t\tConfiguration successful...")
		print("\t\tMaster services started...\n")
	else:
		print("\t\tSystem Err...")
		print("\t\tCheck your system and try again...\n")
