#!/bin/bash
sdptool add --channel=3 SP
rfcomm connect /dev/rfcomm0 B8:27:EB:D3:BF:86 3

