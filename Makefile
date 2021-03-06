
TMP_ROOT := tmp
SCRIPTS_DIR := scripts
TOOL_DIR := tools
PYTHON_DIR := python
OUT_DIR := out
AUDIO_DIR := audio

SCRIPT ?= test
SCRIPT_FILE ?=  $(SCRIPTS_DIR)/$(SCRIPT).txt
BLENDER_SCRIPT ?= $(PYTHON_DIR)/generate_video.py
TARGET_EXT ?= .webm
TARGET ?= $(OUT_DIR)/$(SCRIPT)$(TARGET_EXT)
MOV_OUT ?= $(TARGET:$(TARGET_EXT)=.mov)
SUBS_FILE = $(MOV_OUT).srt

TMP_DIR := $(TMP_ROOT)/$(SCRIPT)

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

# this sucks but i don't have anything better yet
ifeq ($(SCRIPT), el.grande.padre.1)
SCRIPT_ARGS += --blendfile ./models/dbs.blend
endif
ifeq ($(SCRIPT), trump)
SCRIPT_ARGS += --blendfile ./models/trump.blend
endif

# tools
BLENDER ?= blender
VIDEO_PLAYER ?= mpv
FFMPEG ?= ffmpeg

# tool to view images
#DISPLAY := display
DISPLAY := chromium-browser

# audio dpendency file
#$(AUDIO_DIR)/audio.d: $(SCRIPTS_DIR)/$(SCRIPT)
#	./scripts/script.py $< -tts
#	./scripts/phonemes.sh $(@D)
#	touch $@

$(TARGET): $(MOV_OUT) $(SUBS_FILE)
	# we hardcode the subs file onto the webm (but not MOV)
	$(FFMPEG) -i $(MOV_OUT) -vf subtitles=$(SUBS_FILE) $@

$(SUBS_FILE):
	# if our subs file wasn't generated during movie rendering this creates an empty default
	echo "1" > $(SUBS_FILE)
	echo "00:00:00,000 --> 00:00:01,00" >> $(SUBS_FILE)
	echo "" >> $(SUBS_FILE)

$(MOV_OUT): $(BLENDER_SCRIPT) $(TMP_DIR)
	mkdir -p $(@D)
	./$(PYTHON_DIR)/script.py $(SCRIPT_FILE) --tts --phonemes --posts --videos -o $(TMP_DIR)
	$(BLENDER) --background --python $< '$(SCRIPT_FILE) --assetdir $(TMP_DIR) --out $@ $(SCRIPT_ARGS)'
	
play: $(TARGET)

clean:
	rm -fr $(OUT_DIR)
	rm -fr $(TMP_ROOT)

$(TMP_DIR):
	mkdir -p $@

#frommp3: $(MP3)
#	mkdir -p $(@D)
#	$(BLENDER) --background --python $(SCRIPTS_DIR)/$(BLENDER_SCRIPT).py $(MP3) $(OUT_DIR)/$(SCRIPT).mov

# infer an unknown rule as a possible scrptfile
%::
	$(MAKE) SCRIPT=$@


