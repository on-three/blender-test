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

class Line(object):
  def __init__(self, speaker, text, index=0):
    self._speaker = speaker
    self._text = text
    self._index = index

  @staticmethod
  def parse(index, line):
    r = re.compile(r'^(?P<speaker>[^\s:]+):( )?(?P<text>.+)')
    matches = r.match(line)
    if matches:
      speaker = matches.group('speaker')
      text = matches.group('text')
      print("SPEAKER: " + speaker + ' TEXT: ' + text)
      return Line(speaker, text, index=index)
    return None
         

class Script(object):
  def __init__(self, filepath):
    self._filepath = filepath
    self._lines = []
    with open(self._filepath) as f:
      for i, line in enumerate(f):
        #strip leading and trailing whitespace
        line = line.strip()
        # eliminate comments
        if line.startswith('#'):
          continue
        l = Line.parse(i, line)
        if l:
          self._lines.append(l)
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
  Main provides a tool that generates tts and phoneme files from a script,
  leveraging the classes above, but the classes above should be used
  to traverse scripts in other .py files.
"""

def main():
  parser = argparse.ArgumentParser(description='Parse simple animation script.')
  parser.add_argument('infile', action="store")
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

if __name__ == '__main__':
  main()






