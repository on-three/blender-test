#!/bin/bash

# diarization.sh
# Attempt to process an audio file to identify individual speakers
# Using the shout toolkit: http://shout-toolkit.sourceforge.net/index.html
# to build shout see: https://askubuntu.com/questions/757394/compiling-a-speech-recognition-toolkit-in-ubuntu-gnome

if [ "$#" -ne 1 ]; then
	echo "USAGE: diarization.sh <input audio file>"
	exit -1
fi

INFILE=$1

gen_diarization_file () {
  INFILE=$1

#see: https://stackoverflow.com/questions/8284943/identifying-segments-when-a-person-is-speaking
# for shout_segment examples
# ffmpeg -i [INPUT_FILE] -vn -acodec pcm_s16le -ar 16000 -ac 1 -f s16le [RAW_FILE]
# shout_segment -a [RAW_FILE] -ams [SHOUT_SAD_MODEL] -mo [SAD_OUTPUT] 
# shout_cluster -a [RAW_FILE] -mo [DIARIZATION_OUTPUT] -mi [SAD_OUTPUT]

# first convert input audio file to raw 16khx sampled pcm
  RAW_AUDIO=${INFILE}.raw
  SOX=sox
  SAMPLE_RATE=16000
  $SOX $INFILE -r $SAMPLE_RATE --bits 16 --encoding signed-integer --endian little $RAW_AUDIO


  # first convert input audio file to raw 16khx sampled pcm
  #RAW_AUDIO=${INFILE}.raw
  #FFMPEG=ffmpeg
  #SAMPLE_RATE=16000
  
  #ffmpeg -y -i $INFILE -vn -acodec pcm_s16le -ar 16000 -ac 1 -f s16le $RAW_AUDIO
  # run the audio file through shout

  SHOUT_SEGMENT=shout_segment
  SHOUT_CLUSTER=shout_cluster
  MODEL_PATH=${HOME}/local/shout
  SHOUT_SAD_MODEL=${MODEL_PATH}/shout.sad
  #ADDITIONAL_ARGS="-time yes -beam 1e-10 -pbeam 1e-10 -lw 0.5"
  #ADDITIONAL_ARGS="-time yes -dither no -beam 1e-10 -pbeam 1e-10 -lw 0.5"
  
  SEGMENTED_AUDIO=${INFILE}.segmentation.txt

  echo "running shout_segment on input raw audio file ${RAW_AUDIO}"
  shout_segment -a $RAW_AUDIO -ams $SHOUT_SAD_MODEL -mo $SEGMENTED_AUDIO


  #$SPHINX -infile $RAW_AUDIO -hmm $HMM_PATH -allphone $ALLPHONE_FILE $ADDITIONAL_ARGS > $OUTFILE

}

#$SPHINX -infile $RAW_AUDIO -hmm $HMM_PATH -allphone $ALLPHONE_FILE $ADDITIONAL_ARGS

# if single argument is a file, run once on single file
# if single argument is a dir, run on all .mp3 files in dir
if [ -d $INFILE ] ; then
  for i in ${INFILE}/*mp3; do
    gen_diarization_file $i
  done
else
  gen_diarization_file $INFILE
fi

