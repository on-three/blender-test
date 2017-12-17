"""
"""

import re
from phonemes import Tokenizer as PhonemeTokenizer

class AnimationController(object):
  def __init__(self, on_frame_handler=None):
    self._on_frame_handler=on_frame_handler
    self._utterances = []

  def add_utterance(self, speaker, start_frame, phoneme_file, fps=24):
    s = PhonemeTokenizer(phoneme_file, start_frame=start_frame, speaker=speaker)
    if s:
      self._utterances.append(s)
    print("number of utterances now: " + str(len(self._utterances)))

  def set_on_frame_handler(self, handler):
    print("SET ON FRAME HANDLER TO " + str(handler))
    self._on_frame_handler = handler

  def update(self, frame):
    for u in self._utterances:
      #x.nothing()
      s = u.get_sound(frame)
      if s and self._on_frame_handler:
        self._on_frame_handler(frame, s)

