"""
Set a voice on a speaker tracked in the script object
"""
import os

class Voice(object):
  def __init__(self, name, speaker=None, asset_dir='./tmp'):
    self._name = name
    self._speaker = speaker
    if self._speaker:
      self._speaker._voice = self
  
  def __str__(self):
    speaker_name = "NONE"
    if self._speaker:
      speaker_name = self._speaker._name
    return "VOICE: " + speaker_name + " : " + self._name

  # the direction name specified in script
  DIRECTION="VOICE"

  @staticmethod
  def generator(script, speaker, args, asset_dir='./tmp'):
    """Static constructor we can store in a dictionary
    """
    return Voice(name=args, speaker=speaker, asset_dir=asset_dir)
    
  def gen_audio_file(self, out_dir='./tmp'):
    pass
    
  def gen_phoneme_file(self, out_dir='./tmp'):
    pass

  def animate(self, scene, animation_controller, current_frame, fps=30):
    """
    """
    end_frame = current_frame
    return end_frame


