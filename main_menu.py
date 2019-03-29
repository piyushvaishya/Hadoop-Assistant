#!/usr/bin/python36

#importing libraries
import sys
import os
import yum_config
import java_config
import master_config
import job_tracker_config
import client_config
import slave_config

def menu():
	print("\nWe can help you in...")
	print("\n\tPress 1: For YUM configuration")
	print("\tPress 2: For JAVA installation")
	print("\tPress 3: For Hadoop Cluster configuration")
	print("\tPress 4: To Exit")
	print("\tEnter your choice: ", end = '')
	menu_choice=int(input())
	if menu_choice == 1:
		yum_config.yum_configuration()
	elif menu_choice == 2:
		java_config.java_configuration_self()
	elif menu_choice == 3:
		#input cluster info...
		cluster_size = int(input("Enter the cluster size(Master+Slaves): "))
		domain_name = input("Enter domain name for the cluster: ")
		master_ip = input("Enter master's IP address: ")
		job_tracker_ip = input("Enter job tracker's IP address: ")
		client_ip = input("Enter client's IP address: ")
		slaves_ip = []
		for x in range(1,cluster_size):
			print(f"Enter slave-{x} IP address: " , end = '')
			ip = input()
			slaves_ip.append(ip)

		#calling master
		master_config.master_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip)

		#calling job_tracker
		job_tracker_config.job_tracker_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip)

		#calling Client
		client_config.client_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip)

		#calling slave
		slave_config.slave_configuration(cluster_size,domain_name,master_ip,job_tracker_ip,client_ip,slaves_ip)
	else:	
		os.system("clear")		
		sys.exit(0)
