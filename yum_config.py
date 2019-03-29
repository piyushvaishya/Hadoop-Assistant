#!/usr/bin/python36
from subprocess import getoutput

def yum_configuration():
	yum_name = input("Enter yum name: ")
	yum_url = input("Enter URL: ")
	yum_signature_verification = input("Signature verification on(1)/off(0): ")
	getoutput("echo '[{}]' >> /etc/yum.conf".format(yum_name))
	getoutput("echo 'baseurl={}' >> /etc/yum.conf".format(yum_url))
	getoutput("echo 'gpgcheck={}' >> /etc/yum.conf".format(yum_signature_verification))
	print("\t\tYum configuration successful...\n")
        
