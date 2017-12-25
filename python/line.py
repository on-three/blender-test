import os.path
import re

from action import Action

class Line(object):
  # infer phoneme files via filename
  PHONEME_FILE_SUFFIX = '.phonemes.out.txt'

  def __init__(self, index=0):
    self._speaker = None
    self._text = None
    self._index = index
    self._audio_file = None
    self._phoneme_file = None
    self._post = None
    self._image = None
    self._voice = None
    self._video = None
    
  def gen_filename(self, path, extension):
    if self._post:
      return path +'/' + self._post + extension
    elif self._video:
      vid = ntpath.basename(self._video)
      return path + '/' + vid + extension
    elif self._speaker:
      return path + '/' + str(self._index) + '.' + self._speaker + extension
    else:
      return path + '/' + str(self._index) + extension

  @staticmethod
  def parse(index, line, tmp_dir='./tmp'):
    # parse indivdual lines of dialog for speaker and text
    r = re.compile(r'^(?P<speaker>[^\s:]+):( )?(?P<text>.+)')
    # parse any string for "stage directions"
    pd = re.compile(r'\((?P<desc>[^\s():]+):(?P<direction>[^()]+)?\)')

    new_line = Line(index=index)
    valid_line = False

    # remove "stage directions" before processing the line properly
    for d in pd.finditer(line):
      valid_line = True
      desc = d.group('desc')
      direction = None
      if 'direction' in d.groupdict():
        direction = d.group('direction').strip()
      print("Direction: {desc} --> {direction}".format(desc=desc, direction=direction))

      if desc == 'AUDIO':
        # an audio file contains the lines spoken at this point
        new_line._audio_file = str(direction)
        new_line._phoneme_file = new_line._audio_file + Line.PHONEME_FILE_SUFFIX
      elif desc == 'POST':
        # a 4chin or archive post contains the lines spoken at this point
        # we require a 'THREAD' direction governing the script in general
        # for this to really work, but we still can create the line
        new_line._post = str(direction)
      elif desc == 'VOICE':
        new_line._voice = direction
      elif desc == 'VIDEO':
        new_line._video = direction

    line = re.sub('\([^\s():]+[^()]+\)', '', line)

    matches = r.match(line)
    if matches:
      valid_line = True
      speaker = matches.group('speaker')
      text = matches.group('text')
      print("SPEAKER: " + speaker + ' TEXT: ' + text)
      new_line._speaker = speaker
      new_line._text = text
      
    # see if the line text has any parenthetical directions embedded        
    if valid_line:
      # estimate what our audio file and phoneme files will be
      if not new_line._audio_file:
        new_line._audio_file = new_line.gen_filename(tmp_dir, '.mp3')
      if not new_line._phoneme_file:
        new_line._phoneme_file = new_line.gen_filename(tmp_dir, '.mp3.phonemes.out.txt')


      return new_line
    return None
