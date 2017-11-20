#!/bin/bash

# phonemes.sh
# Simple script to extract estimates for spoken
# phonemes from audio files,
# results in a simple time mapping to spoken phonemes
# suitable for synching to animation.

if [ "$#" -ne 1 ]; then
	echo "USAGE: phonemes.sh <input audio file>"
	exit -1
fi

INFILE=$1

# first convert input audio file to raw 16khx sampled pcm
RAW_AUDIO=${INFILE}.raw
SOX=sox
SAMPLE_RATE=16000
$SOX $INFILE -r $SAMPLE_RATE $RAW_AUDIO

# run the audio file through pocketsphinx_continuous and get raw phonemes

SPHINX=pocketsphinx_continuous
MODEL_PATH=./sphinx/model/en-us
HMM_PATH=${MODEL_PATH}/en-us/
ALLPHONE_FILE=${MODEL_PATH}/en-us-phone.lm.bin
ADDITIONAL_ARGS="-time yes -beam 1e-10 -pbeam 1e-10 -lw 0.5"

OUTFILE=${INFILE}.phonemes.out.txt

$SPHINX -infile $RAW_AUDIO -hmm $HMM_PATH -allphone $ALLPHONE_FILE $ADDITIONAL_ARGS > $OUTFILE


