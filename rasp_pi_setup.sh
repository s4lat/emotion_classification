sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y build-essential cmake pkg-config
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y libatlas3-base
sudo apt-get install -y libhdf5-dev libhdf5-serial-dev
sudo apt-get install -y libqtgui4 libqtgui4-test
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libcanberra-gtk*
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python2.7-dev python3-dev



sudo apt-get remove python3-pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py



sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart

python3 -m pip install dlib

sudo sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart
