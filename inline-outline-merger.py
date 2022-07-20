#!/opt/homebrew/bin/python3

import os
import sys


class Transcript:
  def __init__(self, timestamp, data, type):
    self.timestamp = float(timestamp[1:-1])
    self.data = data
    self.type = type


def parse_transcripts(lines, transcripts, type):
  timestamp = ''
  data = []
  for line in lines:
    if line.startswith('[') and line.endswith(']'):
      if timestamp and data:
        transcripts.append(Transcript(timestamp, data, type))
      data = []
      timestamp = line
    else:
      data.append(line)
  if timestamp and data:
    transcripts.append(Transcript(timestamp, data, type))


folder = sys.argv[1]
INLINE_SUFFIX = "_inLine.txt"
OUTLINE_SUFFIX = "_outLine.txt"

inline_files = [x[:-len(INLINE_SUFFIX)]
                for x in os.listdir(folder) if INLINE_SUFFIX in x]
outline_files = [x[:-len(OUTLINE_SUFFIX)]
                 for x in os.listdir(folder) if OUTLINE_SUFFIX in x]

inline_files.sort()
outline_files.sort()

for inline in inline_files:
  if inline not in outline_files:
    continue
  # found a valid pair of inline/outline
  print(inline)
  inline_lines = [x.strip() for x in open(os.path.join(
      folder, inline + INLINE_SUFFIX), 'r').readlines()]
  outline_lines = [x.strip() for x in open(os.path.join(
      folder, inline + OUTLINE_SUFFIX), 'r').readlines()]
  transcripts = []
  parse_transcripts(inline_lines, transcripts, 'inLine')
  parse_transcripts(outline_lines, transcripts, 'outLine')

  transcripts.sort(key=lambda x: x.timestamp)
  for transcript in transcripts:
    row = '{}\t{}\t{}'.format(
        transcript.type, transcript.timestamp, '\t'.join(transcript.data))
    print(row)
  print('\n\n\n')
