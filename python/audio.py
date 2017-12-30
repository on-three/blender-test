

import os


class Audio(object):
  def __init__(self, filename, speaker=None, asset_dir='./tmp'):
    self._filename = filename
    self._speaker = speaker
    f = os.path.basename(filename)
    self._phoneme_file = None
    if self._speaker:
      self._phoneme_file = asset_dir + '/' + f + '.phonemes.txt'
      print("*** PHONEME FILE: " + self._phoneme_file)
  
  def __str__(self):
    return "AUDIO: " + str(self._speaker) + " : " + self._filename

  # the direction name specified in script
  DIRECTION="AUDIO"

  @staticmethod
  def generator(script, speaker, args, asset_dir='./tmp'):
    """Static constructor we can store in a dictionary
    """
    return Audio(filename=args, speaker=speaker, asset_dir=asset_dir)
    
  def gen_audio_file(self, out_dir='./tmp'):
    # don't generate this audio file. it should already exist
    # so we just check it's there
    if not os.path.isfile(self._filename):
    	raise IOError("Could not find audio file: %s" % (self._filename))
    
  def gen_phoneme_file(self, out_dir='./tmp'):
    print("Attempting to generate phoneme file for file " + self._filename)
    print("out dir = " + out_dir)
    # only generate a phoneme file if there is a "speaker" to say this shit
    if not self._speaker:
      return
    outfile = self._phoneme_file 
    infile = self._filename
    print(">>>> phoneme file to generate: " + self._phoneme_file)
    cmd = 'tools/phonemes.sh {infile} {output_dir}'.format(infile=infile, output_dir=out_dir)
    print("Generating phonemes file for input audio file " + infile)
    os.system(cmd)

  def animate(self, scene, animation_controller, current_frame, fps=30):
    """
    """
    end_frame = current_frame
    audio_file = self._filename
    # fail if the required audio file is not present
    if not os.path.isfile(audio_file):
      raise IOError("Could not find requried audio file: %s" % audio_file)

    phoneme_file = self._phoneme_file
    if phoneme_file and not os.path.isfile(phoneme_file):
      raise IOError("Coudld not find requried phoneme file: %s" % phoneme_file)
    
    if phoneme_file:
      animation_controller.add_utterance(self._speaker, current_frame, "", phoneme_file)
      #def add_utterance(self, speaker, start_frame, text, phoneme_file, fps=30):
    
    soundstrip = scene.sequence_editor.sequences.new_sound(audio_file, audio_file, 3, current_frame)
      # as per https://blender.stackexchange.com/questions/47131/retrieving-d-imagessome-image-frame-duration-always-returns-1
    print(str(soundstrip.frame_final_end))
    duration = soundstrip.frame_final_end
    print(duration)

    end_frame = soundstrip.frame_final_end #frame_duration
    return end_frame

  
