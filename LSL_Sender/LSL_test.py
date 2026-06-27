import pylsl
from pylsl.lib import cf_string
import time

pylsl.set_config_filename("cfg/amyTI.cfg")

info = pylsl.StreamInfo(
    name="Triggers",
    type="Markers",
    channel_count= 1,
    nominal_srate =0,
    channel_format = cf_string,
    source_id = "desktop_triggers"
)
channel = pylsl.StreamOutlet(info)
while True:
    channel.push_sample(["hello from the other side... i must have pinged a thousand times"])
    time.sleep(2)
