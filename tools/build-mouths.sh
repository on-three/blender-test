#!/bin/bash

# create a 4x4 image using various mouth images into one single
# spritemap of mouths

# layout should be the following:
#IL = 0 # same as m.b.p
#A = 1
#I = 1
#O = 2
#E = 3
#W = 4
#R = 4
#T = 5
#S = 5
#L = 6
#N = 6
#U = 7
#Q = 7
#M = 8
#B = 8
#P = 8
#F = 9
#V = 9

DIR=./img/trump

SUBIMAGE_WIDTH=`identify -format "%w" ${DIR}/trump-ww.jpg`
echo image width $SUBIMAGE_WIDTH

SUBIMAGE_HEIGHT=`identify -format "%h" ${DIR}/trump-ww.jpg`
echo image height $SUBIMAGE_HEIGHT

IMAGE_WIDTH=$(($SUBIMAGE_WIDTH * 4))
IMAGE_HEIGHT=$(($SUBIMAGE_HEIGHT * 4))

echo Going to generate mosaic image witdh: $IMAGE_WIDTH x $IMAGE_HEIGHT

IMAGE_OUT=${DIR}/trump-mouths.jpg

convert -size ${IMAGE_WIDTH}x${IMAGE_HEIGHT} xc:white $IMAGE_OUT
#composite photo_cropped.jpg result.png result.png

composite -geometry +$(($SUBIMAGE_WIDTH * 0))+$(($SUBIMAGE_HEIGHT * 0)) ${DIR}/trump-closed.jpg ${IMAGE_OUT} ${IMAGE_OUT}
composite -geometry +$(($SUBIMAGE_WIDTH * 1))+$(($SUBIMAGE_HEIGHT * 0)) ${DIR}/trump-aa.jpg ${IMAGE_OUT} ${IMAGE_OUT}
composite -geometry +$(($SUBIMAGE_WIDTH * 2))+$(($SUBIMAGE_HEIGHT * 0)) ${DIR}/trump-oo.jpg ${IMAGE_OUT} ${IMAGE_OUT}
composite -geometry +$(($SUBIMAGE_WIDTH * 3))+$(($SUBIMAGE_HEIGHT * 0)) ${DIR}/trump-ee.jpg ${IMAGE_OUT} ${IMAGE_OUT}

composite -geometry +$(($SUBIMAGE_WIDTH * 0))+$(($SUBIMAGE_HEIGHT * 1)) ${DIR}/trump-ww.jpg ${IMAGE_OUT} ${IMAGE_OUT}
composite -geometry +$(($SUBIMAGE_WIDTH * 1))+$(($SUBIMAGE_HEIGHT * 1)) ${DIR}/trump-dd.jpg ${IMAGE_OUT} ${IMAGE_OUT}
composite -geometry +$(($SUBIMAGE_WIDTH * 2))+$(($SUBIMAGE_HEIGHT * 1)) ${DIR}/trump-nn.jpg ${IMAGE_OUT} ${IMAGE_OUT}
composite -geometry +$(($SUBIMAGE_WIDTH * 3))+$(($SUBIMAGE_HEIGHT * 1)) ${DIR}/trump-normal.jpg ${IMAGE_OUT} ${IMAGE_OUT}


composite -geometry +$(($SUBIMAGE_WIDTH * 0))+$(($SUBIMAGE_HEIGHT * 2)) ${DIR}/trump-closed.jpg ${IMAGE_OUT} ${IMAGE_OUT}
composite -geometry +$(($SUBIMAGE_WIDTH * 1))+$(($SUBIMAGE_HEIGHT * 2)) ${DIR}/trump-ww.jpg ${IMAGE_OUT} ${IMAGE_OUT}
#composite -geometry +$(($SUBIMAGE_WIDTH * 2))+$(($SUBIMAGE_HEIGHT * 2)) ${DIR}/trump-ee.jpg ${IMAGE_OUT} ${IMAGE_OUT}
#composite -geometry +$(($SUBIMAGE_WIDTH * 3))+$(($SUBIMAGE_HEIGHT * 2)) ${DIR}/trump-ee.jpg ${IMAGE_OUT} ${IMAGE_OUT}



