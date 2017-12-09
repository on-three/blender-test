

SCRIPTS_DIR := scripts
OUT_DIR := out
AUDIO_DIR := audio
TMP_DIR := tmp

SCRIPT ?= test.txt
BLENDER_SCRIPT ?= generate_video
TARGET_EXT ?= .webm
TARGET ?= $(OUT_DIR)/$(SCRIPT)$(TARGET_EXT)
MOV_OUT ?= $(TARGET:$(TARGET_EXT)=.mov)

# some additional args that are passed to blender via
# the SCRIPT_ARGS variable
SCRIPT_ARGS ?=
ifeq ($(SNAPSHOT), 1)
  SCRIPT_ARGS += --test
endif
ifeq ($(NORENDER), 1)
  SCRIPT_ARGS += --norender
  SCRIPT_ARGS += -s $(OUT_DIR)/$(SCRIPT).blend
endif



# tools
BLENDER ?= blender
VIDEO_PLAYER ?= mpv
FFMPEG ?= ffmpeg

# tool to view images
#DISPLAY := display
DISPLAY := chromium-browser

run: $(TARGET)

# audio dpendency file
#$(AUDIO_DIR)/audio.d: $(SCRIPTS_DIR)/$(SCRIPT)
#	./scripts/script.py $< -tts
#	./scripts/phonemes.sh $(@D)
#	touch $@

$(TARGET): $(MOV_OUT)
	$(FFMPEG) -y -i $< $@

$(MOV_OUT): $(SCRIPTS_DIR)/$(BLENDER_SCRIPT).py $(TMP_DIR)
	mkdir -p $(@D)
	./scripts/script.py $(SCRIPTS_DIR)/$(SCRIPT) --tts --phonemes --posts -o $(TMP_DIR)
	$(BLENDER) --background --python $< '$(SCRIPTS_DIR)/$(SCRIPT) --out $@ $(SCRIPT_ARGS)'
	
play: $(TARGET)

clean:
	rm -fr $(OUT_DIR)
	rm -fr $(TMP_DIR)

$(TMP_DIR):
	mkdir -p $@

#frommp3: $(MP3)
#	mkdir -p $(@D)
#	$(BLENDER) --background --python $(SCRIPTS_DIR)/$(BLENDER_SCRIPT).py $(MP3) $(OUT_DIR)/$(SCRIPT).mov
	
