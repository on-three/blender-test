# Run as: blender -b <filename> -P <this_script> -- <args>
import bpy
import sys, os
from math import pi
from mathutils import Vector

# prep for and import our local python modules
#dir = os.path.dirname(bpy.data.filepath)
dir = dir_path = os.path.dirname(os.path.realpath(__file__))
print("****" + dir)
if not dir in sys.path:
  sys.path.append(dir)
for x in sys.path:
  print(">>>" + x)

from phonemes import Phoneme
from phonemes import Tokenizer

def setRenderSettings():
  render = bpy.context.scene.render
  render.resolution_x = 1920
  render.resolution_y = 1080
  render.resolution_percentage = 100
  render.fps = 24    
  render.use_raytrace = False
  #render.use_color_management = True
  render.use_sss = False
  return

def look_at(obj_camera, point):
  loc_camera = obj_camera.matrix_world.to_translation()

  p = Vector(point)
  direction = p - loc_camera
  # point the cameras '-Z' and use its 'Y' as up
  rot_quat = direction.to_track_quat('-Z', 'Y')

  # assume we're using euler rotation
  obj_camera.rotation_euler = rot_quat.to_euler()

  #m1 = [ [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,5,1] ]
  #obj_camera.projection_matrix = m1

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

def add_background(filepath):
  img = bpy.data.images.load(filepath)
  #for area in bpy.context.screen.areas:
  #  if area.type == 'VIEW_3D':
  #    space_data = area.spaces.active
  #    bg = space_data.background_images.new()
  #    bg.image = img
  #    space_data.show_background_images = True
  #    break

  texture = bpy.data.textures.new("Texture.001", 'IMAGE')
  texture.image = img
  bpy.data.worlds['World'].active_texture = texture
  bpy.context.scene.world.texture_slots[0].use_map_horizon = True
  bpy.context.scene.world.texture_slots[0].texture_coords = 'VIEW'



def add_texture(obj, img_path, texture_name):
  # TODO: check to see if this texture is already loaded
  try:
    img = bpy.data.images.load(img_path)
    #img.alpha_mode = 'STRAIGHT'
    #img.use_alpha = True
  except:
    raise NameError("Cannot load image %s" % img_path)
  
  cTex = bpy.data.textures.new(texture_name, type = 'IMAGE')
  cTex.image = img

  aTex = bpy.data.textures.new(texture_name+"-alpha", type = 'IMAGE')
  aTex.image = img
  
  # Create new material
  mtex = bpy.data.materials.new(texture_name + '-material')
  mtex.diffuse_color = (1, 1, 1)
  mtex.transparency_method = 'Z_TRANSPARENCY'
  mtex.use_transparency = True
  mtex.alpha = 0.0
  
  slot = mtex.texture_slots.add()
  slot.texture = cTex
  slot.texture_coords = 'UV'
  #slot.use_map_color_diffuse = True 
  #slot.use_map_color_emission = True
  slot.use_map_alpha = True
  #slot.emission_color_factor = 0.5
  #slot.use_map_density = True 
  #slot.mapping = 'FLAT'

  #aslot = mtex.texture_slots.add()
  #slot.texture = aTex
  #slot.texture_coords = 'UV'
  #slot.use_map_alpha = True

  # Map cloud to alpha, reflection and normal, but not diffuse
  #mtex.add_texture(texture = cTex, texture_coordinates = 'UV', map_to = 'ALPHA')
  #cl_mtex = mat.textures[2]
  #cl_mtex.map_reflection = True
  #cl_mtex.map_normal = True

  obj.data.materials.append(mtex)
  return (mtex, cTex)


def add_billboard(img_path, n, loc=[0,0,0], scale=1):
  bpy.ops.mesh.primitive_plane_add(view_align=True,
  radius=1,
  location=loc,
  rotation=[0, 0, 0])
  #layers=selectLayer(2))
  plane = context.object
  plane.name = n
  bpy.context.scene.layers[2] = True
  #plane.uvs_rotate()
  bpy.ops.mesh.uv_texture_add()
  material_name = n + '-material'
  texture_name = n + '-texture'
  #plane_mat = bpy.data.materials.new(name=material_name)
  #plane.data.materials.append(plane_mat)
  #plane.active_material.diffuse_color = (1, 1, 1)
  #bpy.data.textures.new(texture_name, type='IMAGE')
  (mat, tex) = add_texture(plane, img_path, n + "_texture")
  # scale the billboard to match image dimensions
  sz = tex.image.size
  x = sz[0]
  y = sz[1]
  plane.scale = (x*scale, y*scale, 1)
  return plane
 


if __name__ == '__main__':
  # you can catch command line arguments this way
  filePath = sys.argv[-1]

  context = bpy.context

  # clear everything
  delete_scene_objects()

  setRenderSettings()
  
  # World settings
  world = bpy.context.scene.world
  #world.use_sky_blend = True
  #world.ambient_color = (0.0, 0, 0)
  #world.horizon_color = (0, 0, 0.2)
  #world.zenith_color = (0.04, 0, 0.04)

  # Environment lighting
  wset = world.light_settings
  wset.use_environment_light = True
  wset.use_ambient_occlusion = True
  wset.ao_blend_type = 'MULTIPLY'
  wset.ao_factor = 0.8
  wset.gather_method = 'APPROXIMATE'

  add_pepe = False
  if add_pepe:
    img = add_billboard('img/smugpepe.jpg', 'billboard3', loc=[0,0,0], scale=0.01)
 
    positions = (22,0,0),(0,0,0),(0,0,0),(-22,0,0)
    frame_num = 0
    for position in positions:
      bpy.context.scene.frame_set(frame_num)
      img.location = position
      img.keyframe_insert(data_path="location", index=-1)
      frame_num += 24
  else:
    frame_num = 24

  # Add a billboard as a background
  #add_billboard('img/background.jpg', 'background', loc=[0,0,0], size=1)


  # fix the UV coordnates of the plane
  #for face in ob.data.polygons:
  #  for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
  #    uv_coords = ob.data.uv_layers.active.data[loop_idx].uv
  #    #print("face idx: %i, vert idx: %i, uvs: %f, %f" % (face.index, vert_idx, uv_coords.x, uv_coords.y))
  #    ob.data.uv_layers.active.data[loop_index].uv = (0.5, 0.5)


  #bpy.ops.mesh.primitive_cube_add(radius=1,
  #  location=[0, 0, 5])
  #cube.name = 'Object1'
  #cube = context.object
  
  bpy.ops.object.camera_add(view_align=False,
    location=[0, 0, 30],
    rotation=[0, 0, 0])
    #rotation=[0.436, 0, pi])
  #bpy.context.object.data.type = 'ORTHO'
  #bpy.context.object.data.ortho_scale = 1920.0*2.0
  camera = context.object
  bpy.context.scene.camera = camera
  #camera.location = (0,10,20)
  look_at(camera, [0,0,0]) 
  #look_at(camera, [0.0, 0.0, 0.0]) 
  camera.name = 'Camera'


  add_background('img/background.jpg')

  #bg_file = 'img/test.jpg'
  #img = bpy.data.images.load(bg_file)
  #for area in bpy.context.screen.areas:
  #  if area.type == 'VIEW_3D':
  #    space_data = area.spaces.active
  #    bg = space_data.background_images.new()
  #    bg.image = img
  #    break

  #bpy.data.scenes['Scene'].render.filepath = bg_file
  #bpy.context.scene.camera = bpy.data.objects['Camera']

  #bpy.ops.view3d.background_image_add(filepath='img/test.jpg')

  # Render to separate file, identified by texture file
  #imageBaseName = bpy.path.basename(imagePath)
  #bpy.context.scene.render.filepath = imagePath

  render_video = True
  if render_video == True:
    for scene in bpy.data.scenes:
      scene.render.image_settings.file_format = 'H264'
      scene.render.ffmpeg.format = 'QUICKTIME'
      scene.render.image_settings.color_mode = 'RGB'
      scene.render.ffmpeg.audio_codec = 'AAC'
      scene.render.ffmpeg.audio_bitrate = 128
      scene.render.resolution_percentage = 100
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = frame_num
    #bpy.context.scene.render.filepath = 'out/' + os.path.basename(__file__) + '.mov'
    bpy.context.scene.render.filepath = filePath
    bpy.ops.render.render(animation = True, write_still = False)
  else:
    # Render still image, automatically write to output path
    bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()
