# pade_flask API Application

- Point of contact: [John Bowyer](mailto:zfi4@cdc.gov)
- Organizational unit: OCIO
- Related projects: EDC
- Related investments:  Pending Public Release
- Governance status: Pending Public Release
- Program official:  [Erik Knudsen](mailto:knu1@cdc.gov)

## pade_flask API Overview

A Python Rest API with functionality to support a react client application and interface/extract information from a Synapse Serverless Database and Alation.

## Geting Started

### Clone the Flask App App Locally

#### Clone the Flask App in POSIT (Primary)

1. Select Ctrl Shift P
2. Select clone
3. Enter https://github.com/cdcent/data-ecosystem-services.git
4. Complete prompt and authorize
5. Clone to your home directory

### Config POSIT (One Time Only)

```sh
make posit-config
```

Add the following to ~/.bashrc

```sh
export OCIO_PADE_DEV_POSIT_SECRET=YOUR_POSIT_TOKEN
export OCIO_PADE_DEV_EDC_SECRET=YOUR_EDC_TOKEN
````

Run

```sh
source ~/.bashrc
```

### Run the Flask App Locally

#### Run the Flask App Locally on POSIT  (Primary)

```sh
cd pade_flask/data_ecosystem_flask
workon OCIO_PADE_DEV
make flask-run-posit-dev
```

#### View Logs Locally

Where zfi4=your_alias

/r-share/home/zfi4/.virtualenvs/OCIO_PADE_DEV/share/.data_ecosystem_services_services_errors.log

#### SetUp Deployment Env

``` sh
/opt/python/3.9.9/bin/python3 -m venv .venv-3.9.9
source .venv-3.9.9/bin/activate
cd ~/data-ecosystem-services/pade_flask/data_ecosystem_flask
poetry lock
poetry install
poetry export -f requirements.txt --output requirements.txt --without-hashes 
```

#### Deploy the Flask App on POSIT (Primary)

``` sh
cd ~/data-ecosystem-services/pade_flask/data_ecosystem_flask
workon OCIO_PADE_DEV
make posit-deploy
```

#### Run your Flask App Locally on Ubuntu or WSL

Steps to test web site

- Next go to posit exension in VS Code
- Click the name of proxied server
- Launch server - if you receive 404 you may need to add /swagger to proxied url
- Test web site

#### Run your Flask App Locally on Ubuntu or WSL

```sh
cd pade_flask/data_ecosystem_flask
workon OCIO_PADE_DEV
make flask-run-wsl
```

Browse the Application at http://127.0.0.1:5000/download-excel

## Debug

nano ~/.virtualenvs/OCIO_PADE_DEV/share/data_ecosystem_services_services_logging.txt

## Installation

### Check if Python is installed

Run in bash or powershell

1. Check Python Version

```sh
make python-check
```

### Install Python 3.9

#### Install Python on POSIT  (Primary)

Should be install by default. Confirm with

```sh
make python-create-posit
```

#### Install Python on Ubuntu or WSL

```sh
make python-create-wsl
```

### Install Pip

#### Install Pip on POSIT (Primary)

Should be install by default. Confirm with

```sh
make pip-check
```

#### Install Pip on Ubuntu or WSL 

```sh
make pip-create-wsl
```

### Install Virtual Environment

#### Install Virtual Environment on Ubuntu or WSL (Primary)

```sh
make venv-create-wsl
```

#### Install Virtual Environment on POSIT

Should be install by default. Confirm with

#### Install Root Virtual Environment on All Platforms

If first environment, create venv root

```sh
make venv-create-root
```

#### Install Project Virtual Environment on All Platforms

```sh
make venv-create-OCIO-PADE-DEV
```

### Install Flask App

#### Install Flask App on All Platforms

```sh
workon OCIO_PADE_DEV
make flask-create-OCIO-PADE-DEV:
```

### To Add a Library to Setup on All Platforms

1. Go to project directory

```sh
cd pade_flask/data_ecosystem_flask
```

2. Open Terminal and workon virtual environment

```sh
workon OCIO_PADE_DEV
```

3. Add Libraries

Examples:

```sh
poetry add six
poetry add openpyxl
poetry add oauthlib
poetry add certifi
poetry add flask
poetry add xlsxwriter        
```

4. Update Libraries

```sh
cd data_ecosystem_flask
poetry update
poetry install
```

### Install RSConnect in POSIT

```sh
poetry add rsconnect-python
```

### Install VA-API driver

1. Check if the VA-API driver is installed on your system by running the following command in the terminal:

```sh
vainfo
```

If you see an error message saying "command not found" or similar, it means that the VA-API driver is not installed on your system. In that case, you can install the driver using the package manager for your system (e.g. apt-get for Ubuntu/Debian, dnf for Fedora, pacman for Arch Linux, etc.).

2. Install the necessary VA-API driver packages on your system using the package manager. For example, on Ubuntu/Debian, you can run the following command:

```sh
cd $HOME
sudo apt-get install i965-va-driver vainfo
```

3. Launch nano and add the following lines to the end of the .bashrc file:

```sh
nano ~/.bashrc
export LIBVA_DRIVERS_PATH=/usr/lib/x86_64-linux-gnu/dri
```

4. Run update. NOTE: Log out of ZScaler

```sh
sudo apt-get update
```

5. Run Intel driver update or equivalent

```sh
sudo systemctl stop vainfo.service
sudo apt-get remove i965-va-driver
sudo add-apt-repository ppa:oibaf/graphics-drivers
sudo apt-get update
#sudo apt-get install xserver-xorg-video-intel
#sudo apt-get install i965-va-driver intel-media-va-driver-non-free
sudo apt-get install --reinstall intel-media-va-driver:amd64
# sudo apt-get install intel-media-va-driver-non-free vainfo
sudo reboot
# sudo apt-get install intel-media-va-driver-non-free vainfo
vainfo 
```

### Relay Network Traffic

NOTE: Log out of ZScaler

1. Install socat by running the following command in a terminal window in WSL Ubuntu

```sh
sudo apt-get update && sudo apt-get install socat
```

2. Determine the IP address of your Windows 10 host by running the following command in a Command Prompt window in Windows:

```sh
ipconfig
```

Example: 192.168.86.26


3. In WSL Ubuntu, run the following command to set up a relay from localhost (127.0.0.1) on port 9000 to the IP address and port of your Windows 10 host:

```sh
socat TCP4-LISTEN:9000,fork,reuseaddr TCP4:WINDOWS_IP_ADDRESS:443
```

example: use LAN Port

```sh
        socat -d  TCP4-LISTEN:9000,fork,reuseaddr TCP4:136.226.12.24:443
```
socat -d TCP-LISTEN:9000,fork PROXY:136.226.12.61:443,proxyport=80


4. Get you proxy server port by visiting https://whatismyipaddress.com/proxy-check

5. In Windows, open a Command Prompt window as Administrator and run the following command to forward traffic from port 9000 to the appropriate Zscaler proxy server:

https://help.zscaler.com/z-app/configuring-port-zscaler-app-listen
Default port is 9000

```sh
netsh interface portproxy add v4tov4 listenport=9000 listenaddress=WINDOWS_IP_ADDRESS connectport=ZSCALER_PROXY_PORT connectaddress=ZSCALER_PROXY_IP_ADDRESS
```
netsh interface portproxy delete v4tov4 listenaddress=192.168.86.26 listenport=9000
example:

```sh
# DO NOT RUN COMMAND
# DO NOT RUN COMMAND THIS -> netsh interface portproxy add v4tov4 listenport=9000 listenaddress=192.168.86.26 connectport=136.226.12.61 connectaddress=9000
```

192.168.86.26
136.226.12.61
443
3128

### Configure ZScaler Proxy

To configure your Ubuntu WSL to use your Windows 10 Zscaler VPN, you can follow these steps:

1. Open a terminal window in Ubuntu WSL.
2. Edit the /etc/apt/apt.conf file using your preferred text editor, such as nano or vim. For example, you could type

```sh
sudo nano /etc/apt/apt.conf
```

Add the following line to the bottom of the file:

```sh
Acquire::http::Proxy "http://localhost:3128";
```

This assumes that you are running the Zscaler App on your Windows 10 host, and that it is configured to listen on port 3128 for incoming proxy connections. If you are using a different Zscaler configuration or proxy port, adjust the above line accordingly.

3. Save and close the /etc/apt/apt.conf file.

4. Edit the /etc/environment file using your preferred text editor. For example, you could type 

```sh
sudo nano /etc/environment
```

Add the following lines to the bottom of the file, replacing the values with the values for your specific Zscaler configuration:

```sh
http_proxy=http://127.0.0.1:9000/
https_proxy=http://127.0.0.1:9000/
```

Add the following to .bashrc

```sh
export http_proxy=http://127.0.0.1:9000/
export https_proxy=http://127.0.0.1:9000/
```

Again, this assumes that you are using the Zscaler App on your Windows 10 host, and that it is configured to listen on port 3128 for incoming proxy connections.

5. Save and close the /etc/environment file.
6. Type 

```sh
source /etc/environment 
```
to apply the changes to your current shell session.

Verify that the proxy settings have been applied correctly by typing 

```sh
env | grep -i proxy
```

This should display the http_proxy and https_proxy environment variables with the values you set.

By following these steps, you should be able to configure your Ubuntu WSL to use your Windows 10 Zscaler VPN. Note that you may need to adjust the configuration settings or ports used based on your specific Zscaler deployment and requirements.

### Configure RSConnect Certificates

To do this in Firefox, for example, you can follow these steps:

1. Navigate to  https://rconnect.edav.cdc.gov

2. Open the Firefox preferences: Click on the "Menu" button in the top-right corner of the Firefox window (the button with three horizontal lines), and select "Preferences" from the dropdown menu.

3. Go to the "Privacy & Security" settings: Click on the "Privacy & Security" tab in the left-hand menu.

4. Manage certificates: Scroll down to the "Certificates" section, and click on the "View Certificates" button.

5. Export the RSconnect Root Certificate: In the "Certificate Manager" window, click on the "Authorities" tab, and then click on the "Export" button. Select the Zscaler Root Certificate file that you downloaded (in DER format), and follow the prompts to import the certificate.

6. Copy the full chain .pem file to your home directory in ubuntu as rstudio-edav-cdc-gov.pem

7. Copy the PEM-formatted certificate to the system's root certificate store:

```sh
sudo cp ~/rstudio-edav-cdc-gov.pem /usr/local/share/ca-certificates/
```

8. sudo update-ca-certificates


### Configure ZScaler Certificates

To do this in Firefox, for example, you can follow these steps:

1. Open the Firefox preferences: Click on the "Menu" button in the top-right corner of the Firefox window (the button with three horizontal lines), and select "Preferences" from the dropdown menu.

2. Go to the "Privacy & Security" settings: Click on the "Privacy & Security" tab in the left-hand menu.

3. Manage certificates: Scroll down to the "Certificates" section, and click on the "View Certificates" button.

4. Export the Zscaler Root Certificate: In the "Certificate Manager" window, click on the "Authorities" tab, and then click on the "Export" button. Select the Zscaler Root Certificate file that you downloaded (in DER format), and follow the prompts to import the certificate.

Note that importing the Zscaler Root Certificate into your user's certificate store may not work for all applications or services that use SSL/TLS connections, and it may not provide the same level of security as installing the certificate in the system's root certificate store. You may need to consult the documentation for your specific application or service to determine the best way to install the certificate.

5. Import DER

Install the Zscaler Root Certificate: Once you have obtained the Zscaler Root Certificate, you need to install it in your system's root certificate store to ensure that SSL/TLS connections to Zscaler-protected resources are properly authenticated. You can do this by following these steps:

a. Convert the certificate from the format provided by Zscaler to the PEM format, which is compatible with OpenSSL:

```sh
openssl x509 -inform DER -in ZscalerRootCA.der -out ZscalerRootCA.pem
```

b. Copy the PEM-formatted certificate to the system's root certificate store:

```sh
sudo cp ZscalerRootCA.pem /usr/local/share/ca-certificates/
```

c. Update the root certificate store:

```sh
sudo update-ca-certificates
```

Configure the proxy settings: You need to configure the proxy settings in your system to use Zscaler as your proxy server. You can do this by setting the "http_proxy" and "https_proxy" environment variables in your shell or in your system-wide configuration files. For example:

```sh
export http_proxy="http://username:password@zscloud.net:443/"
export https_proxy="https://username:password@zscloud.net:443/"
```

Replace "username" and "password" with your Zscaler login credentials, and "zscloud.net" with the hostname of your Zscaler instance.

Restart the affected application: If you are still experiencing the "verify error:num=20:unable to get local issuer certificate" error after following the above steps, you may need to restart the affected application or service to ensure that it uses the updated root certificate store and the correct proxy settings.

### Configure SSL

The default ca-certificates PEM file in Ubuntu is located at /etc/ssl/certs/ca-certificates.crt.

This file contains a list of trusted root CA certificates that are used by OpenSSL and other SSL/TLS libraries to validate the identity of remote servers. By default, Ubuntu includes a set of well-known root CA certificates in this file, such as those issued by VeriSign, Thawte, and GeoTrust.

If you need to add additional CA certificates to the ca-certificates file, you can do so by placing them in the /usr/local/share/ca-certificates directory and running the update-ca-certificates command to update the ca-certificates file. This will ensure that your custom CA certificates are included in the list of trusted certificates used by SSL/TLS libraries on your Ubuntu system.

1. Generate a self-signed SSL certificate:

```bash
make cert
```

2. Add the SSL certificate and key to your Flask app:

In your Flask app, add the following lines to configure SSL:

```python
from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app, subdomains=True)

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
```

This will use the cert.pem and key.pem files to set up SSL for your Flask application.

3. Run your Flask app:

Run your Flask app with the following command:

```bash
cd pade_flask/data_ecosystem_flask
workon OCIO_PADE_DEV
make run
```

if you receive a port conflict error 

```bash
cd pade_flask/data_ecosystem_flask
make kill
make run~
```

This will start your Flask app with SSL enabled.

Access your Flask app over HTTPS:

```bash
google-chrome https://127.0.0.1:5000/
```

### Configure VS Code

1. Select Interpreter
2. Select ctrl+shift+ps
3. Select Python: Select Interpreter
4. Select Python 3.9.7 64-bit ('OCIO_PADE_DEV': venv)
 
### Trouble Shooting

To trouble shoot the application, see the [Trouble Shooting](../data_ecosystem_services/readme.md) section of the PADE Python project.

### Check Cert

openssl x509 -in custom-ca.pem -text
openssl x509 -in cert.pem -text

### Export Cert list

openssl crl2pkcs7 -nocrl -certfile custom-ca.pem | openssl pkcs7 -print_certs -noout > certificates.txt