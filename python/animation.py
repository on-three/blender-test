"""
"""

import re
from phonemes import Tokenizer as PhonemeTokenizer
from blender_utils import add_action as bpy_add_action
import bpy

def srt_time_format(time_seconds):
  seconds = time_seconds
  hours = int(seconds/3600)
  seconds = seconds - (hours * 3600)
  minutes = int(seconds/60)
  seconds = seconds - (minutes * 60)
  fractional = time_seconds - int(time_seconds)
  #00:02:17,440 --> 00:02:20,375
  s = "%02d:%02d:%02d,%03d" % (hours, minutes, int(seconds), int(fractional*100))
  return s

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

class SRTSubtitleWriter(object):
  def __init__(self, outfile, max_sub_time_sec=3.5, fps=30):
    self._outfile = outfile
    self._max_sub_time_sec = max_sub_time_sec
    self._fps = fps
    self._f = open(self._outfile, "w")
    self._last_utterance_text = None
    self._last_utterance_frame = 0
    self._counter = 1

  def finalize(self):
    if self._last_utterance_text:
      last_frame = int((self._last_utterance_frame / self._fps + self._max_sub_time_sec)*self._fps)
      self.write_line(self._last_utterance_text, last_frame)
    self._f.close()

  def write_line(self, text, current_frame):
    if self._last_utterance_text:
      start_time = self._last_utterance_frame / self._fps
      end_time = current_frame / self._fps
      if end_time - start_time > self._max_sub_time_sec:
        end_time = start_time + self._max_sub_time_sec
      self._f.write("%d\n" % (self._counter))
      self._f.write("%s --> %s\n" % (srt_time_format(start_time), srt_time_format(end_time)))
      self._f.write("%s\n" % (self._last_utterance_text))
      self._f.write("\n")
      self._f.flush()
      self._counter = self._counter + 1

    self._last_utterance_frame = current_frame
    self._last_utterance_text = text
    
  def update(self, frame):
    # has enough time elapsed to write the last sub to the file?
    pass


class AnimationController(object):
  def __init__(self, on_utterance=None, on_video=None, srt_outfile=None):
    self._on_utterance = on_utterance
    self._on_video = on_video
    self._utterances = []
    self._videos = []
    self._srt = None
    if srt_outfile:
      self._srt = SRTSubtitleWriter(srt_outfile)

  def add_utterance(self, speaker, start_frame, text, phoneme_file, fps=30):
    s = PhonemeTokenizer(phoneme_file, start_frame=start_frame, speaker=speaker, text=text)
    if s:
      self._utterances.append(s)
    print("number of utterances now: " + str(len(self._utterances)))

    if self._srt:
      self._srt.write_line(text, start_frame);

    return s

  def finalize(self):
    if self._srt:
      self._srt.finalize()

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

