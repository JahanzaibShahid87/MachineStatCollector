#MachineStatCollector

##Prerequisites or Dependencies are:
>1. OS Linux  or for windows use bash for linux 
1. Python 2.7
2. Postgresql installed


##Project Setup
>1. Clone MachineStatCollector project 

>2. Move to source directory
	```cd JahanzaibShahidSiddiqui_SR_Python_SysInfo/Source/MachineStatCollector```

>3. Install requirements 
	```pip install -r requirements.txt```
	you can also create virtual enviornment for above requirement's installation.
	if there is fatal error please upgrade pip and try above installation command again
	```pip install --upgrade pip```

>4. create database user and database
	```./create.db.sh```

>5. open settings.ini
	```
	set MAIL_SENDER_EMAIL, MAIL_SENDER_PASS values so you will get email if threshold reached
	```

>6. Run tests
	```behave```

>7. Run Project
	Update config.xml
	```python server.py```

>8. To view logs
	```tail -f collect.log```


##Assumptions:
Client should be accessable by username and password not by SSH KEY.
Client was on linux as I have only tested on linux system.
Project server side is running on linux too. 

##Requirements Not Covered in project.
Windows client no covered,	and also encryption/decryption not covered as i am communicating through ssh by using paramiko and its already encrypted.

##Feedback:
Its really good and different type of assignment but there should be sample smtp client credentials provided by crossover so we set that credentails in settings.ini.  