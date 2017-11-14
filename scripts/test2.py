# Run as: blender -b <filename> -P <this_script> -- <args>
import bpy
import sys, os
from math import pi

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


if __name__ == '__main__':
  # you can catch command line arguments this way
  filePath = sys.argv[-1]
  
  setRenderSettings()
  for scene in bpy.data.scenes:
    scene.render.image_settings.file_format = 'H264'
    scene.render.ffmpeg.format = 'QUICKTIME'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.ffmpeg.audio_codec = 'AAC'
  scene.render.ffmpeg.audio_bitrate = 128
  scene.render.resolution_percentage = 100
  bpy.context.scene.frame_start = 0
  bpy.context.scene.frame_end = 24
  bpy.context.scene.render.filepath = filePath
  bpy.ops.render.render(animation = True, write_still = False)

  bpy.ops.wm.quit_blender()
