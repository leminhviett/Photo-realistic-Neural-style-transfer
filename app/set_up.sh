#!/bin/bash

# Image and model names
MODEL_PATH=ade20k-resnet50dilated-ppm_deepsup
ENCODER=$MODEL_PATH/encoder_epoch_20.pth
DECODER=$MODEL_PATH/decoder_epoch_20.pth
LOCAL_PATH=segment_model/ade20k-resnet50dilated-ppm_deepsup


# Download model weights and image
if [ ! -e $LOCAL_PATH ]; then
  mkdir $LOCAL_PATH
fi
if [ ! -e $ENCODER ]; then
  wget -P $LOCAL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$ENCODER
fi
if [ ! -e $DECODER ]; then
  wget -P $LOCAL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$DECODER
fi

#set up folders
mkdir 'upload'
mkdir 'segment_res'
mkdir 'static'

mkdir 'upload/content'
mkdir 'upload/style'

mkdir 'segment_res/content'
mkdir 'segment_res/style'