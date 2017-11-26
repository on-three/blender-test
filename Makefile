

SCRIPTS_DIR := scripts
OUT_DIR := out
AUDIO_DIR := audio

SCRIPT ?= script.txt
BLENDER_SCRIPT ?= test4
TARGET ?= $(OUT_DIR)/$(SCRIPT).mov

# tools
BLENDER ?= blender
VIDEO_PLAYER ?= mpv

# tool to view images
#DISPLAY := display
DISPLAY := chromium-browser

run: $(TARGET)

# audio dpendency file
$(AUDIO_DIR)/audio.d: $(SCRIPTS_DIR)/$(SCRIPT)
	./scripts/script.py $< -tts
	./scripts/phonemes.sh $(@D)
	touch $@

$(TARGET): $(SCRIPTS_DIR)/$(BLENDER_SCRIPT).py $(AUDIO_DIR)/audio.d 
	mkdir -p $(@D)
	$(BLENDER) --background --python $< $(TARGET)
	
play: $(TARGET)

clean:
	rm -fr $(OUT_DIR)
