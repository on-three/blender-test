"""
Simple pause for N seconds
"""

import os


class Pause(object):
  def __init__(self, duration, speaker=None, asset_dir='./tmp'):
    self._duration = float(duration)
  
  def __str__(self):
    return "PAUSE: " + str(self._duration) + " seconds."

  # the direction name specified in script
  DIRECTION="PAUSE"

  @staticmethod
  def generator(script, speaker, args, asset_dir='./tmp'):
    """Static constructor we can store in a dictionary
    """
    return Pause(duration=args, speaker=speaker, asset_dir=asset_dir)
    
  def gen_audio_file(self, out_dir='./tmp'):
    pass

  def gen_phoneme_file(self, out_dir='./tmp'):
    pass

  def animate(self, scene, animation_controller, current_frame, fps=30):
    """
    """
    end_frame = current_frame + self._duration * fps
    return end_frame

  
