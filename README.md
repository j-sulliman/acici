# nxos_to_aci
Overview:
Imports L2 constructs (VLANs, SVIs and associated VRF) from Legacy NXOS configuration, imports into Django Database.  
Cleans data before pushing to APIC

Reads an NXOS configuration file and imports key configuration into Django models DB

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
