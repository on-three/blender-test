

SCRIPTS_DIR := scripts
OUT_DIR := out

SCRIPT ?= $(SCRIPTS_DIR)/test.py

BLENDER := blender

# tool to view images
DISPLAY := display

IMG ?= $(OUT_DIR)/test.jpg

run: $(IMG)

$(IMG): $(SCRIPT)
	mkdir -p $(@D)
	$(BLENDER) --background --python $< $(IMG)

show: $(IMG)
	$(DISPLAY) $<

clean:
	rm -fr $(OUT_DIR)
