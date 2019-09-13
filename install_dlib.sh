python3 -m pip install wheel

sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile restart

git clone https://github.com/davisking/dlib.git
cd dlib
python3 setup.py install --yes USE_NEON_INSTRUCTIONS

sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile restart
