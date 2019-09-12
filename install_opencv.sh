#Run this script not from project folder
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.1.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.1.zip
unzip opencv_contrib.zip

rm -rf opencv.zip
rm -rf opencv_contrib.zip

cd opencv-4.1.1
mkdir build
cd build

sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile restart

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.1.1/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D CMAKE_SHARED_LINKER_FLAGS='-latomic' \
    -D BUILD_EXAMPLES=OFF ..

make -j1

sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile restart