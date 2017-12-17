"""
"""

import re
from phonemes import Tokenizer as PhonemeTokenizer

class Video(object):
  def __init__(self, filename, name, start_frame, end_frame, fps):
    self._filename = filename
    self._name = name
    self._start_frame = start_frame
    # TODO: correctly calculate endframe or feed as arg
    self._end_frame = end_frame #start_frame + fps
    self._fps = fps

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

  def add_utterance(self, speaker, start_frame, phoneme_file, fps=24):
    s = PhonemeTokenizer(phoneme_file, start_frame=start_frame, speaker=speaker)
    if s:
      self._utterances.append(s)
    print("number of utterances now: " + str(len(self._utterances)))

  def add_video(self, speaker, video, start_frame, end_frame, fps=30):
   print("Going to play video {video} at frame {start_frame}".format(video=video, start_frame=start_frame))
   self._videos.append(Video(video, speaker, start_frame, end_frame, fps))


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

