import time
import sys
sys.path.insert(0, '..')
from python_artnet import python_artnet as Artnet
import DDPDevice
import numpy as np

debug = False

ddpIp = "192.168.7.34"

# What DMX channels we want to listen to
startchannel = 1

### ArtNet Config ###
artnetBindIp = "0.0.0.0"
artnetUniverse = 0

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(artnetBindIp, DEBUG=debug)

## DDP setup
ddp = DDPDevice.DDPDevice(ddpIp)

while True:
    try:
        # First get the latest Art-Net data
        artNetBuffer = artNet.readBuffer()
        # And make sure we actually got something
        if artNetBuffer is not None:
            # Get the packet from the buffer for the specific universe
            artNetPacket = artNetBuffer[artnetUniverse]
            # And make sure the packet has some data
            if artNetPacket.data is not None:
                # Stores the packet data array
                dmxPacket = artNetPacket.data
                sequenceNo = artNetPacket.sequence
                
                # Then print out the data from each channel
                print("Sequence no: ", sequenceNo)
                print("Sent data: ", end="")

                leds = np.array(dmxPacket[startchannel-1:startchannel+2])
                print(leds)
                
                ddp.send_to_queue(leds)
        
         #Default refresh rate ~ 44 Hz
        time.sleep(0.022)
        
    except KeyboardInterrupt:
        break

# Close the various connections cleanly so nothing explodes :)
artNet.close()
sys.exit()