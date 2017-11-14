

SCRIPTS_DIR := scripts
OUT_DIR := out

SCRIPT ?= test
TARGET ?= $(OUT_DIR)/$(SCRIPT).mov

# tools
BLENDER ?= blender
VIDEO_PLAYER ?= mpv

# tool to view images
#DISPLAY := display
DISPLAY := chromium-browser

run: $(TARGET)

$(TARGET): $(SCRIPTS_DIR)/$(SCRIPT).py
	mkdir -p $(@D)
	$(BLENDER) --background --python $< $(TARGET)
	
play: $(TARGET)

clean:
	rm -fr $(OUT_DIR)
