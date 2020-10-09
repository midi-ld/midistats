# /usr/bin/env python
from mido import MidiFile
import sys
import os.path

dataset_stats = {}
dataset_stats['files'] = 0
for i in range(128):
    dataset_stats['note_' + str(i)] = 0
for i in range(128):
    dataset_stats['program_' + str(i)] = 0


def process_midi(path, file):
    # file_stats = {'filename' : os.path.join(path, file)}
    try:
        with MidiFile(os.path.join(path, file)) as mid:
            for i, track in enumerate(mid.tracks):
                for msg in track:
                    # General message counts
                    # if msg.type not in file_stats:
                    #     file_stats[msg.type] = 1
                    # else:
                    #     file_stats[msg.type] += 1

                    # pitches
                    if msg.type == 'note_on':
                        dataset_stats['note_' + str(msg.note)] += 1
                        #print('note_on: {}'.format(msg.note))
                    # instruments
                    if msg.type == 'program_change':
                        dataset_stats['program_' + str(msg.program)] += 1
                        #print('program_change: {}'.format(msg.program))
                    # tempo
                    if msg.type == 'set_tempo':
                        if str('tempo_' + str(msg.tempo)) not in dataset_stats:
                                dataset_stats['tempo_' + str(msg.tempo)] = 0
                        dataset_stats['tempo_' + str(msg.tempo)] += 1
                        # print('set_tempo: {}'.format(msg.tempo))
                    # time signature
                    if msg.type == 'time_signature':
                        # print('time_signature: {}'.format(str(msg.numerator) + '/' + str(msg.denominator)))
                        if str('time_signature_' + str(msg.numerator) + '/' + str(msg.denominator)) not in dataset_stats:
                            dataset_stats['time_signature_' + str(msg.numerator) + '/' + str(msg.denominator)] = 0
                        dataset_stats['time_signature_' + str(msg.numerator) + '/' + str(msg.denominator)] += 1
    except (OSError, EOFError, KeyError) as e:
        print("Error in MIDI file: {}".format(e))
        pass


    # Output
    # print(','.join(str(v) for v in file_stats.values()))

for path, directories, files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith('.mid'):
            process_midi(path, file)
            dataset_stats['files'] += 1

print(dataset_stats)
exit(0)
