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

def selectLayer(layernum):
  bools = []
  for i in range(20):
    if layernum == i:
      bools.append(True)
    else:
      bools.append(False)
  return tuple(bools) #does a typecast from list to tuple

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

def add_background(filepath):
  img = bpy.data.images.load(filepath)
  for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
      space_data = area.spaces.active
      bg = space_data.background_images.new()
      bg.image = img
      space_data.show_background_images = True
      break

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


def add_billboard(img_path, n, loc=[0,0,0], size=1):
  bpy.ops.mesh.primitive_plane_add(view_align=True,
  radius=size,
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
  add_texture(plane, img_path, n + "_texture")
 


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

  # add a material to text
  text_mat = bpy.data.materials.new(name="TextMaterial")
  text_obj.data.materials.append(text_mat)
  text_obj.active_material.diffuse_color = (1, 1, 0)

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

  add_billboard('img/elsa.png', 'billboard1', loc=[-4,4,0], size=3)
  add_billboard('img/spiderman.png', 'billboard2', loc=[4,4,0], size=3)
 
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
    location=[0, 0, 20],
    rotation=[0, 0, 0])
    #rotation=[0.436, 0, pi])
  camera = context.object
  bpy.context.scene.camera = camera
  #camera.location = (0,10,20)
  look_at(camera, text_obj.matrix_world.to_translation()) 
  camera.name = 'Camera'

  add_background('img/test.jpg')

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
  bpy.context.scene.render.filepath = imagePath

  # Render still image, automatically write to output path
  bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()
