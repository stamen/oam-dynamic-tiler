#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import json
import re
import sys
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: {} <warped VRT>".format(os.path.basename(sys.argv[0])), file=sys.stderr)
        exit(1)

    input = sys.argv[1]
    doc = ET.parse(sys.argv[1])
    root = doc.getroot()
    # TODO treat remaining VRTRasterBand's ColorInterp as 'Alpha' (vs. Red)
    [root.remove(x) for x in root.findall("VRTRasterBand")[1:]]
    band_list = doc.find(".//GDALWarpOptions/BandList")
    [band_list.remove(x) for x in band_list.findall("BandMapping")[1:]]
    root.findall("SourceDataset")
    source_dataset = doc.find("./GDALWarpOptions/SourceDataset")
    source_dataset.text = re.sub(".tif$", ".tif.msk", source_dataset.text)
    resample_alg = doc.find("./GDALWarpOptions/ResampleAlg")
    resample_alg.text = "NearestNeighbour"

    ET.dump(doc)