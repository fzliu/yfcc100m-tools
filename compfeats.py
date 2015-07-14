"""
compfeats.py: Compute convolutional activation features for YFCC100M.
Requires caffe and pycaffe (see caffe.berkeleyvision.org for more info).
Model is based of Alex Krizhevsky's ILSVRC'12 winning model (AlexNet).

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

import argparse
import os
import sys

# library imports
import caffe
import numpy as np
from sklearn.svm import LinearSVC

# local imports
from parse100m import YFCC100MParser

CAFFE_ROOT = os.path.join("..", "caffe")
MODEL_PATH = os.path.join(CAFFE_ROOT, 
                          "models", 
                          "bvlc_reference_caffenet", 
                          "bvlc_reference_caffenet.caffemodel")
MODEL_DEF_PATH = os.path.join(CAFFE_ROOT,
                              "models", 
                              "bvlc_reference_caffenet", 
                              "deploy.prototxt")
MODEL_MEAN_PATH = os.path.join(CAFFE_ROOT,
                               "python",
                               "caffe",
                               "imagenet",
                               "ilsvrc_2012_mean.npy")

# argparse
parser = argparse.ArgumentParser(description="Compute YFCC100M deep features.",
                                 usage="compfeats.py")
parser.add_argument("-o", "--output", required=True, help="output filename")
parser.add_argument("-t", "--test", action="store_true", help="run test")

# output filename
out_path = ""

# caffe net
classifier = caffe.Classifier(MODEL_DEF_PATH, MODEL_PATH,
                              mean=np.load(MODEL_MEAN_PATH).mean(1).mean(1),
                              channel_swap=(2, 1, 0),
                              raw_scale=255,
                              image_dims=(256, 256))


def compute_activation_features(img):
    """
        Compute deep convolutional activation features for an image.
    """
    global classifier

    classifier.predict([img])
    return classifier.blobs["fc7"].data


def _dumpDeepFeatsFn(data):
    """
        Callback function for dumping AlexNet features.
    """
    global out_path

    # compute the features, with camera type
    with open(out_path, "a") as f:
        feats = compute_activation_features(data["image"])
        line = "{0}\t{1}\t{2}".format(data["photo_id"], data["camera_type"], feats)
        f.write(line + "\n")


# dump the photo_id, features, and camera_type 
if __name__ == "__main__":
    from skimage.data import lena

    args = parser.parse_args()

    # test caffe
    if args.test:
        feats = compute_activation_features(lena())
        print("Activation features for lena image:\n{0}".format(feats))
        sys.exit(0)

    # overwrite the output file
    out_path = args.output
    with open(out_path, "w") as f:
        pass

    np.set_printoptions(threshold='nan')
    parse_100m = YFCC100MParser(_dumpDeepFeatsFn)
    parse_100m.parse(prob=0.001)

