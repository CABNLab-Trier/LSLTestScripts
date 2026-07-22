import pylsl
from pylsl.lib import cf_string
import time
import json

pylsl.set_config_filename("cfg/lsl_api.cfg")

look_for_device_channel = False

streams = []
while not streams:
    print("Looking for trigger stream...")
    streams = pylsl.resolve_byprop('name', 'Triggers', timeout=2.)
print(f"Found streams: {streams}")

trigger_stream = pylsl.StreamInlet(streams[0])

mxn_info = pylsl.StreamInfo(
    name="HD-SC_Markers",
    type="Markers",
    channel_count=1,
    nominal_srate=0,
    channel_format=cf_string,
    source_id="973D9621-CE2A-499E-AD33-1CA9D07450F5"
)
mxn_output = pylsl.StreamOutlet(mxn_info)

if look_for_device_channel:
    streams = []
    while not streams:
        print("Looking for device stream...")
        streams = pylsl.resolve_byprop('name', 'HD-SC_Stimulation', timeout=2.)
    print(f"Found streams: {streams}")

    stim_stream = pylsl.StreamInlet(streams[0])
else:
    stim_stream = None

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
        "Action": 0,
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
        "Action": 0,
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
        "Action": 0,
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

def send_messages(msgs, timeout=pylsl.FOREVER):
    for msg in msgs:
        print(f'Sending message: {msg}')
        mxn_output.push_sample([json.dumps(msg)])
        if stim_stream is None:
            time.sleep(timeout)
        else:
            response, ts = stim_stream.pull_sample(timeout=timeout)
            if response is not None:
               print(f'Received response: {response}')
            else:
               print(f'Received no response')

while True:
    msg, timestamp = trigger_stream.pull_sample()
    msg = msg[0]
    print(f"Received sample '{msg}' at {timestamp}")
    if msg == "stim 1":
        send_messages(stim_1(),2)
        send_messages(start_stim(),2)
    elif msg == "stim 2":
        print("Stim 2 not implemented yet")
    else:
        print(f"Received unknown message '{msg}'")
