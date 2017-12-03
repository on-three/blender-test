#!/usr/bin/env python
"""
FILE: script.py
DESC: parse a simple input script. Also
provides some methods to generate tts and phoneme
files.

"""
import argparse
import os.path
import re
import pipes

class Line(object):
  # infer phoneme files via filename
  PHONEME_FILE_SUFFIX = '.phonemes.out.txt'

  def __init__(self, speaker, text, index=0):
    self._speaker = speaker
    self._text = text
    self._index = index
    self._audio_file = None
    self._phoneme_file = None
    
    # estimate what our audio and phoneme file are
    self._audio_file = './audio/{index}.{speaker}.mp3'.format(index=str(self._index), speaker=self._speaker)
    self._phoneme_file = self._audio_file + Line.PHONEME_FILE_SUFFIX

  @staticmethod
  def parse(index, line):
    # parse indivdual lines of dialog for speaker and text
    r = re.compile(r'^(?P<speaker>[^\s:]+):( )?(?P<text>.+)')
    # parse any string for "stage directions"
    pd = re.compile(r'\((?P<desc>[^\s():]+):(?P<direction>[^()]+)\)')
    
    matches = r.match(line)
    if matches:
      speaker = matches.group('speaker')
      text = matches.group('text')
      print("SPEAKER: " + speaker + ' TEXT: ' + text)

      new_line = Line(speaker, text, index=index)
      
      # see if the line text has any parenthetical directions embedded
      for d in pd.finditer(text):
        desc = d.group('desc')
        direction = None
        if 'direction' in d.groupdict():
          direction = d.group('direction').strip()
        print("Direction: {desc} --> {direction}".format(desc=desc, direction=direction))

        if desc == 'AUDIO':
          new_line._audio_file = str(direction)
          new_line._phoneme_file = new_line._audio_file + Line.PHONEME_FILE_SUFFIX
      
      return new_line

    return None
         

class Script(object):
  def __init__(self, filepath):
    self._filepath = filepath
    self._lines = []
    with open(self._filepath) as f:
      i = 1 # don't enumerate so we can increment by SPEAKER
      for line in f:
        # eliminate comments
        line = line.split('#')[0].strip()
        
        l = Line.parse(i, line)
        if l:
          self._lines.append(l)
          i = i + 1
        self._current = 0

  def __iter__(self):
    self._current = 0
    return self

  def next(self): # Python 3: def __next__(self)
    if self._current >= len(self._lines):
      raise StopIteration
    else:
      self._current += 1
    return self._lines[self._current-1]


"""
Generate audio off a script
ARGS:
script: parsed script object (see above)
tool: path to tts tool to use (defaults to gtts-cli)

"""
def do_tts(script, out_path='./audio/', tool='gtts-cli', args='{tool} -o {outfile} {text}'):
  print("Generating tts audio files off input script")
  for line in script:
    outfile = out_path + str(line._index) + '.' + line._speaker + '.mp3'
    l = pipes.quote(line._text)
    s = args.format(tool=tool, outfile=outfile, text=l)
    print('Making system call: "%s"' % (s))
    os.system(s)
    # if we didn't generate a file, fail
    if not os.path.isfile(outfile):
      raise IOError("Could not generate file: %s" % (outfile))
    print('Wrote file %s' % (outfile))


"""
  Main provides a tool that generates tts and phoneme files from a script,
  leveraging the classes above, but the classes above should be used
  to traverse scripts in other .py files.
"""

def main():
  parser = argparse.ArgumentParser(description='Parse simple animation script.')
  parser.add_argument('infile', action="store")
  parser.add_argument('-tts', action="store_true", default=False)
  parser.add_argument('-o', '--outdir', type=str, default='./audio/')
  #parser.add_argument('-a', action="store_true", default=False)
  #parser.add_argument('-b', action="store", dest="b")
  #parser.add_argument('-c', action="store", dest="c", type=int)
  args = parser.parse_args()
  
  infile = args.infile
  if not os.path.isfile(infile):
    print("File: " + infile + " not found.")
    return -1

  script = Script(infile)
  for line in script:
    print("Line: " + str(line._index) + " speaker: " + line._speaker + " text: " + line._text)

  if args.tts:
    do_tts(script, out_path=args.outdir)

if __name__ == '__main__':
  main()






