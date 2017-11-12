# Run as: blender -b <filename> -P <this_script> -- <args>
import bpy, sys, os

# you can catch command line arguments this way
imagePath = sys.argv[-1]

#bpy.ops.object.text_add()
#obj = bpy.context.object
#tcu = obj.data

#print(ob, tcu)

# TextCurve attributes
#tcu.body = "Hello, world"
#tcu.font = bpy.data.fonts[0]
#print("Font", tcu.font)
#tcu.offset_x = 0.1
#tcu.offset_y = -0.25
#tcu.shear = 0.5
#tcu.spacing = 2
#tcu.ul_height = 0.7
#tcu.ul_position = -1
#tcu.word_spacing = 4

# Inherited Curve attributes
#tcu.extrude = 0.2
#tcu.back = True

# Render to separate file, identified by texture file
#imageBaseName = bpy.path.basename(imagePath)
bpy.context.scene.render.filepath = imagePath

# Render still image, automatically write to output path
bpy.ops.render.render(write_still=True)

bpy.ops.wm.quit_blender()
