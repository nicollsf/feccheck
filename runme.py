from fec_check import FECCheck
from crs_parser import parsecrsinput, apply_update
import numpy as np
import os
from pathlib import Path

dirname = '.'
#ufname = os.path.join(dirname, 'fec2026_updates.xlsx')
crsnames = [
    'EEE CSV 2 March 2026.csv'
]

if __name__ == '__main__':
    
  for fname in crsnames:
    crsfname = os.path.join(dirname, fname)
    oxlsfname = os.path.join(dirname, Path(crsfname).stem + '_FNlatest.xlsx')
            
    stinfob, cinfo = parsecrsinput(crsfname, np.inf)
    #stinfo = apply_update(stinfob, ufname)
    stinfo = stinfob
            
    feco = FECCheck(stinfo)
    feco.process(oxlsfname)
