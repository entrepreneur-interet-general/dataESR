# Deployment
## Deploy a virtual machine with Vagrant
### Requirements
You will need to install [https://www.vagrantup.com/docs/installation/](Vagrant)
in your local machine before.
### Manual
Once it is done, you will be able to run the command `vagrant up` in this folder to start the installation of the box.
To connect to the machine the, run `vagrant ssh` from the same directory.
### Current actions
The machine installs for now :
* Python(latest 2.7) with the packages `virtualenv` and `virtualenvwrapper`.
* Docker.
* Deploy a `mongodb` docker container on port `27017`.
