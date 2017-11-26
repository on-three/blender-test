

SCRIPTS_DIR := scripts
OUT_DIR := out
AUDIO_DIR := audio

SCRIPT ?= script.txt
BLENDER_SCRIPT ?= test4
TARGET_EXT ?= .webm
TARGET ?= $(OUT_DIR)/$(SCRIPT)$(TARGET_EXT)
MOV_OUT ?= $(TARGET:$(TARGET_EXT)=.mov)

# tools
BLENDER ?= blender
VIDEO_PLAYER ?= mpv
FFMPEG ?= ffmpeg

# tool to view images
#DISPLAY := display
DISPLAY := chromium-browser

run: $(TARGET)

# audio dpendency file
$(AUDIO_DIR)/audio.d: $(SCRIPTS_DIR)/$(SCRIPT)
	./scripts/script.py $< -tts
	./scripts/phonemes.sh $(@D)
	touch $@

$(TARGET): $(MOV_OUT)
	$(FFMPEG) -i $< $@

$(MOV_OUT): $(SCRIPTS_DIR)/$(BLENDER_SCRIPT).py $(AUDIO_DIR)/audio.d 
	mkdir -p $(@D)
	$(BLENDER) --background --python $< $(SCRIPTS_DIR)/$(SCRIPT) $@
	
play: $(TARGET)

clean:
	rm -fr $(OUT_DIR)

#frommp3: $(MP3)
#	mkdir -p $(@D)
#	$(BLENDER) --background --python $(SCRIPTS_DIR)/$(BLENDER_SCRIPT).py $(MP3) $(OUT_DIR)/$(SCRIPT).mov
	
