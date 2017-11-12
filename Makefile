

SCRIPTS_DIR := scripts
OUT_DIR := out

SCRIPT ?= $(SCRIPTS_DIR)/test.py

BLENDER := blender

IMG ?= $(OUT_DIR)/test.jpg

run: $(IMG)

$(IMG): $(SCRIPT)
	mkdir -p $(@D)
	$(BLENDER) --background --python $< $(IMG)

clean:
	rm -fr $(OUT_DIR)
