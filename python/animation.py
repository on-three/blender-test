"""
"""

import re
from phonemes import Tokenizer as PhonemeTokenizer
from blender_utils import add_action as bpy_add_action
import bpy

class Video(object):
  def __init__(self, filename, name, start_frame, fps):
    self._filename = filename
    self._name = name
    self._start_frame = start_frame
    # TODO: correctly calculate endframe or feed as arg
    #self._end_frame = end_frame #start_frame + fps
    self._fps = fps
    # we may not add it to a mesh until later, but attempt to preload
    # the video texture as we can access video length (in frames)
    img = bpy.data.images.load(filename)
    # as per https://blender.stackexchange.com/questions/47131/retrieving-d-imagessome-image-frame-duration-always-returns-1
    #img.use_cyclic = True
    print(img.resolution)
    duration = img.frame_duration
    print(duration)
 
    # documentation indicates we can use IMAGE here for videos
    ctex = bpy.data.textures.new(filename, type = 'IMAGE')
    ctex.image = img
    ctex.image_user.frame_duration = img.frame_duration
    self._length = img.frame_duration
    # unless there's an override, define end_frame as start_frame + length
    self._end_frame = self._start_frame + self._length
    self._movie = img
    self._texture = ctex
    
  def get_frame(self, frame):
    if frame >= self._start_frame and frame <= self._end_frame:
      return self;
    return None


class AnimationController(object):
  def __init__(self, on_utterance=None, on_video=None):
    self._on_utterance = on_utterance
    self._on_video = on_video
    self._utterances = []
    self._videos = []

  def add_utterance(self, speaker, start_frame, text, phoneme_file, fps=24):
    s = PhonemeTokenizer(phoneme_file, start_frame=start_frame, speaker=speaker, text=text)
    if s:
      self._utterances.append(s)
    print("number of utterances now: " + str(len(self._utterances)))
    return s

  def add_video(self, speaker, video, start_frame, fps=30):
    print("Going to play video {video} at frame {start_frame}".format(video=video, start_frame=start_frame))
    vid = Video(video, speaker, start_frame, fps)
    self._videos.append(vid)
    return vid

  def add_action(self, obj_name, action_name, start_frame):
    s = bpy_add_action(obj_name, action_name, start_frame)
    return s

 
  def set_on_utterance(self, handler):
    self._on_utterance = handler

  def set_on_video(self, handler):
    self._on_video = handler

  def update(self, frame):
    for u in self._utterances:
      s = u.get_sound(frame)
      if s and self._on_utterance:
        self._on_utterance(frame, s)
    
    for vid in self._videos:
      s = vid.get_frame(frame)
      if s and self._on_video:
        #TODO: update blender video texture in some way?
        self._on_video(s,frame)

