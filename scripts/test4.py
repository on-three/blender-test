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
from phonemes import AnimationController
from script import Script
from script import Line

animation_controller = AnimationController()

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

def set_mouth_img(obj, _pos):
  # position 0 mps to silence (SIL) so we can hide the "mouth"
  #if pos == 0:
  #  obj.hide = True
  #  return

  #obj.hide = False

  # phonemee sounds are one based, but indexes into image are zro based
  pos = _pos -1

  
  # U,V coordinates are reversed in Y direction
  # and pos 0 serves as both "A" and "SIL"
  x1 = (pos % 3) * 0.333
  x2 = x1 + 0.333
  y2 = 1.0 - int(pos/3) * 0.333
  y1 = y2 - 0.333
  
  obj.data.uv_layers.active.data[0].uv = (x1, y1)
  obj.data.uv_layers.active.data[1].uv = (x2, y1)
  obj.data.uv_layers.active.data[2].uv = (x2, y2)
  obj.data.uv_layers.active.data[3].uv = (x1, y2)

  for face in obj.data.polygons:
    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
      uv_coords = obj.data.uv_layers.active.data[loop_idx].uv
      print("face idx: %i, vert idx: %i, uvs: %f, %f" % (face.index, vert_idx, uv_coords.x, uv_coords.y))
      #ob.data.uv_layers.active.data[loop_index].uv = (0.5, 0.5)

def returnObjectByName (passedName= ""):
  r = None
  obs = bpy.data.objects
  for ob in obs:
    if ob.name == passedName:
      r = ob
      return r
  return r

def on_animation_frame(frame, s):
  obj = returnObjectByName('mouth')
  set_mouth_img(obj, s.sound())
  #set_mouth_img(obj, frame % 9)
 
def update_phoneme(scene):
  global animation_controller
  #animation_controller.set_on_frame_handler(on_animation_frame)
  animation_controller._on_frame_handler = on_animation_frame
  scene = bpy.data.scenes['Scene']
  frame = scene.frame_current
  animation_controller.update(frame)
  #obj = returnObjectByName('mouth')
  #set_mouth_img(obj, frame % 9)
   

#animation_controller.set_on_frame_handler = on_animation_frame

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
  #    bre5k
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
  global animation_controller

  # you can catch command line arguments this way
  # arg is the input file (either a script to be parsed or a raw mp3 file)
  script_filepath = sys.argv[-2]
  # arg is the output file to generate (.mov)
  filePath = sys.argv[-1]

  context = bpy.context
  scene = bpy.context.scene
  if not scene.sequence_editor:
    scene.sequence_editor_create()

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

  end_frame = 0
  
  if script_filepath.endswith('txt'):

    # load a script passed as argument
    print("opening file: " + script_filepath)
    script = Script(script_filepath)

    # TODO: add a character model for each speaker in script

    # add audio for all lines in script
    #for line in script:
    for i in range(len(script._lines)):
      print("line: " + str(i) + " end_frame: " + str(end_frame))
      line = script._lines[i]
      audio_file = './audio/' + str(line._index) + '.' + line._speaker + '.mp3'
      phoneme_file = audio_file + '.phonemes.out.txt'
      animation_controller.add_utterance(line._speaker, end_frame, phoneme_file)
      soundstrip = scene.sequence_editor.sequences.new_sound(audio_file, audio_file, 3, end_frame)
      end_frame = soundstrip.frame_final_end #frame_duration

  else:
    # assume single input mp3 file for now
 
    phoneme_file = script_filepath + '.phonemes.out.txt'
    animation_controller.add_utterance("MP3", 0, phoneme_file)
    soundstrip = scene.sequence_editor.sequences.new_sound("1", script_filepath, 3, 1)
    end_frame = soundstrip.frame_final_end #frame_duration

  filepath = "models/person.blend"

  # run a handler on each frame
  bpy.app.handlers.frame_change_pre.append(update_phoneme)

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

  img = add_billboard('img/mouth_front.jpg', 'mouth', loc=[0,0,0], scale=0.005)
 

  # Add a billboard as a background
  #add_billboard('img/background.jpg', 'background', loc=[0,0,0], size=1)
  
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
    bpy.context.scene.frame_end = end_frame #frame_num
    #bpy.context.scene.render.filepath = 'out/' + os.path.basename(__file__) + '.mov'
    bpy.context.scene.render.filepath = filePath
    bpy.ops.render.render(animation = True, write_still = False)
  else:
    # Render still image, automatically write to output path
    bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()
