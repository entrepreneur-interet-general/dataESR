Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |vb|
     vb.memory = "1024"
     vb.name = "dev"
  end

$python = <<SCRIPT
    echo Installing python, packages...
    sudo apt-get update
    sudo apt-get install -y python-virtualenv virtualenvwrapper git \
        mercurial build-essential python-dev zlib1g-dev \
        zlib1g zlibc libtool libffi-dev libssl-dev libpq-dev libgeoip-dev \
        libxml2-dev libxslt1-dev libbz2-dev libsqlite3-dev libreadline-dev \
        libjpeg-dev 
    echo "Configuring virtualenvwrapper ..."
    printf '\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' 'export PIP_REQUIRE_VIRTUALENV=true' \
        'export WORKON_HOME=/vagrant/.virtualenvs' \
        'export PROJECT_HOME=/vagrant' \
        'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python' \
        'export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv' \
        'source /usr/share/virtualenvwrapper/virtualenvwrapper.sh' >> /home/vagrant/.bashrc
    source /home/vagrant/.bashrc
SCRIPT

  config.vm.provision "shell", inline: $python

end
