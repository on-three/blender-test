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

def add_texture(obj, imgName):
  # Image texture
  #imgPath = '/home/thomas/picture.jpg'
  #imgPath = imgName
  #img = bpy.data.add_image(imgPath)
  #imtex = bpy.data.textures.new('ImageTex')
  #imtex.type = 'IMAGE' 
  #imtex = imtex.recast_type()
  #imtex.image = img
  try:
    img = bpy.data.images.load(imgName)
  except:
    raise NameError("Cannot load image %s" % realpath)

  cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
  cTex.image = img

  # Marble texture
  #mbtex = bpy.data.textures.new('MarbleTex')
  #mbtex.type = 'MARBLE' 
  #mbtex = mbtex.recast_type()
  #mbtex.noise_depth = 1
  #mbtex.noise_size = 1.6
  #mbtex.noisebasis2 = 'SIN'
  #mbtex.turbulence = 5

  # Cloud texture
  #cltex = bpy.data.textures.new('CloudsTex')
  #cltex.type = 'CLOUDS'
  # Cloud texture by default, don't need to recast
  #cltex.noise_basis = 'BLENDER_ORIGINAL'
  #cltex.noise_size = 1.05
  #cltex.noise_type = 'SOFT_NOISE'

  # Create new material
  mtex = bpy.data.materials.new('TexMat')
  #mat.alpha = 0
  #mtex.texture = cTex
  slot = mtex.texture_slots.add()
  slot.texture = cTex
  slot.texture_coords = 'UV'
  slot.use_map_color_diffuse = True 
  slot.use_map_color_emission = True 
  slot.emission_color_factor = 0.5
  slot.use_map_density = True 
  slot.mapping = 'FLAT'

  # Map image to color, this is the default
  #mat.add_texture(texture = imtex, texture_coordinates = 'UV')
  #im_mtex = mat.textures[0]

  # Map marble to specularity
  #mat.add_texture(texture = mbtex, texture_coordinates = 'UV', map_to = 'SPECULARITY')
  #mb_mtex = mat.textures[1]

  # Map cloud to alpha, reflection and normal, but not diffuse
  #mat.add_texture(texture = cltex, texture_coordinates = 'UV', map_to = 'ALPHA')
  #cl_mtex = mat.textures[2]
  #cl_mtex.map_reflection = True
  #cl_mtex.map_normal = True

  # Create new material
  #mat2 = bpy.data.materials.new('Blue')
  #mat2.diffuse_color = (0.0, 0.0, 1.0)
  #mat2.specular_color = (1.0, 1.0, 0.0)

  # Pick active object, remove its old material (assume exactly one old material).
  #ob = bpy.context.object
  #bpy.ops.object.material_slot_remove()

  # Add the two materials to mesh
  #me = ob.data
  #me.add_material(mat)
  #me.add_material(mat2)
  #obj.add_material(mat)
  obj.data.materials.append(mtex)


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

  bpy.ops.mesh.primitive_plane_add(view_align=True,
    location=[0, 0, -2],
    rotation=[0, 0, 0],
    layers=selectLayer(2))
  plane = context.object
  plane.name = 'Plane1'
  bpy.context.scene.layers[2] = True
  #plane_mat = bpy.data.materials.new(name="PlaneMaterial")
  #plane.data.materials.append(plane_mat)
  #plane.active_material.diffuse_color = (1, 1, 1)
  #bpy.data.textures.new("PlaneTexture", type='IMAGE')
  add_texture(plane, "img/test.jpg")
  
  
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

  # Render to separate file, identified by texture file
  #imageBaseName = bpy.path.basename(imagePath)
  bpy.context.scene.render.filepath = imagePath

  # Render still image, automatically write to output path
  bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()
