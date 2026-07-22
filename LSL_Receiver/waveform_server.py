import pylsl
from pylsl.lib import cf_string
import time
import json

pylsl.set_config_filename("cfg/amyTI.cfg")

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

def stim_1():
    yield {# general stimulation parameters
        "Action": 7,
        "RampUp": 10,
        "Duration": 1200,
        "WaveformType":"TACS",
        "Intensity": 1.1,
    }
    yield {# add channel
        "Action": 0,
        "ChannelNumber": 1
    }
    yield {# adjust frequency
        "Action": 7,
        "ChannelNumber": 1,
        "Frequency": 2000
    }
    yield {  # general stimulation parameters
        "Action": 7,
        "RampUp": 10,
        "Duration": 1200,
        "WaveformType": "TACS",
        "Intensity": -1.1,
    }
    yield {# add channel
        "Action": 2,
        "ChannelNumber": 2,
    }
    yield {# adjust frequency
        "Action": 7,
        "ChannelNumber": 2,
        "Frequency": 2000
    }
    yield {  # general stimulation parameters
        "Action": 7,
        "RampUp": 10,
        "Duration": 1200,
        "WaveformType": "TACS",
        "Intensity": 0.9,
    }
    yield {  # add channel
        "Action": 2,
        "ChannelNumber": 3,
    }
    yield {  # adjust frequency
        "Action": 7,
        "ChannelNumber": 3,
        "Frequency": 2070
    }
    yield {  # general stimulation parameters
        "Action": 7,
        "RampUp": 10,
        "Duration": 1200,
        "WaveformType": "TACS",
        "Intensity": -0.9,
    }
    yield {  # add channel
        "Action": 2,
        "ChannelNumber": 4,
    }
    yield {  # adjust frequency
        "Action": 7,
        "ChannelNumber": 4,
        "Frequency": 2070
    }

def start_stim():
    yield {
        "Action": 3,
    }
    yield {
        "Action": 4,
    }

def send_messages(msgs, timeout= 2):
    for msg in msgs:
        print(f'Sending message: {msg}')
        mxn_output.push_sample([json.dumps(msg)])
        time.sleep(timeout)

while True:
    msg, timestamp = stream.pull_sample()
    print(f"Received sample '{msg}' at {timestamp}")
    if msg == "stim 1":
        send_messages(stim_1(),1)
        send_messages(start_stim(),2)
    elif msg == "stim 2":
        print("Stim 2 not implemented yet")
    else:
        print(f"Received unknown message '{msg}'")
