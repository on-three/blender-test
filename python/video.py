


class Video(object):
  def __ini__(self, filename, start_frame=0, obj_name="screen", fps=30, end_frame=None):
    self._filename = filename
    self._fps = fps
    self._obj_name = obj_name
    self._start_frame = start_frame
    self._end_frame = end_frame

  def animate(self, animation_controller, current_frame):
    """
    Animate this video, adding it to the scene for X frames
    """
    # Add video to timeline, get length
    self._start_frame = self._start_frame + current_frame
    print("LINE: video {video} at frame {start}".format(video=line._video, start=start_frame)) 
    vid = animation_controller.add_video(self._obj_name, self._filename, self._start_frame, 30)
    # TODO: better handling of end frame to play video segments
    self._end_frame = vid._end_frame
    #add_video_billboard('./video/tits.avi', 'TITS', loc=[0,0,0], scale=0.015, frame=0)
    return self._end_frame
