#!/bin/bash

mkdir cmu_tmp
cd cmu_tmp/
wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_awb_arctic-0.90-release.tar.bz2
wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_bdl_arctic-0.95-release.tar.bz2
wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_clb_arctic-0.95-release.tar.bz2
wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_jmk_arctic-0.95-release.tar.bz2
wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_rms_arctic-0.95-release.tar.bz2
wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_slt_arctic-0.95-release.tar.bz2


for t in `ls cmu_*` ; do tar xf $t ; done
#rm *.bz2

sudo mkdir -p /usr/share/festival/voices/english/
sudo mv * /usr/share/festival/voices/english/

for d in `ls /usr/share/festival/voices/english` ; do
  if [[ "$d" =~ "cmu_us_" ]] ; then
    sudo mv "/usr/share/festival/voices/english/${d}" "/usr/share/festival/voices/english/${d}_clunits" 
  fi
done

cd ../
#rm -rf cmu_tmp/


