

SCRIPTS_DIR := scripts
OUT_DIR := out

SCRIPT ?= $(SCRIPTS_DIR)/test.py

BLENDER := blender

# tool to view images
#DISPLAY := display
DISPLAY := chromium-browser

IMG ?= $(OUT_DIR)/test.png

run: $(IMG)

$(IMG): $(SCRIPT)
	mkdir -p $(@D)
	$(BLENDER) --background --python $< $(IMG)

view: $(IMG)
	$(DISPLAY) $<

clean:
	rm -fr $(OUT_DIR)
