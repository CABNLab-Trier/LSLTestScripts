from random import sample

import pylsl

pylsl.set_config_filename("cfg/lsl_api.cfg")

streams = []
while not streams:
    print("Looking for streams...")
    streams = pylsl.resolve_streams(2.)
print(f"Found streams: {streams}")

stream = pylsl.StreamInlet(streams[0])

while True:
    sample, timestamp = stream.pull_sample()
    print(f"Received sample '{sample}' at {timestamp}")