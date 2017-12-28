#!/usr/bin/env python
"""
  Basic script to scrape www.naturalreaders.com for decent TTS voices
  Currently relies on a static API key so I don't know how well this will work.

"""
import argparse
import urllib
import requests

#wget "https://api.naturalreaders.com/v4/tts/macspeak?apikey=b98x9xlfs54ws4k0wc0o8g4gwc0w8ss&src=pw&r=0&s=1&t=I%20am%20el%20grande%20padre." -O el.grande.padre.mp3


#src="pw"
#reader="0"
#speed="1"

#text="I am el grande padre."
#text=urllib.quote(text, safe='')



# after https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(url, filename):
  #local_filename = url.split('/')[-1]
  local_filename = filename
  # NOTE the stream=True parameter
  r = requests.get(url, stream=True)
  with open(local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk: # filter out keep-alive new chunks
        f.write(chunk)
        #f.flush() commented by recommendation from J.F.Sebastian
  return local_filename


def do_tts(text, outfile, voice="0", speed="1"):
  apikey="b98x9xlfs54ws4k0wc0o8g4gwc0w8ss"
  src="pw"
  text = urllib.quote(text, safe='')
  url = "https://api.naturalreaders.com/v4/tts/macspeak?apikey={apikey}&src={src}&r={reader}&s={speed}&t={text}".format(apikey=apikey, src=src, reader=voice, speed=speed, text=text)
  download_file(url, outfile)

def main():
  parser = argparse.ArgumentParser(description='Scrape naturalreaders for TTS mp3 files.')
  parser.add_argument('text', action="store")
  parser.add_argument('-v', '--voice', type=str, default="0")
  parser.add_argument('-s','--speed', type=str, default="1")
  parser.add_argument('-o', '--outfile', type=str, default='output.mp3')
  args = parser.parse_args()

  print("Doing TTS for input string: '{text}'".format(text=args.text))
  print("Generating output file: {outfile}".format(outfile=args.outfile))
  
  do_tts(args.text, args.outfile, voice=args.voice, speed=args.speed)
  

if __name__ == '__main__':
  main()

