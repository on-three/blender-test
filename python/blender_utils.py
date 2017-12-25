# -*- coding: utf-8 -*-
"""
MODULE: blener_utils
AUTHOR: on-three
EMAIL: on.three.email@gmail.com
DESC: Simple untility functions to configure blender scripting
"""

import bpy
import sys, os
from math import pi
from mathutils import Vector

def set_render_settings(w=1920, h=1080, scale=100, fps=24):
  """
  Set blender render settings
  Args:
    w: rendered screen width in pixels
    h: rendered screen height in pixels
    scale: scaling factor applied to rendering (render.resolution_percentage)
    fps: rendered video fps
  """
  render = bpy.context.scene.render
  render.resolution_x = w
  render.resolution_y = h
  render.resolution_percentage = scale
  render.fps = 24
  render.use_raytrace = False
  #render.use_color_management = True
  render.use_sss = False
  return

def get_object_by_name (name= ""):
  """
  Get a blender object in the current scene by its string name
  Args:
    name: name of the object we'll retrieve.
  Returns:
    Blender object found or None if not found
  """
  r = None
  obs = bpy.data.objects
  for ob in obs:
    if ob.name == name:
      r = ob
      return r
  return r

def hide_obj(obj, hide=True):
  for child in obj.children:
    child.hide_render = hide
    hide_obj(child, hide)

def look_at(obj_camera, point):
  """
  Configure the current scene camera to look at a specific point in 3Space
  Args:
    obj_camer: camera object in scene
    point: 3Space position of object to look at
  """
  loc_camera = obj_camera.matrix_world.to_translation()

  p = Vector(point)
  direction = p - loc_camera
  # point the cameras '-Z' and use its 'Y' as up
  rot_quat = direction.to_track_quat('-Z', 'Y')

  # assume we're using euler rotation
  obj_camera.rotation_euler = rot_quat.to_euler()

def delete_scene_objects(scene=None):
  """
  Delete a scene and all its objects.
  Note that this will also delete your current camera and lighting,
  which MUST be added again to render successfully.
  """
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
  """
  Add a background to the current view
  I don't recommend using this approach.
  Args:
    filepath: path to the image you'll load to the background
  """
  img = bpy.data.images.load(filepath)
  texture = bpy.data.textures.new("Texture.001", 'IMAGE')
  texture.image = img
  bpy.data.worlds['World'].active_texture = texture
  bpy.context.scene.world.texture_slots[0].use_map_horizon = True
  bpy.context.scene.world.texture_slots[0].texture_coords = 'VIEW'



def add_texture(obj, img_path, texture_name):
  """
  Add a texture to the provided object.
  This is mainly a utility function used by add_billboard function and
  I don't recommend using it in other modules.
  Args:
    obj: Blender object we'll add a texture to
  """
  try:
    img = bpy.data.images.load(img_path)
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
  slot.use_map_alpha = True

  obj.data.materials.append(mtex)
  return (mtex, cTex)

def add_video_texture(obj, video_path, texture_name):
  """
  Add a video texture to the provided object.
  This is mainly a utility function used by add_billboard function and
  I don't recommend using it in other modules.
  Args:
    obj: Blender object we'll add a texture to
  """
  try:
    img = bpy.data.images.load(video_path)
    # as per https://blender.stackexchange.com/questions/47131/retrieving-d-imagessome-image-frame-duration-always-returns-1
    #img.use_cyclic = True
    print(img.resolution)
    duration = img.frame_duration
    print(duration)
    with open(texture_name + "_xxx.txt", "w") as f:
      f.write("duration: " + str(img.frame_duration))
      f.close()
  except:
    raise NameError("Cannot load video %s" % video_path)
 
  # documentation indicates we can use IMAGE here for videos
  ctex = bpy.data.textures.new(texture_name, type = 'IMAGE')
  ctex.image = img

  ctex.image_user.frame_duration = img.frame_duration
  
  # Create new material
  mtex = bpy.data.materials.new(texture_name + '-material')
  mtex.diffuse_color = (1, 1, 1)
  mtex.transparency_method = 'Z_TRANSPARENCY'
  #mtex.use_transparency = True
  mtex.alpha = 0.0
  
  
  slot = mtex.texture_slots.add()
  slot.texture = ctex
  slot.texture_coords = 'UV'
  #slot.use_map_alpha = True

  #img.frame_duration = 400
  
  obj.data.materials.append(mtex)
  return (mtex, ctex)



def add_billboard(img_path, n, loc=[0,0,0], scale=1):
  """
  Add a simple billboard at a given location in 3Space.
  It will be sized according to the image dimensions.
  Generally I'd suggest using 'import as plane' in blender rather
  than using this.
  Args:
    img_path: path to image we'll load on the billboard
    n: string name of the new object to help manipulating later
    loc: 3Space coordinates (array) of position of billboard center.
    scale: scaling factor evenly applied to all dimensions of billboard.
  """
  context = bpy.context
  bpy.ops.mesh.primitive_plane_add(view_align=True,
  radius=1,
  location=loc,
  rotation=[0, 0, 0])
  plane = context.object
  plane.name = n
  bpy.context.scene.layers[2] = True
  bpy.ops.mesh.uv_texture_add()
  material_name = n + '-material'
  texture_name = n + '-texture'
  (mat, tex) = add_texture(plane, img_path, n + "_texture")
  # scale the billboard to match image dimensions
  sz = tex.image.size
  x = sz[0]
  y = sz[1]
  plane.scale = (x*scale, y*scale, 1)
  return plane
 
def add_video_billboard(video_path, name, loc=[0,0,0], scale=1, frame=0):
  """
  Add a simple billboard at a given location in 3Space.
  It will be sized according to the image dimensions.
  Generally I'd suggest using 'import as plane' in blender rather
  than using this.
  Args:
    img_path: path to image we'll load on the billboard
    n: string name of the new object to help manipulating later
    loc: 3Space coordinates (array) of position of billboard center.
    scale: scaling factor evenly applied to all dimensions of billboard.
  """
  context = bpy.context
  bpy.ops.mesh.primitive_plane_add(view_align=True,
  radius=1,
  location=loc,
  rotation=[0, 0, 0])
  plane = context.object
  plane.name = name
  bpy.context.scene.layers[2] = True
  bpy.ops.mesh.uv_texture_add()
  material_name = name + '-material'
  texture_name = name + '-texture'
  (mtex, tex) = add_video_texture(plane, video_path, name + "-texture")
  # scale the billboard to match image dimensions
  sz = tex.image.size
  # we scale the plane we created to match movie dimensions
  # AND the scale used by "import as plan" extension in blender, where
  # a 1024x1024 image is imported as a 1.024x1.024 square.
  x = sz[0]/1000.0
  y = sz[1]/1000.0
  plane.scale = (x*scale, y*scale, 1)
  tex.image_user.frame_start = frame
  return plane

def add_action(obj_name, action_name, start_frame):
  """
  Method returns an object describing the added action
  ESPECIALLY the ending frame for the strip added to the NLA editor
  """
  #try:
  #    selected_strips = [strip for strip in bpy.context.object.animation_data.nla_tracks.active.strips if strip.select]
  #    except AttributeError:
  #        selected_strips = []

  #bject.animation_data_create()
  #object.animation_data.action = bpy.data.actions.get(action_name)
  
  # get the object
  obj = bpy.data.objects.get(obj_name)
  if not obj:
    print("Could not find object named: " + obj_name + " in scene.")
    pass #return
  
  # get our action
  action = bpy.data.actions.get(action_name)
  if not action:
    pass #return

  # get/create the animation track (we'll add the action above as a strip to this track)
  a = obj.animation_data.action
  track = obj.animation_data.nla_tracks.new()
  s = track.strips.new(action.name, start_frame, action);
  #bpy.ops.nla.actionclip_add(s)

  # clients can get the end frame from the returned strip
  return s


  #obj = bpy.data.objects[obj_name]
  #if not obj:
  #  return None

  #if obj.animation_data is not None:
  #  action = obj.animation_data.action
  #  if action is not None:
  #    track = obj.animation_data.nla_tracks.new()
  #    track.strips.new(action.name, action.frame_range[0], action)
  #    obj.animation_data.action = None
  #pass

