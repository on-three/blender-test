#!/bin/bash

POST_URL=http://boards.4chan.org/tv/thread/91304338#p91304338

# get the post image and text
POST_NUM=91304338
POST_IMG=${POST_NUM}.png
POST_TXT=${POST_NUM}.txt
POST_AUDIO=${POST_NUM}.mp3
POST_VIDEO=${POST_NUM}.mp4

# generate TTS audio
#gtts-cli -o $POST_AUDIO -f $POST_AUDIO
gtts-cli -f ${POST_TXT} -o ${POST_AUDIO}

AUDIO_LENGTH=`ffmpeg -i ${POST_AUDIO} 2>&1 |grep -oP "[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}"`
echo Generated TTS audio file length: $AUDIO_LENGTH

echo Generating video from image $POST_IMG


ffmpeg -y -loop 1 -i $POST_IMG -i $POST_AUDIO -c:a aac -ab 112k -c:v libx264 -shortest -strict -2 $POST_VIDEO

