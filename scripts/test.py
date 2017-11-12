# Run as: blender -b <filename> -P <this_script> -- <args>
import bpy
import sys, os
from math import pi

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

def look_at(obj_camera, point):
  loc_camera = obj_camera.matrix_world.to_translation()

  direction = point - loc_camera
  # point the cameras '-Z' and use its 'Y' as up
  rot_quat = direction.to_track_quat('-Z', 'Y')

  # assume we're using euler rotation
  obj_camera.rotation_euler = rot_quat.to_euler()

def delete_scene_objects(scene=None):
  """Delete a scene and all its objects."""
  #
  # Sort out the scene object.
  if scene is None:
    # Not specified: it's the current scene.
    scene = bpy.context.screen.scene
  else:
    if isinstance(scene, str):
      # Specified by name: get the scene object.
      scene = bpy.data.scenes[scene]
    # Otherwise, assume it's a scene object already.
    #
  # Remove objects.
  for object_ in scene.objects:
    scene.objects.unlink(object_)
    #object.user_clear()
    bpy.data.objects.remove(object_)
  #
  # Remove scene.
  #bpy.data.scenes.remove(scene)



if __name__ == '__main__':
  # you can catch command line arguments this way
  imagePath = sys.argv[-1]

  context = bpy.context

  # clear everything
  delete_scene_objects()

  setRenderSettings()
  
  bpy.ops.object.text_add(location=(0,0,0))
  text_obj = bpy.context.object
  tcu = text_obj.data

  #print(ob, tcu)

  # TextCurve attributes
  tcu.body = "Hello, world"
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

  #bpy.ops.mesh.primitive_circle_add(radius=6,
  #  fill_type='TRIFAN',
  #  location=[0, 0, 0])
  #plane = context.object
  #plane.name = 'Plane1'
  
  #bpy.ops.mesh.primitive_cube_add(radius=1,
  #  location=[0, 0, 5])
  #cube.name = 'Object1'
  #cube = context.object
  
  bpy.ops.object.camera_add(view_align=False,
    location=[0, 0, 20],
    rotation=[0, 0, 0])
    #rotation=[0.436, 0, pi])
  camera = context.object
  bpy.context.scene.camera = camera
  #camera.location = (0,10,20)
  look_at(camera, text_obj.matrix_world.to_translation()) 

  camera.name = 'Object2'

  # Render to separate file, identified by texture file
  #imageBaseName = bpy.path.basename(imagePath)
  bpy.context.scene.render.filepath = imagePath

  # Render still image, automatically write to output path
  bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()
