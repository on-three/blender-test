# -*- coding: utf-8 -*-
# Run as: blender -b <filename> -P <this_script> -- <args>
"""
MODULE: generate_video
AUTHOR: on-three
EMAIL: on.three.email@gmail.com
DESC: Use blender to generate a video off a very simple script file
"""
import bpy
import sys, os
from math import pi
from mathutils import Vector
import argparse

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
from animation import AnimationController
from script import Script
from script import Line

# some simple utilities for blender
from blender_utils import set_render_settings
from blender_utils import delete_scene_objects
from blender_utils import get_object_by_name
from blender_utils import look_at
from blender_utils import add_background
from blender_utils import add_billboard
from blender_utils import add_video_billboard
from blender_utils import hide_obj
from blender_utils import add_action

animation_controller = AnimationController()

def set_mouth_img(obj, _pos):
  """ Mouth positions arem apped 0->9 as described in phonemes.py
  We set the "position" by remapping UV coordinates for an object
  called "mouth" somwhere in the scene.
  The layout of the mouths texture a simple 4x4 layout with
  zero position in the UL corner.
  """
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

def on_utterance_frame(frame, s):
  """
  callback invoked once per frame by animation system to set a
  mouth object to the proper texture as provided by phonemes in
  the animation.
  """
  obj = get_object_by_name('mouth')
  set_mouth_img(obj, s.sound())

def on_video_frame(video, frame):
  """
  callback invoked once per frame (before render) to create/destroy video objects
  as they are played by the animation.
  Yes I'd like to simply hide them for greater control but blender sux, so...
  """
  if frame == video._start_frame:
    bb = add_video_billboard(video._filename, video._name, loc=[-0.26,0.15,1.0], scale=0.15, frame=frame)
  elif frame == video._end_frame:
    bpy.data.objects[video._name].select = True
    bpy.ops.object.delete()
    

# set callbacks in the animation controller
animation_controller._on_utterance = on_utterance_frame
animation_controller._on_video = on_video_frame

def on_before_render(scene):
  global animation_controller
  scene = bpy.context.scene
  frame = scene.frame_current
  animation_controller.update(frame)
   

def generate_video():
  """
  Primary function to generate video via blender
  """
  global animation_controller

  # args are passed as a single string, the last command line arg
  a = sys.argv[-1]
  a = ' '.join(a.split())
  _args = a.strip().split(' ')
  print("Generating Video with command line args: " + str(_args))
  parser = argparse.ArgumentParser(description='Generate video from input script.')
  parser.add_argument('infile', help='Input script txt file.')
  parser.add_argument('-o', '--out', help='Output file path')
  parser.add_argument('-a', '--assetdir', help='Generated asset resource dir')
  parser.add_argument('-t', '--test', action='store_true', default=False, help='Test run only generating single output image')
  parser.add_argument('-n', '--norender', action='store_true', default=False, help='Turn off all rendering.')
  parser.add_argument('-s', '--save', help='Save a blend file of configuration.')
  args = parser.parse_args(_args)
  
  script_filepath = args.infile
  out_filepath = script_filepath + '.mov'
  if args.out:
    out_filepath = args.out
  only_render_image = args.test
  no_render = args.norender
  blendfile_to_save = None
  if args.save:
    blendfile_to_save = args.save

  # Load our default scene and assets.
  # TODO: specify this by argument
  bpy.ops.wm.open_mainfile(filepath="./models/default.blend")


  context = bpy.context
  scene = bpy.context.scene
  world = bpy.context.scene.world
  if not scene.sequence_editor:
    scene.sequence_editor_create()

  # end_frame tracks the length in total frames of generated video
  end_frame = 0
  
  # load a script passed as argument
  print("opening file: " + script_filepath)
  script = Script(script_filepath, asset_dir=args.assetdir)

  # for debugging just add an enter action at frame zero
  do_dummy_actions = False
  if do_dummy_actions:
    enter_action = add_action("anime.girl.head", "enter", 0)
    end_frame = enter_action.frame_end

  # add audio for all lines in script
  #for line in script:
  for i in range(len(script._lines)):
    print("line: " + str(i) + " at frame: " + str(end_frame))
    line = script._lines[i]
    end_frame = line.animate(scene, animation_controller, current_frame=end_frame)

  if do_dummy_actions:
    exit_action = add_action("anime.girl.head", "exit", end_frame)
    end_frame = exit_action.frame_end

  # run a handler on each frame
  bpy.app.handlers.frame_change_pre.append(on_before_render)

  # TODO: ability to cap frame limit for test renders
  #end_frame = 48
  bpy.context.scene.frame_end = end_frame
  bpy.context.scene.render.filepath = out_filepath
 
  if blendfile_to_save:
    print("Saving script configuration as blend file: " + blendfile_to_save)
    bpy.ops.wm.save_as_mainfile(filepath=blendfile_to_save)

  # render video
  if not no_render:
    render_video = not only_render_image
    if render_video == True:
      bpy.ops.render.render(animation = True, write_still = False)
    else:
      # Render still image, automatically write to output path
      bpy.context.scene.render.filepath = out_filepath + '.png'
      bpy.ops.render.render(write_still=True)

  bpy.ops.wm.quit_blender()


if __name__ == '__main__':
  generate_video()
