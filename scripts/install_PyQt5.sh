wget -O sip.tar.gz https://www.riverbankcomputing.com/static/Downloads/sip/4.19.19/sip-4.19.19.tar.gz
tar -xf sip.tar.gz
cd sip-4.19.19

python3 configure.py --sip-module=PyQt5.sip

make -j1
make install

cd ..

wget -O pyqt5.tar.gz https://www.riverbankcomputing.com/static/Downloads/PyQt5/5.13.1/PyQt5_gpl-5.13.1.tar.gz
tar -xf pyqt5.tar.gz

rm -rf pyqt5.tar.gz
cd PyQt5_gpl-5.13.1

sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile restart

python3 configure.py

make -j4
make install

sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile restart