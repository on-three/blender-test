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

# some simple utilities for blender
from blender_utils import set_render_settings
from blender_utils import delete_scene_objects
from blender_utils import get_object_by_name
from blender_utils import look_at
from blender_utils import add_background
from blender_utils import add_billboard


animation_controller = AnimationController()

def set_mouth_img(obj, _pos):
  # position 0 mps to silence (SIL) so we can hide the "mouth"
  #if pos == 0:
  #  obj.hide = True
  #  return

  #obj.hide = False

  # phonemee sounds are one based, but indexes into image are zro based
  #pos = _pos -1
  pos = _pos
  
  # U,V coordinates are reversed in Y direction
  # and pos 0 serves as both "A" and "SIL"
  x1 = (pos % 4) * 0.25
  x2 = x1 + 0.25
  y2 = 1.0 - int(pos/4) * 0.25
  y1 = y2 - 0.25
  
  obj.data.uv_layers.active.data[0].uv = (x1, y1)
  obj.data.uv_layers.active.data[1].uv = (x2, y1)
  obj.data.uv_layers.active.data[2].uv = (x2, y2)
  obj.data.uv_layers.active.data[3].uv = (x1, y2)

  for face in obj.data.polygons:
    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
      uv_coords = obj.data.uv_layers.active.data[loop_idx].uv
      print("face idx: %i, vert idx: %i, uvs: %f, %f" % (face.index, vert_idx, uv_coords.x, uv_coords.y))
      #ob.data.uv_layers.active.data[loop_index].uv = (0.5, 0.5)

def on_animation_frame(frame, s):
  obj = get_object_by_name('mouth')
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
   

if __name__ == '__main__':
  global animation_controller

  # you can catch command line arguments this way
  # first arg is the input script file path (txt)
  # 2nd arg is the output .mov file path
  # TODO: proper arg handling
  script_filepath = sys.argv[-2]
  out_filepath = sys.argv[-1]

  context = bpy.context
  scene = bpy.context.scene
  if not scene.sequence_editor:
    scene.sequence_editor_create()

  # clear everything
  delete_scene_objects()

  set_render_settings()

  # World settings
  world = bpy.context.scene.world
  
  # Environment lighting
  wset = world.light_settings
  wset.use_environment_light = True
  wset.use_ambient_occlusion = True
  wset.ao_blend_type = 'MULTIPLY'
  wset.ao_factor = 0.8
  wset.gather_method = 'APPROXIMATE'

  end_frame = 0
  
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
    if line._audio_file:
      audio_file = line._audio_file
    phoneme_file = audio_file + '.phonemes.out.txt'
    if line._phoneme_file:
      phoneme_file = line._phoneme_file
    animation_controller.add_utterance(line._speaker, end_frame, phoneme_file)
    soundstrip = scene.sequence_editor.sequences.new_sound(audio_file, audio_file, 3, end_frame)
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

  img = add_billboard('img/anime-mouths.png', 'mouth', loc=[1.5,-5.5,0], scale=0.0015)
 

  # Add a billboard as a background
  add_billboard('img/anime-girl-head.png', 'background', loc=[0,0,0], scale=0.004)
  
  #bpy.ops.view3d.background_image_add(filepath='img/classroom.jpg')
  add_billboard('img/classroom.jpg', 'background', loc=[0,0,0], scale=0.015)
  
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
    bpy.context.scene.render.filepath = out_filepath
    bpy.ops.render.render(animation = True, write_still = False)
  else:
    # Render still image, automatically write to output path
    bpy.context.scene.render.filepath = out_filepath + '.png'
    bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()
