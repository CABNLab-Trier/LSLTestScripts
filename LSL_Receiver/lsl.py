from random import sample

import pylsl
from pylsl.lib import cf_string

pylsl.set_config_filename("cfg/lsl_api.cfg")

streams = []
while not streams:
    print("Looking for streams...")
    streams = pylsl.resolve_byprop('name', 'Triggers', timeout=2.)
print(f"Found streams: {streams}")

stream = pylsl.StreamInlet(streams[0])

mxn_info = pylsl.StreamInfo(
    name="HD-SC_Markers",
    type="Markers",
    channel_count=1,
    nominal_srate=0,
    channel_format=cf_string,
    source_id="973D9621-CE2A-499E-AD33-1CA9D07450F5"
)
mxn_output = pylsl.StreamOutlet(mxn_info)

while True:
    sample, timestamp = stream.pull_sample()
    print(f"Received sample '{sample}' at {timestamp}")
    mxn_output.push_sample(sample)