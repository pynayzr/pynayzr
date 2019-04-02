# -*- coding: utf-8 -*-
#
# Cropper: crop news frame into block
#
# How to add a new cropper
#   1. Add new cropper.py file in cropper folder
#   2. Add new absolute import under last import
#   3. Add correspond news media into support_news dict
#

from pynayzr.cropper import ftv
from pynayzr.cropper import sets
from pynayzr.cropper import ttv
from pynayzr.cropper import cti
from pynayzr.cropper import tvbs
from pynayzr.cropper import ebc
from pynayzr.cropper import pts
from pynayzr.cropper import cts
from pynayzr.cropper import ctv

support_news = {
    'ftv': ftv.FTVCropper,
    'set': sets.SETSCropper,
    'ttv': ttv.TTVCropper,
    'cti': cti.CTICropper,
    'tvbs': tvbs.TVBSCropper,
    'ebc': ebc.EBCCropper,
    'pts': pts.PTSCropper,
    'cts': cts.CTSCropper,
    'ctv': ctv.CTVCropper
}
