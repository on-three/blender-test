# Run as: blender -b <filename> -P <this_script> -- <args>
import bpy
import sys, os

def setRenderSettings():
  render = bpy.context.scene.render
  render.resolution_x = 720
  render.resolution_y = 576
  render.resolution_percentage = 100
  render.fps = 24    
  render.use_raytrace = False
  #render.use_color_management = True
  render.use_sss = False
  return

if __name__ == '__main__':
  # you can catch command line arguments this way
  imagePath = sys.argv[-1]

  # clear everything
  #bpy.ops.wm.read_factory_settings(use_empty=True)

  setRenderSettings()
  
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

  # World settings
  world = bpy.context.scene.world
  world.use_sky_blend = True
  world.ambient_color = (0.0, 0, 0)
  world.horizon_color = (0, 0, 0.2)
  world.zenith_color = (0.04, 0, 0.04)

  # Environment lighting
  wset = world.light_settings
  wset.use_environment_light = True
  wset.use_ambient_occlusion = True
  wset.ao_blend_type = 'MULTIPLY'
  wset.ao_factor = 0.8
  wset.gather_method = 'APPROXIMATE'

  # Render to separate file, identified by texture file
  #imageBaseName = bpy.path.basename(imagePath)
  bpy.context.scene.render.filepath = imagePath

  # Render still image, automatically write to output path
  bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()
