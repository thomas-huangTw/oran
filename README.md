# ORAN xApp introduction
***
The internal architecture of xApp can be divided into different parts, among which xApp includes Near Real Time RAN Intelligent Controller (Near-RT RIC) libraries and RIC Message Router (RMR) libraries.
xApp and other Components use RMR for data exchange and communication, and stores data through Shared Data Layer (SDL).  

Before establishing the Near-RT RIC system, you need to install the basic system environment including Kubernetes, Docker, RMR, SDL, E2 Node, E2 Termination, Redis database and xApp Framework, etc. This report will explain in detail how to establish the system environment and the deployment of RMR and xApp. This report will explain in detail how to establish the system environment and the deployment of RMR and xApp. For related E2 Node, E2 Termination, Redis database, and SDL information, please refer to Open Radio Access Network (O-RAN) official documents for detailed instructions.  

This report explains how xApp communicates with E2 Node and how to build a basic xApp. In addition, the report also details how to use the xApp Framework and the xApp API package. The xApp Framework assembles the complex structure of RMR into a package, and the xApp API combines the complex RMR settings and Message Type into simple commands, which is beneficial to speed up the development of xApp by developers.
***
## What is xApp?
xApp is designed for applications running on Near-RT RIC in O-RAN architecture. The application may contain one or more microservices, and xApp can interact with the base station after adding Near-RT RIC. For example: the base station reports data to xApp, and can also control the parameter settings of the base station through Control commands, etc. The application is independent of Near-RT RIC and can be provided by any third party software. xApp can communicate with E2 Node through the Near-RT RIC Procedure defined by O-RAN, such as Subscription, Control, Indication Report, etc.
***
## Installation environment requirements for xApp
1. Before using and installing xApp, you need to have a basic understanding of the Python programming language.
Python tutorial, please refer to Python: https://docs.python.org/3/tutorial/

In addition, in order for xApp to be deployed smoothly, the following environment settings must be adopted:
* Execution environment: Docker and Python environment.
* Supported programming language: Python version 3.7 or above
* Operating system: Ubuntu 18.04 or above.
* Communication between xApp and other components: RMR
### Install Docker Engine
https://docs.docker.com/engine/install/ubuntu/
#### Installation example:
**1. Set up the repository**  

Update the apt package index
```
$ sudo apt-get update
```  
Install Docker-related packages  
```
$ sudo apt-get install \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg \
       lsb-release
```
Add Docker’s official GPG key  
```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```  
Add Stable version of the repository  
```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```  
**2. Install Docker Engine**  

Update the apt package index, and install the latest version of Docker Engine and containerd
```
$ sudo apt-get update  
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```
Verify that Docker Engine is installed correctly
```
$ sudo docker -v
$ sudo docker run hello-world
```
