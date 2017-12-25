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
import ntpath

from line import Line

class Script(object):
  def __init__(self, filepath, asset_dir='./tmp'):
    self._filepath = filepath
    self._lines = []
    self._thread = None

    # parse any string for "stage directions"
    pd = re.compile(r'^\((?P<desc>[^\s():]+):(?P<direction>[^()]+)?\)')

    with open(self._filepath) as f:
      i = 1 # don't enumerate so we can increment by SPEAKER
      for line in f:
        # eliminate comments
        line = line.split('#')[0].strip()
       
        d = pd.match(line)
        if d:
          desc = d.group('desc')
          direction = None
          if 'direction' in d.groupdict():
            direction = d.group('direction').strip()
          print("Single Direction: {desc} --> {direction}".format(desc=desc, direction=direction))

          if desc == 'THREAD':
            # an audio file contains the lines spoken at this point
            self._thread = str(direction)
        
          continue

        l = Line.parse(i, line, asset_dir)
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


def do_tts(script, out_dir='./tmp/',
            tool='gtts-cli',
            args='{tool} -o {outfile} {text}',
            gen_phonemes=False):
  """
  Generate audio off a script
  ARGS:
  script: parsed script object (see above)
  tool: path to tts tool to use (defaults to gtts-cli)

  """
  print("Generating tts audio files off input script")
  for line in script:
    outfile = line._audio_file or line.gen_filename(out_dir, '.mp3')
    
    # the audio file for this line might already exist
    if os.path.isfile(outfile):
      print("Audio file {file} already exists. Not generating.".format(file=line._audio_file))
      continue
    text = ''
    if line._post:
      # TODO: remove quotes, urls etc from post text
      infile = line.gen_filename(out_dir, '.txt')
      s = 'gtts-cli -o {outfile} -f {file}'.format(outfile=outfile, file=infile)
      print('Making system call: "%s"' % (s))
      os.system(s)
      # it's possible that for posts, there might be no text 
      # if we didn't generate a file, fail

    elif line._speaker:
      text = pipes.quote(line._text)
      s = args.format(tool=tool, outfile=outfile, text=text)
      print('Making system call: "%s"' % (s))
      os.system(s)
      # if we didn't generate a file, fail
      if not os.path.isfile(outfile):
        raise IOError("Could not generate file: %s" % (outfile))
      print('Wrote file %s' % (outfile))

def do_phonemes(script, out_dir='./tmp/'):
  """
  Generate phoneme files off input audio files
  ARGS:
    filepath: path to input audio file
    out_path: output directory for generated phoeneme file.
  """
  for line in script:
    filepath = line._audio_file or line.gen_filename(out_dir, '.mp3') 
    cmd = 'tools/phonemes.sh {filepath}'.format(filepath=filepath)
    print("Generating phonemes file for input audio file " + filepath)
    os.system(cmd)


def get_posts(script, out_dir='./tmp/'):
  # script has to specify a THREAD to do anything
  if not script._thread:
    print("Script did not specify a THREAD for post sources.")
    return

  thread = script._thread
  for line in script:
    if line._post:
      # as it's expensive to generate post images, first check if it's already there
      image_filename = line.gen_filename(out_dir, '.png')
      text_filename = line.gen_filename(out_dir, '.txt')
      if(os.path.isfile(image_filename) and os.path.isfile(text_filename)):
        print("skipping {image} and {txt} because they already exist.".format(image=image_filename, txt=text_filename))
        continue
      cmd = 'phantomjs tools/get_post.js \'{thread}\' \'{post}\' {out_dir}'.format(thread=thread, post=line._post, out_dir=out_dir)
      print("Running os.system command: " + cmd)
      os.system(cmd)
      # TODO: check files now exist or throw

def get_video_info(script, out_dir='./tmp/'):
  """
  Generate video (and audio) info files off input video files
  ARGS:
    filepath: path to input audio file
    out_path: output directory for generated phoeneme file.
  """
  for line in script:
    filename = line._video or line._audio_file
    if filename:
      print("**** " + filename)
      outfile = line.gen_filename(out_dir, '.runtime.txt')
      cmd = 'ffprobe -i "{filename}" -show_entries format=duration -v quiet -of csv="p=0" > {outfile}'.format(filename=filename, outfile=outfile)
      print("Generating video length file for input media file " + filename)
      print(cmd)
      os.system(cmd)


"""
  Main provides a tool that generates tts and phoneme files from a script,
  leveraging the classes above, but the classes above should be used
  to traverse scripts in other .py files.
"""

def main():
  parser = argparse.ArgumentParser(description='Parse simple animation script.')
  parser.add_argument('infile', action="store")
  parser.add_argument('--tts', action="store_true", default=False)
  parser.add_argument('--phonemes', action="store_true", default=False)
  parser.add_argument('--videos', action="store_true", default=False)
  parser.add_argument('-o', '--outdir', type=str, default='./tmp/')
  parser.add_argument('--posts', action="store_true", default=False, help="create snapshots of post numbers in script.")
  args = parser.parse_args()

  print("Generating supporting assets in dir: {dir}".format(dir=args.outdir))

  infile = args.infile
  if not os.path.isfile(infile):
    print("File: " + infile + " not found.")
    return -1

  script = Script(infile, asset_dir=args.outdir)
  for line in script:
    print("Line: " + str(line._index) + " speaker: " + line._speaker + " text: " + line._text)

  if args.posts:
    get_posts(script, out_dir=args.outdir)

  if args.tts:
    do_tts(script, out_dir=args.outdir)

  if args.phonemes:
    do_phonemes(script, out_dir=args.outdir)

  if args.videos:
    get_video_info(script, out_dir=args.outdir)

if __name__ == '__main__':
  main()






