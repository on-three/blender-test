"""
Example input phonemes file (not optimized)

SIL IH TH AE NG T IH NG D EH AA AA F UH EY IH DH AA NG HH AH SIL
SIL 0.000 0.030 1.000000
IH 0.040 0.130 1.000000
TH 0.140 0.180 1.000000
AE 0.190 0.310 1.000000
NG 0.320 0.350 1.000000
T 0.360 0.430 1.000000
IH 0.440 0.530 1.000000
NG 0.540 0.580 1.000000
D 0.590 0.620 1.000000
EH 0.630 0.730 1.000000
AA 0.740 0.790 1.000000
AA 0.800 1.030 1.000000
F 1.040 1.120 1.000000
UH 1.130 1.180 1.000000
EY 1.190 1.280 1.000000
IH 1.290 1.360 1.000000
DH 1.370 1.400 1.000000
AA 1.410 1.690 1.000000
NG 1.700 1.760 1.000000
HH 1.770 1.810 1.000000
AH 1.820 1.860 1.000000
SIL 1.870 2.090 1.000000
"""

"""
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
  SIL = 0
  A = 1
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
  def __init__(sound, start_frame, stop_frame):
    self._sound = sound
    self._start_frame = start_frame
    self.end_frame = end_frame

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
}

class Tokenizer(object):
  def __init__(self, filename, min_threshold=0.03, phoneme_map=DEFAULT_PHONEME_MAP):
    self._filename = filename
    self._min_threshold = min_threshold
    self._phoneme_map = phoneme_map
    
    # SIL 0.000 0.030 1.000000
    r = re.compile(r'^(?P<phoneme>\S{1,3}) (?P<start>\d+\.\d+) (?P<end>\d+\.\d+) (?P<prob>\d+\.\d+)', re.IGNORECASE)
    #r = re.compile(r'^(?P<phoneme>\W{1,3}) ', re.IGNORECASE)
    with open(self._filename) as f:
      for line in f:
        #print("*** line: " + line)
        matches = r.match(line)
        if matches:
          p = matches.group('phoneme')
          s = matches.group('start')
          e = matches.group('end')
          print("Phoneme: " + p + ' start:' + str(s) + " end: " + str(e))


