# Near Realtime RIC. 
***
Near-RT RIC is located in RAN, receiving and analyzing real-time information from RAN, combined with additional information provided by Non-RT RIC. Use machine learning model deployed by Non-RT RIC to monitor or predict changes in user connection status. According to the policies and changes set by Non-RT RIC, the RAN parameters can be adjusted to allow each user to maintain the established policy goals.
***
## Near Realtime RIC Installation
#### VM Minimum Requirments for RIC 
* OS: Ubuntu 18.04 LTS (Bionic Beaver).  
* CPU(s):  4.  
* RAM: 16 GB.  
* Storage: 160 GB.  

#### Step.1 Obtaining the Deployment Scripts and Charts
```
$ sudo -i

$ git clone http://gerrit.o-ran-sc.org/r/it/dep -b bronze

$ cd dep
$ git submodule update --init --recursive --remote
```
#### Step.2 Generation of cloud-init Script 
```
$ cd tools/k8s/bin
$ ./gen-cloud-init.sh   # will generate the stack install script for what RIC needs
```
#### Note:  
The outputted script is will be used for preparing K8 cluster for RIC deployment (k8s-1node-cloud-init-k_1_16-h_2_12-d_cur.sh)

#### Step.3 Installation of Kubernetes, Helm, Docker, etc.
```
$ ./k8s-1node-cloud-init-k_1_16-h_2_12-d_cur.sh
```
#### NOTE:   
Be patient as this takes some time to complete. Upon completion of this script, the VM will be rebooted.  You will then need to login to the VM and run sudo once again.
```
$ sudo -i

$ kubectl get pods --all-namespaces  # There should be  9 pods running in kube-system namespace.
```
#### Step.4 Deploy RIC using Recipe
```
$ cd dep/bin
$ ./deploy-ric-platform -f ../RECIPE_EXAMPLE/PLATFORM/example_recipe.yaml
$ kubectl get pods -n ricplt    
```
#### note:  
ERROR: Can't locate the ric-common helm package in the local repo. Please make sure that it is properly installed.  
You just need to initialize Helm repositories with the following :
```
$ helm init --stable-repo-url=https://charts.helm.sh/stable --client-only
```
#### Step.5 Onboarding a Test xApp(HelloWorld xApp)
```
$ cd dep

# Create the file that will contain the URL used to start the on-boarding process...
$ echo '{ "config-file.json_url": "https://gerrit.o-ran-sc.org/r/gitweb?p=ric-app/hw.git;a=blob_plain;f=init/config-file.json;hb=HEAD" }' > onboard.hw.url

# Start on-boarding process...

$ curl --location --request POST "http://$(hostname):32080/onboard/api/v1/onboard/download"  --header 'Content-Type: application/json' --data-binary "@./onboard.hw.url"


# Verify list of all on-boarded xApps...
$ curl --location --request GET "http://$(hostname):32080/onboard/api/v1/charts"
```
#### Step.6 Deploy Test xApp(HelloWorld xApp)
```
#  Verify xApp is not running...  This may take a minute so refresh the command below
$ kubectl get pods -n ricxapp



# Call xApp Manager to deploy HelloWorld xApp...

$ curl --location --request POST "http://$(hostname):32080/appmgr/ric/v1/xapps"  --header 'Content-Type: application/json'  --data-raw '{"xappName": "hwxapp"}'



#  Verify xApp is running...

$ kubectl get pods -n ricxapp



#  View logs...

$ kubectl logs -n ricxapp <name of POD retrieved from statement above>
```
