# Yscan
fast scan tool written using python give you all open ports and the service with the version to search if there are exploits for its
- the script provide you with possible open ports
- provide you with services with version
- can search about exploits for these versions of services
- you need to input the ip address of the machine
- you need to input the start port
- you need to input the end port
- also input the number of threads default 10 or 100
- this is an addition (exist gui for the tool (guiscan.py) ).
  
## running Exmaple
- ip address like 192.168.8.146
- start port like 1
- end port like 65535
- threads like 100
  
>> the Output results are (the open ports) , (the services) , (the versions).


### to run this tool you need to install some python libraries 

> run this command in you terminal


#### this library for the banner of the tool 
```
pip install pyfiglet
```
#### to get this tool run this command line
```
git clone https://github.com/Youssef530245/Yscan.git
```

#### to run the tool run this command line 
```
python3 scan.py
```
>> this an image show the results
![Yscan](https://github.com/Youssef530245/Yscan/blob/main/photo.png?raw=true "photo.png")


### if you want to run the gui script (GuiScan.py) You need to install this library also
```
sudo apt-get install python3-tk
```
### to run the script (GuiScan.py)
```
python3 GuiScan.py
```
>> here an image show the results of run the GuiScan.py

![Yscan](https://github.com/Youssef530245/Yscan/blob/main/gui.png?raw=true "gui.png")



**I'M Eng: Youssef Mohamed 🌏🌏 would like to thank you for reading**
