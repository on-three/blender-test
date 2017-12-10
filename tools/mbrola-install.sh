#!/bin/sh

mkdir mbrola_tmp
cd mbrola_tmp/
wget http://tcts.fpms.ac.be/synthesis/mbrola/bin/pclinux/mbrola3.0.1h_i386.deb
wget -c http://tcts.fpms.ac.be/synthesis/mbrola/dba/us1/us1-980512.zip
wget -c http://tcts.fpms.ac.be/synthesis/mbrola/dba/us2/us2-980812.zip
wget -c http://tcts.fpms.ac.be/synthesis/mbrola/dba/us3/us3-990208.zip
wget -c http://www.festvox.org/packed/festival/latest/festvox_us1.tar.gz
wget -c http://www.festvox.org/packed/festival/latest/festvox_us2.tar.gz
wget -c http://www.festvox.org/packed/festival/latest/festvox_us3.tar.gz

#sudo dpkg -i mbrola3.0.1h_i386.deb

unzip -x us1-980512.zip
unzip -x us2-980812.zip
unzip -x us3-990208.zip
tar xvf festvox_us1.tar.gz
tar xvf festvox_us2.tar.gz
tar xvf festvox_us3.tar.gz

sudo mkdir -p /usr/share/festival/voices/english/us1_mbrola/
sudo mkdir -p /usr/share/festival/voices/english/us2_mbrola/
sudo mkdir -p /usr/share/festival/voices/english/us3_mbrola/

sudo mv us1 /usr/share/festival/voices/english/us1_mbrola/
sudo mv us2 /usr/share/festival/voices/english/us2_mbrola/
sudo mv us3 /usr/share/festival/voices/english/us3_mbrola/
sudo mv festival/lib/voices/english/us1_mbrola/* /usr/share/festival/voices/english/us1_mbrola/
sudo mv festival/lib/voices/english/us2_mbrola/* /usr/share/festival/voices/english/us2_mbrola/
sudo mv festival/lib/voices/english/us3_mbrola/* /usr/share/festival/voices/english/us3_mbrola/

cd ../
#rm -rf mbrola_tmp/
