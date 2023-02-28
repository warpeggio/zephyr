# -*- mode: ruby -*-
# vi: set ft=ruby :
# See https://docs.vagrantup.com
#
# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version
Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu-focal'
  config.vm.box_url = 'https://cloud-images.ubuntu.com/focal/20230215/focal-server-cloudimg-amd64-vagrant.box'
  config.vm.network "forwarded_port", guest: 80,    host: 8888  # web
  config.vm.network "forwarded_port", guest: 5000,  host: 5000  # api
  config.ssh.forward_agent = true
  config.vm.hostname = "zephyr-vagrant"
  config.vm.network :private_network,
  ip: "172.27.2.2",
  netmask: "255.255.255.0"
  config.vbguest.auto_update = false
  config.vm.provider "virtualbox" do |vb|
    # More memory or RAM can be specified in the user's ENV
    vb.memory = ENV['VAGRANT_ALLOWED_RAM'] || "2048"
    vb.cpus = ENV['VAGRANT_ALLOWED_CPU'] || "2"
    # Disable writing a guest log to the host disk, we don't care
    vb.customize [ "modifyvm", :id, "--uartmode1", "file /tmp/bogus" ]
    vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
    vb.customize [ "modifyvm", :id, "--uart1", "0x3F8", "4"]
    vb.customize [ "modifyvm", :id, "--uartmode1", "file", File::NULL]
  end
  config.ssh.insert_key = true
  config.vm.provision :shell, :inline => "echo 'Waiting for on-boot apt tasks to finish...'"
  config.vm.provision :shell, :inline => "systemd-run --property='After=apt-daily.service apt-daily-upgrade.service' --wait /bin/true"
end
