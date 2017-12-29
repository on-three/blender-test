"""
	action.py
	Basic script driven action
"""

class Action(object):
  def __init__(self, name, speaker, start_frame=0, asset_dir='./tmp'):
    self._name = name
    self._speaker = speaker
    self._start_frame = start_frame
    self._asset_dir = asset_dir
  
  def __str__(self):
    return Action.DIRECTION + ":"  + self._name

  # the direction name specified in script
  DIRECTION="ACTION"

  def gen_audio_file(self, out_dir='./tmp'):
    # don't generate audio off actions
    pass
    
  def gen_phoneme_file(self, out_dir='./tmp'):
    # don't generate phoneme files of actions
    pass

  @staticmethod
  def generator(script, speaker, args, asset_dir='./tmp'):
    """Static constructor we can store in a dictionary
    """
    return Action(name=args, speaker=speaker, asset_dir=asset_dir)
 
  #end_frame = line.animate(scene, animation_controller, current_frame=end_frame)
  def animate(self, scene, animation_controller, current_frame):
    """
    Animate this video, adding it to the scene for X frames
    """
    print("ACTION: speaker: " + str(self._speaker) + " name: " + self._name + " start frame: " + str(self._start_frame));
    # Add video to timeline, get length
    self._start_frame = self._start_frame + current_frame
    target = None
    if self._speaker:
      target = self._speaker._name
    exit_action = animation_controller.add_action(target, self._name, self._start_frame)
    print("----> " + str(exit_action.frame_end))
    self._end_frame = exit_action.frame_end
    print("----> " + str(exit_action.frame_end))

    self._end_frame = exit_action.frame_end
    return self._end_frame
