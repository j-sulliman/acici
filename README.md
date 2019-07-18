# nxos_to_aci: automate ACI configuration of low complexity, high volume configuration items in legacy network
Imports L2 constructs (VLANs, SVIs and associated VRF) from Legacy NXOS configuration, 
Imports into Django models DB
Bul clean of data (e.g EPG/BD naming convention) 
Option editing of imported data  
Post imported objects to APIC (EPGS are be default included in a preferred group)

# Setup
$ python3 -m venv venv
$ source venv/bin/activate
$ git init
$ git pull https://github.com/j-sulliman/nxos_to_aci.git

Install the required dependencies:
$ pip3 install -r requirements.txt

# Start Django Server
$ python3 manage.py runserver 0:8080
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 18, 2019 - 13:17:42
Django version 2.2.2, using settings 'nxos_aci.settings'
Starting development server at http://0:8080/
Quit the server with CONTROL-C.

# Logon and Import NXOS file
i.e. http://127.0.0.1:8080
Login as admin/C1sc0123

Menu --> Upload Config File
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.23.58%20PM.png)

Provide the defaults for configuration naming convention and BD construct.  BD mode in most cases should be l2 which will enable ARP and BUM flooding.  L3 mode will enable unicast routing and configure the SVI address as a BD Subnet.
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.26.01%20PM.png)


View and Edit the Imported configuration
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.51.46%20PM.png)

Enter the APIC connection info and submit
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.52.47%20PM.png)


View the resulting JSON and HTTP Post status code
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.56.15%20PM.png)


Check the APIC
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.57.24%20PM.png)

# Create associated fabric access policies and L3Os manually
Rational - items like Physical domain, vlan pools to legacy network will likely only be configured once.  
Fabric access policies therefore less onerous than tenant policy.

L3Os configuration very environment dependant.

# Note
Tested against NXOS 7.X configuration files, may work with IOS but needs testing.
Use at your own risk - recommend dry-run against a simulator or non-prod APIC
