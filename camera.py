"""
cameratype.py: Create camera type counts for YFCC100M.

author: Frank Liu - frank.zijie@gmail.com
last modified: 05/30/2015

Copyright (c) 2015, Frank Liu
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Frank Liu (fzliu) nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Frank Liu (fzliu) BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from collections import defaultdict

# local imports
from parse100m import YFCC100MParser

MODELS_OUT_FNAME = "camera_types.txt"
MAKERS_OUT_FNAME = "camera_makers.txt"

# camera makers
DEFAULT_MAKERS = ["canon",
                  "nikon",
                  "sony",
                  "panasonic",
                  "apple",
                  "olympus"]

camera_types = defaultdict(int)
camera_makers = defaultdict(int)

def _countCameraTypesFn(data):
    """
        Callback function to count camera types.
    """
    global camera_types, camera_makers

    # udpate camera types
    ct = data["camera_type"]
    camera_types[ct] += 1

    # update camera makers
    maker = ct.split("+")[0]
    if maker in DEFAULT_MAKERS:
        camera_makers[maker] += 1
    else:
        camera_makers[""] += 1

if __name__ == "__main__":

    parser = YFCC100MParser(_countCameraTypesFn)
    parser.parse(do_get_imgs=False)

    # save camera type counts to a file
    with open(MODELS_OUT_FNAME, "w") as f:
        for k, v in sorted(camera_types.items(), key=lambda x: x[1], reverse=True):
            if v >= 100:
                f.write("{0}\t{1}\n".format(k, v))

    # save the camera manufacturers to a file
    with open(MAKERS_OUT_FNAME, "w") as f:
        for k, v in sorted(camera_makers.items(), key=lambda x: x[1], reverse=True):
            if k in DEFAULT_MAKERS:
                f.write("{0}\t{1}\n".format(k, v))
