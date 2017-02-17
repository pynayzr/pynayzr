# -*- coding: utf-8 -*-

from pynayzr.cropper import ftv
from pynayzr.cropper import sets
from pynayzr.cropper import ttv
from pynayzr.cropper import cti
from pynayzr.cropper import tvbs
from pynayzr.cropper import ebc
from pynayzr.cropper import pts

support_news = {
    'ftv': ftv.FTVCropper,
    'set': sets.SETSCropper,
    'ttv': ttv.TTVCropper,
    'cti': cti.CTICropper,
    'tvbs': tvbs.TVBSCropper,
    'ebc': ebc.EBCCropper,
    'pts': pts.PTSCropper
}
