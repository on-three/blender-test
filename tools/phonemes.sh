#!/bin/bash

# phonemes.sh
# Simple script to extract estimates for spoken
# phonemes from audio files,
# results in a simple time mapping to spoken phonemes
# suitable for synching to animation.

if [ "$#" -lt 1 ]; then
	echo "USAGE: phonemes.sh <input audio file> [optional output dir]"
	exit -1
fi

INFILE=$1

OUTPUT_DIR=./tmp

if [ "$#" -gt 1 ]; then
OUTPUT_DIR=$2
else
OUTPUT_DIR=$(dirname "${INFILE}")
fi

gen_phoneme_file () {
  INFILE=$1
  OUTPUT_DIR= $2
  
  FILENAME=$(basename ${INFILE})
  
  # first convert input audio file to raw 16khx sampled pcm
  RAW_AUDIO=${OUTPUT_DIR}/${FILENAME}.raw
  SOX=sox
  SAMPLE_RATE=16000
  $SOX $INFILE -r $SAMPLE_RATE --bits 16 --encoding signed-integer --endian little $RAW_AUDIO

  # run the audio file through pocketsphinx_continuous and get raw phonemes

  SPHINX=pocketsphinx_continuous
  MODEL_PATH=./sphinx/model/en-us
  HMM_PATH=${MODEL_PATH}/en-us/
  ALLPHONE_FILE=${MODEL_PATH}/en-us-phone.lm.bin
  #ADDITIONAL_ARGS="-time yes -beam 1e-10 -pbeam 1e-10 -lw 0.5"
  ADDITIONAL_ARGS="-time yes -dither no -beam 1e-10 -pbeam 1e-10 -lw 0.5"

  OUTFILE=${OUTPUT_DIR}/${FILENAME}.phonemes.txt

  $SPHINX -infile $RAW_AUDIO -hmm $HMM_PATH -allphone $ALLPHONE_FILE $ADDITIONAL_ARGS > $OUTFILE

}

#$SPHINX -infile $RAW_AUDIO -hmm $HMM_PATH -allphone $ALLPHONE_FILE $ADDITIONAL_ARGS

# if single argument is a file, run once on single file
# if single argument is a dir, run on all .mp3 files in dir
if [ -d $INFILE ] ; then
  for i in ${INFILE}/*mp3; do
    gen_phoneme_file $i $OUTPUT_DIR
  done
else
  gen_phoneme_file $INFILE $OUTPUT_DIR
fi
 
