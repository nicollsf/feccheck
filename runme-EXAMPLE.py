from fec_check import FECCheck
from crs_parser import parsecrsinput, apply_update
import numpy as np
import os
from pathlib import Path

dirname = '.'
# Point this to your manual updates file (or use the provided example)
ufname = os.path.join(dirname, 'fec_updates-EXAMPLE.xlsx')

# Put the name of your CRS CSV data dump here
crsnames = [
    'YOUR_CRS_DATA_HERE.csv'
]

if __name__ == '__main__':
    for fname in crsnames:
        crsfname = os.path.join(dirname, fname)
        oxlsfname = os.path.join(dirname, Path(crsfname).stem + '_output.xlsx')
                
        stinfob, cinfo = parsecrsinput(crsfname, np.inf)
        # Uncomment the line below to apply manual overrides from the ufname Excel file
        # stinfo = apply_update(stinfob, ufname)
        stinfo = stinfob
                
        feco = FECCheck(stinfo)
        feco.process(oxlsfname)