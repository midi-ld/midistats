# /usr/bin/env python
from mido import MidiFile
import sys

in_file = sys.argv[1]

file_stats = {'filename' : in_file}
with MidiFile(in_file) as mid:
    print("Tracks: {}".format(len(mid.tracks)))
    for i, track in enumerate(mid.tracks):
        track_stats = {'track_nr' : i, 'track_label' : track.name}
        # track_stats = {}
        for msg in track:
            if msg.type not in track_stats:
                track_stats[msg.type] = 1
            else:
                track_stats[msg.type] += 1
            if msg.type not in file_stats:
                file_stats[msg.type] = 1
            else:
                file_stats[msg.type] += 1
        print(track_stats)
        print(file_stats)

# print all file stats in one CSV row
print(','.join(str(v) for v in file_stats.values()))


exit(0)
