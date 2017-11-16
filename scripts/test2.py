# Run as: blender -b <filename> -P <this_script> -- <args>
import bpy
import sys, os
from math import pi
from mathutils import Vector

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

def add_camera(name, loc, look_pt):
  context = bpy.context
  bpy.ops.object.camera_add(view_align=False,
    location=loc,
    rotation=[0, 0, 0])
  #bpy.context.object.data.type = 'ORTHO'
  #bpy.context.object.data.ortho_scale = 1920.0*2.0
  camera = context.object
  bpy.context.scene.camera = camera
  #camera.location = (0,10,20)
  look_at(camera, look_pt) 
  #look_at(camera, [0.0, 0.0, 0.0]) 
  camera.name = name

def on_frame(scene):
  print("Frame Change", scene.frame_current)
  scene = bpy.data.scenes['Scene']
  frame = scene.frame_current
  if frame < 2* 24:
    scene.camera = bpy.data.objects['Camera.1']
  elif frame < 4* 24:
    scene.camera = bpy.data.objects['Camera.2']
  elif frame < 6 * 24:
    scene.camera = bpy.data.objects['Camera.3']
  else:
    scene.camera = bpy.data.objects['Camera.1']

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

def setup_scene():
  scene = bpy.context.scene
  if not scene.sequence_editor:
    scene.sequence_editor_create()

  soundstrip = scene.sequence_editor.sequences.new_sound("1", "audio/1.cia.mp3", 3, 1)
  end = soundstrip.frame_final_end #frame_duration
  soundstrip = scene.sequence_editor.sequences.new_sound("2", "audio/2.bane.mp3", 3, end)
  end = soundstrip.frame_final_end #end + soundstrip.frame_duration
  soundstrip = scene.sequence_editor.sequences.new_sound("3", "audio/3.cia.mp3", 3, end)
  end = soundstrip.frame_final_end #end + soundstrip.frame_duration
  soundstrip = scene.sequence_editor.sequences.new_sound("4", "audio/4.bane.mp3", 3, end)
  filepath = "models/person.blend"

  
  # append all objects starting with 'house'
  with bpy.data.libraries.load(filepath) as (data_from, data_to):
    #data_to.objects = [name for name in data_from.objects if name == "person"]
    #data_to.objects = ['person', 'body', 'Pose', 'Armature']
    data_to.objects = ['person', 'body']
  
  

  # link them to scene
  x = 0.5
  y = 0.5
  scene = bpy.context.scene

  for obj in data_to.objects:
    if obj is not None:
      scene.objects.link(obj)
      obj.location = (x, y, 3)

  x = x - 1
  y = y - 1

  body_data = bpy.data.objects['body'].data
  body_copy = body_data.copy()
  body2 = bpy.data.objects.new("body2", body_copy)
  body2.location = (x, y, 3)
  body2.scale = bpy.data.objects['body'].scale
  scene.objects.link(body2)
  scene.update()

  person_data = bpy.data.objects['person'].data
  person_copy = person_data.copy()
  person2 = bpy.data.objects.new("person2", person_copy)
  person2.location = (x, y, 3)
  person2.scale = bpy.data.objects['person'].scale
  scene.objects.link(person2)
  
  body2.parent = person2

  scene.update()

  # Add some cameras to cycle through
  add_camera("Camera.1", [0,-5,5], [0,0,5])
  add_camera("Camera.2", [2,-5,5], [0,0,5])
  add_camera("Camera.3", [-2,-5,5], [0,0,5])

if __name__ == '__main__':
  # you can catch command line arguments this way
  filePath = sys.argv[-1]
  
  setRenderSettings()

  setup_scene()
  
  # run a handler on each frame
  bpy.app.handlers.frame_change_pre.append(on_frame)

  render_video = True
  if render_video == True:
    for scene in bpy.data.scenes:
      scene.render.image_settings.file_format = 'H264'
      scene.render.ffmpeg.format = 'QUICKTIME'
      scene.render.image_settings.color_mode = 'RGB'
      scene.render.ffmpeg.audio_codec = 'AAC'
      scene.render.ffmpeg.audio_bitrate = 128
      scene.render.resolution_percentage = 100
    #bpy.context.scene.frame_start = 0
    #bpy.context.scene.frame_end = 24
    #bpy.context.scene.render.filepath = 'out/' + os.path.basename(__file__) + '.mov'
    bpy.context.scene.render.filepath = filePath
    bpy.ops.render.render(animation = True, write_still = False)
  else:
    # Render still image, automatically write to output path
    bpy.context.scene.render.filepath = 'out/' + os.path.basename(__file__) + '.png'
    bpy.ops.render.render(write_still=True)
  
  bpy.ops.wm.quit_blender()
