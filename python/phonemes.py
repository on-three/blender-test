"""
Example input phonemes file (not optimized)

SIL IH F AE NG D IH EY D EH AA F UH EY DH AA NG HH AH SIL
SIL 0.000 0.030 1.000000
IH 0.040 0.130 1.000000
F 0.140 0.180 1.000000
AE 0.190 0.310 1.000000
NG 0.320 0.340 1.000000
D 0.350 0.430 1.000000
IH 0.440 0.480 1.000000
EY 0.490 0.560 1.000000
D 0.570 0.620 1.000000
EH 0.630 0.730 1.000000
AA 0.740 1.030 1.000000
F 1.040 1.120 1.000000
UH 1.130 1.180 1.000000
EY 1.190 1.350 1.000000
DH 1.360 1.400 1.000000
AA 1.410 1.690 1.000000
NG 1.700 1.760 1.000000
HH 1.770 1.810 1.000000
AH 1.820 1.860 1.000000
SIL 1.870 2.090 1.000000

standard animation mouth positions are:
A
O
E
W,R
T,S
L,N
U,Q
M,B,P
F,V
"""

import re

class Phoneme(object):
  SIL = 0 # same as m.b.p
  A = 1
  I = 1
  O = 2
  E = 3
  W = 4
  R = 4
  T = 5
  S = 5
  L = 6
  N = 6
  U = 7
  Q = 7
  M = 8
  B = 8
  P = 8
  F = 9
  V = 9
  def __init__(self, sound, start_frame, end_frame, text="", speaker=None):
    self._sound = sound
    self._start_frame = start_frame
    self._end_frame = end_frame
    self._text = text
    self._speaker = speaker
    print("created phoneme: " + str(self._sound) + "  start: " + str(self._start_frame) + " end: " + str(self._end_frame))

  def sound(self):
    return self._sound

  def text(self):
    return self._text

#SIL K F ER Y UW N SIL
#SIL IH F AE NG D IH EY D EH AA F UH EY DH AA NG HH AH SIL
#SIL IH L IH N B IY IH K Z G R UW R EY D HH UH EY UH D B OW SIL
#SIL Y R UH G EY N G AE AA NG SIL

DEFAULT_PHONEME_MAP = {
  'SIL' : Phoneme.SIL,
  'AE'  : Phoneme.A,
  'IH'  : Phoneme.E,
  'TH'  : Phoneme.T,
  'T'   : Phoneme.T,
  'AE'  : Phoneme.A,
  'NG'  : Phoneme.N,
  'D'   : Phoneme.T,
  'EH'  : Phoneme.E,
  'AA'  : Phoneme.A,
  'F'   : Phoneme.F,
  'UH'  : Phoneme.U,
  'EY'  : Phoneme.E,
  'DH'  : Phoneme.T,
  'HH'  : Phoneme.E, # ???
  'AH'  : Phoneme.A,
  'K'   : Phoneme.T,
  'ER'  : Phoneme.R,
  'Y'   : Phoneme.E,
  'UW'  : Phoneme.U,
  'N'   : Phoneme.N,
  'L'   : Phoneme.L,
  'N'   : Phoneme.N,
  'B'   : Phoneme.B,
  'IY'  : Phoneme.I,
  'Z'   : Phoneme.T,
  'G'   : Phoneme.T,
  'R'   : Phoneme.R,
  'HH'  : Phoneme.R,
  'UH'  : Phoneme.U,
  'OW'  : Phoneme.O,
  'NG'  : Phoneme.N,
  'AY'  : Phoneme.A,
  'W'   : Phoneme.W,
  'AO'  : Phoneme.A,
  'P'   : Phoneme.P,
  'AW'  : Phoneme.A,
  'CH'  : Phoneme.T,
  'M'   : Phoneme.M,
  'JH'  : Phoneme.T,
  'S'   : Phoneme.S,
  'V'   : Phoneme.F,
  'SH'  : Phoneme.R,
  'OY'  : Phoneme.E,
  'ZH'  : Phoneme.T,
}

class Tokenizer(object):
  def __init__(self, filename, fps=24, speaker=None, start_frame=0, text="", min_threshold=0.0035, phoneme_map=DEFAULT_PHONEME_MAP):
    self._filename = filename
    self._start_frame = start_frame
    self._min_threshold = min_threshold
    self._phoneme_map = phoneme_map
    self._fps = fps
    self._phonemes = []
    self._speaker = speaker
    self._text = text

    # SIL 0.000 0.030 1.000000
    r = re.compile(r'^(?P<phoneme>\S{1,3}) (?P<start>\d+\.\d+) (?P<end>\d+\.\d+) (?P<prob>\d+\.\d+)', re.IGNORECASE)
    #r = re.compile(r'^(?P<phoneme>\W{1,3}) ', re.IGNORECASE)
    print("Opening phoneme file at: " + filename)
    end = 0
    try:
      with open(self._filename) as f:
        for line in f:
          #print("*** line: " + line)
          matches = r.match(line)
          if matches:
            p = matches.group('phoneme')
            s = float(matches.group('start'))
            e = float(matches.group('end'))
            start = int(s*self._fps) + self._start_frame
            end = int(e*self._fps) + self._start_frame
            # attampt to remove 'noise' by only taking phonemes longer than 0.3 seconds
            # and if there is a previous phoneme, we extend its time to cover this one
            print("Phoneme: " + p + ' start:' + str(s) + " end: " + str(e))
            if (e - s) <= self._min_threshold:
              if len(self._phonemes) > 0:
                self._phonemes[-1]._end_frame = int(e*self._fps)
              continue
            self._phonemes.append(Phoneme(self._phoneme_map[p],
              start, end, self._text, speaker=self._speaker))
      # append a SIL phoneme at the end for a single frame
      self._end_frame = end +1
      self._phonemes.append(Phoneme(Phoneme.SIL, end, self._end_frame, self._text, speaker=self._speaker))
    except:
      print("Exctption thrown while parsing phoneme file.")
  def start_frame(self):
    return self._start_frame

  def speaker(self):
    return self._speaker
    

  def get_sound(self, frame):
    for s in self._phonemes:
      if frame >= s._start_frame and frame <= s._end_frame:
        print("sound returned: " + str(s.sound()))
        return s
    return None

