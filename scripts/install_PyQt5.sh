wget -o pyqt5.tar.gz https://www.riverbankcomputing.com/static/Downloads/PyQt5/5.13.1/PyQt5_gpl-5.13.1.tar.gz
tar -xf pyqt5.tar.gz

rm -rf pyqt5.tar.gz
cd PyQt5_gpl-5

python3 configure.py

make -j1
make install