import os.path
import re
import pipes

from audio import Audio
from action import Action
from video import Video
from voice import Voice
from pause import Pause
from naturalreaders import do_tts

class Speaker(object):
  def __init__(self, name):
    self._name = name
    self._voice = None
  def __str__(self):
    return self._name

class Line(object):
  # infer phoneme files via filename
  PHONEME_FILE_SUFFIX = '.phonemes.out.txt'
  PADDING_SECONDS = 0.5 # pad utterances by n frames at the start
  directions = {
    Audio.DIRECTION : Audio.generator,
    Video.DIRECTION : Video.generator,
    Action.DIRECTION : Action.generator,
    Voice.DIRECTION : Voice.generator,
    Pause.DIRECTION : Pause.generator,
  }

  def gen_filename(self, path, extension):
    if self._speaker:
      return path + '/' + str(self._index) + '.' +  self._speaker._name + extension
    else:
      return path + '/' + str(self._index) + extension
  
  def __init__(self, text, index, speaker=None, asset_dir='./tmp'):
    # simply put this 'line' is meaningless without additional assets
    # so an asset directory is really needed to infer assets
    self._asset_dir = asset_dir
    self._speaker = speaker
    self._text = text
    self._index = index
    self._audio_file = self.gen_filename(asset_dir, '.mp3')
    self._phoneme_file = self._audio_file + '.phonemes.txt'
    self._voice = None

  def set_voice(self, voice):
    self._voice = voice

  def get_voice(self):
    return self._voice

  def __str__(self):
    speaker = "NONE"
    if self._speaker:
      speaker = self._speaker._name
    s = "Line: " + speaker + " : " + self._text
    return s

	
  def gen_audio_file(self, out_dir='./tmp'):
    outfile = self._audio_file or self.gen_filename(out_dir, '.mp3')
    self._audio_file = outfile
   
    # the audio file for this line might already exist
    if os.path.isfile(outfile):
      print("Audio file {file} already exists. Not generating.".format(file=self._audio_file))
      return
    # if we've set a voice, try to fetch tts from the web naturalvoices
    text = pipes.quote(self._text)
    if self._speaker and self._speaker._voice:
      voice = self._speaker._voice
      do_tts(text, outfile, voice=self._speaker._voice._name, speed="1")
    else:
      tool = 'gtts-cli'
      cmd = '{tool} -o {outfile} {text}'.format(tool=tool, outfile=outfile, text=text)
      print('Making system call: "%s"' % (cmd))
      os.system(cmd)

    # if we didn't generate a file, fail
    if not os.path.isfile(outfile):
    	raise IOError("Could not generate file: %s" % (outfile))
      
    print('Wrote file %s' % (outfile))
    
  def gen_phoneme_file(self, out_dir='./tmp'):
    outfile = self._phoneme_file or self.gen_filename(out_dir, '.phonemes.txt') 
    self._phoneme_file = outfile
    infile = self._audio_file or self.gen_filename(out_dir, '.mp3')
    cmd = 'tools/phonemes.sh {infile}'.format(infile=infile)
    print("Generating phonemes file for input audio file " + infile)
    os.system(cmd)

  def animate(self, scene, animation_controller, current_frame, fps=30):
    """Handle a spoken line
    """
    end_frame = current_frame
    audio_file = self._audio_file
    # fail if the required audio file is not present
    if not os.path.isfile(audio_file):
      raise IOError("Could not find requried audio file: %s" % audio_file)

    phoneme_file = self._phoneme_file
    if not os.path.isfile(phoneme_file):
      raise IOError("Coudld not find requried phoneme file: %s" % phoneme_file)
   
    start_frame = current_frame + Line.PADDING_SECONDS * fps
    animation_controller.add_utterance(self._speaker, start_frame, self._text, phoneme_file)
    soundstrip = scene.sequence_editor.sequences.new_sound(audio_file, audio_file, 3, start_frame)
      # as per https://blender.stackexchange.com/questions/47131/retrieving-d-imagessome-image-frame-duration-always-returns-1
    print(str(soundstrip.frame_final_end))
    duration = soundstrip.frame_final_end
    print(duration)

    end_frame = soundstrip.frame_final_end #frame_duration
    return end_frame
 
  @staticmethod
  def parse(script, index, line, asset_dir='./tmp'):
		# eliminate comments
    line = line.split('#')[0].strip()
    if not len(line):
      return index

    # first remove speaker at start of line if there is one
    # There may or may not be a speaker for a line
    speaker = None

    speaker_regex = re.compile(r'^(?P<speaker>[^()\s:]+):(?P<remainder>.+)')
    #speaker_regex = re.compile(r'^(?P<speaker>[^:\w]+):(?<remainder>.+)$')
    speaker_match = speaker_regex.match(line)
    if speaker_match:
      speaker_name = speaker_match.groupdict()['speaker']
      if not speaker_name in script._speaker_map:
        speaker = Speaker(speaker_name)
        script._speaker_map[speaker_name] = speaker
      else:
        speaker = script._speaker_map[speaker_name]

      line = speaker_match.groupdict()['remainder'].strip()
		
    if not len(line):
      if speaker:
        # TODO; speaker with no line means insert x second pause
        pass
      return index
		
		# chew through the rest of the line, removing text and
		# stage directions sequentially
    #r = re.compile( r'\([^:\w]+:[^)]?\)' )
    #r = re.compile( r'(\([^)]+\))' )
    r = re.compile( r'(\([^\W:]+:[^)]+\))' )
    direction_regex = re.compile( r'(\((?P<direction>[^\W:]+):(?P<args>[^)]+)\))' )
    elements = re.split(r, line)
    print("split line: " + str(elements))
    for e in range(len(elements)):
      element = elements[e]
      element = element.strip()
      if not len(element):
        continue

      print("element: " + element)
      m = direction_regex.match(element)
      newline = None
      if m:
        direction = m.groupdict()['direction']
        args = m.groupdict()['args'].strip()
        print("Detected an direction. speaker: " + str(speaker) + " direction: " + direction + " args: " + args)
        if direction in Line.directions:
          newline = Line.directions[direction](script, speaker, args, asset_dir=asset_dir)
      else:
        # this just a spoken line
        newline = Line(element, index, speaker=speaker, asset_dir=asset_dir)

      if newline:
        index = index + 1
        script.add_line(newline)
    return index

				
