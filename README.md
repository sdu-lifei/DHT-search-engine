# DHT-search-engine

tx 申请了一个试用的主机, 安装了python.

部署了DHT爬虫, 能够获取infohash.

想要获取种子的时候, 需要用到 libtorrent.

于是又下载安装.

这里面坑多得很...

1. centos系统中没有一键安装的操作, 不像Ubuntu中的apt-get/Macos中的brew.
2. google找到的办法是 install & binding .
yum install -y boost boost-devel
yum install -y make gcc gcc-c++ kernel-devel python-devel
wget https://github.com/arvidn/libtorrent/releases/download/libtorrent-1_1_4/libtorrent-rasterbar-1.1.4.tar.gz
tar zxvf libtorrent-rasterbar-1.1.4.tar.gz
cd libtorrent-rasterbar-1.1.4
./configure --disable-debug --with-boost-libdir=/usr/lib64 --disable-encryption --enable-python-binding
make && make install
export LD_LIBRARY_PATH=/usr/local/lib/
cd bindings/python
python setup.py build
python setup.py install
3. make的时候报错: g++: 内部错误：Killed (程序 cc1plus). 网友反馈是内存不足.
需要增加交换空间, 解决:
sudo dd if=/dev/zero of=/home/swap bs=64M count=16
sudo mkswap /home/swap
sudo swapon /home/swap

4. 果然后面就成功了.
