#!/bin/bash


mkdir hts_tmp
cd hts_tmp/
wget -c http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_awb_arctic_hts-2.1.tar.bz2
wget -c http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_bdl_arctic_hts-2.1.tar.bz2
wget -c http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_clb_arctic_hts-2.1.tar.bz2
wget -c http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_rms_arctic_hts-2.1.tar.bz2
wget -c http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_slt_arctic_hts-2.1.tar.bz2
wget -c http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_jmk_arctic_hts-2.1.tar.bz2
wget -c http://hts.sp.nitech.ac.jp/archives/1.1.1/cmu_us_kal_com_hts.tar.gz
wget -c http://hts.sp.nitech.ac.jp/archives/1.1.1/cstr_us_ked_timit_hts.tar.gz


for t in `ls` ; do tar xvf $t ; done

sudo mkdir -p /usr/share/festival/voices/us
sudo mv lib/voices/us/* /usr/share/festival/voices/us/
sudo mv lib/hts.scm /usr/share/festival/hts.scm

cd ../
#rm -rf hts_tmp/
