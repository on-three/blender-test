#!/bin/bash


if [ "$#" -ne 1 ]; then
	echo "USAGE: $0  <url to 4chin post>"
	exit -1
fi

#POST_URL=http://boards.4chan.org/tv/thread/91304338#p91304338
POST_URL=$1

# get the post number off the url for bash regex
POST_NUM=91304338
regex="#p([0-9]+)$"
if [[ $POST_URL =~ $regex ]]
then
  POST_NUM=${BASH_REMATCH[1]}
else
  echo "Script currently only supports single #pXXX url style links off 4chin."
  exit -1
fi

echo Generating webm off post $POST_NUM on page at $POST_URL

#use /tmp/ as a working dir
WORKING_DIR=/tmp

POST_IMG=${WORKING_DIR}/${POST_NUM}.png
POST_TXT=${WORKING_DIR}/${POST_NUM}.txt
POST_AUDIO=${WORKING_DIR}/${POST_NUM}.mp3
POST_VIDEO=${WORKING_DIR}/${POST_NUM}.mp4
POST_WEBM=${POST_NUM}.webm

# generate an image and textfile off the post
phantomjs scripts/get_post.js "$POST_URL" "$WORKING_DIR"

# fail if we don't have the resultant .png and .txt files
if [ ! -f $POST_IMG ]; then
  echo "Post file does not exist. FAILING"
  exit -1
fi
if [ ! -f $POST_TXT ]; then
  echo "Post text does not exist. FAILING"
  exit -1
fi

# generate TTS audio
gtts-cli -f ${POST_TXT} -o ${POST_AUDIO}

AUDIO_LENGTH=`ffmpeg -i ${POST_AUDIO} 2>&1 |grep -oP "[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}"`
echo Generated TTS audio file length: $AUDIO_LENGTH

echo Generating video from image $POST_IMG


ffmpeg -y -loop 1 -i $POST_IMG -i $POST_AUDIO -c:a aac -ab 112k -c:v libx264 -shortest -strict -2 $POST_VIDEO

# TODO generate directly to webm
ffmpeg -i $POST_VIDEO $POST_WEBM
