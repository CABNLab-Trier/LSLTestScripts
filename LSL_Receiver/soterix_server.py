# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 14:21:24 2026
Server script to transfer remote commands to
Soterix MxN stimulator.  
@author: kastenf
"""

import pylsl

# setup input stream
streams = []

while not streams:
    streams = pylsl.resolve_byprop('type', 'Markers', timeout=10)
print(f"Found streams: {streams}")

inlet = pylsl.StreamInlet(streams[0])

# setup output stream
info = pylsl.StreamInfo("HD-SC_Markers", "Markers", 1, 0, 'string')
outlet = pylsl.StreamOutlet(info)

while True:
    
    ## inlet waiting for incomming sample
    inp_cmd, timestamp = inlet.pull_sample()
    
    # if a command is received hand over to outlet
    outlet.push_sample(inp_cmd)
    
    
