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
    i = 1
    with open(self._filepath) as f:
      for line in f:
        i = Line.parse(self, i, line, asset_dir)
      self._current = 0
      
  def add_line(self, line):
    self._lines.append(line)
  
  def __iter__(self):
    self._current = 0
    return self
    
  def next(self): # Python 3: def __next__(self)
    if self._current >= len(self._lines):
      raise StopIteration
    else:
      self._current += 1
    return self._lines[self._current-1]


def do_tts(script, out_dir):
	for line in script:
		line.gen_audio_file(out_dir)

def do_phonemes(script, out_dir):
	for line in script:
		line.gen_phoneme_file(out_dir)


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

  #if args.posts:
  #  get_posts(script, out_dir=args.outdir)

  if args.tts:
    do_tts(script, out_dir=args.outdir)

  if args.phonemes:
    do_phonemes(script, out_dir=args.outdir)

  #if args.videos:
  #  get_video_info(script, out_dir=args.outdir)

if __name__ == '__main__':
  main()

