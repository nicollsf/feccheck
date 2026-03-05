import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Union, Optional

from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter        

from program_defs import PROGRAM_SPECS, COURSE_EQUIVALENCIES
from crs_parser import parsecrsinput

StudentInfo = Dict[str, Union[Any, pd.DataFrame]]
InputType = Union[str, List[StudentInfo]]

EEE_PROGS = {'EB009', 'EB809', 'EB011', 'EB811', 'EB022', 'EB822'}

class FECCheck:
    def __init__(self, data_or_fname: InputType, ufname: Optional[str] = None):
        """
        FECCHECK: Construct FEC check object.
        Initializes the programme definitions and filters student records.
        """
        self.pdefs: Dict[str, Any] = {}
        stinfo: List[Dict[str, Any]] = []

        if isinstance(data_or_fname, list):
            stinfo = data_or_fname
            cinfo = None

        elif isinstance(data_or_fname, str):
            crsfname = data_or_fname
            stinfo, cinfo = parsecrsinput(crsfname, ufname=ufname)

        if not stinfo:
            return
        
        # Filter out students where the srec element is empty
        stinfo = [record for record in stinfo if record.get('srec') is not None and (not isinstance(record.get('srec'), pd.DataFrame) or not record.get('srec').empty)]

        # Filter students whose current academic program (sinfo[3]) is in EEE
        eeflag = [s['sinfo'][3] in EEE_PROGS for s in stinfo]
        stinfo = [stinfo[i] for i, flag in enumerate(eeflag) if flag]
        self.stinfo = stinfo
        if not self.stinfo:  return

        # Programme definitions
        pgs = PROGRAM_SPECS
        for pg in pgs:
            cclist = list(pg.get('core', []))
            for item in pg.get('necore', []):  # add courses from necore
                cclist.extend(item[1:])
            for item in pg.get('cecore', []):  # add courses from cecore
                cclist.extend(item[1:])
            pg['cclist'] = sorted(list(set(cclist)))  # store unique
        cequivs = COURSE_EQUIVALENCIES
        pdefs = {'pgs': pgs, 'cequivs': cequivs, 'cinfo': cinfo}
        self.pdefs = pdefs


    def process(self, ofname: str):

        # Main process loop
        for i, strec in enumerate(self.stinfo):
            print(f"{strec['sinfo'][1]}")  # print campusid
            
            # Get conditional progressions
            cpcs = self.gencondprogs(strec)
            
            # Add to stinfo structure
            pcres = self.genfecdecision(strec)
            
            self.stinfo[i]['cpcs'] = cpcs
            self.stinfo[i]['pcres'] = pcres

        # Generaate output xlsx sheet
        self.writenotes(ofname)
        self.writeprogtable(self.stinfo, 'pcs_curr', ofname, 'Curr')
        self.writeprogtable(self.stinfo, 'pcs_pY', ofname, 'PY')
        self.writeprogtable(self.stinfo, 'pcs_pS2', ofname, 'PS2')
        self.writeprogtable(self.stinfo, 'pcs_pspremb', ofname, 'PsPremB')
        self.writeprogtable(self.stinfo, 'pcs_pspremw', ofname, 'PsPremW')
        self.writeprogtable(self.stinfo, 'pcs_fspremb', ofname, 'FsPremB')
        self.writeprogtable(self.stinfo, 'pcs_fsfrem', ofname, 'FsFrem')
        self.writeoutputtable(self.stinfo, ofname, 'Legacy')

    def _parse_crs_input(self, fname: str, maxrec: float) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Placeholder for reading the CRS input file."""
        # This function would be implemented externally to read and convert
        # the CRS data (likely CSV/TSV) into the stinfo and cinfo structures.
        return [], {}
    
    def genstrecp(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate synthetic student record with all supps/DE/OSS passed (100% mark).
        This synthetic record is used to determine the BEST CASE progression (pcsp).
        """
        ystats_df = strec['ystats'].copy()
        srec_df = strec['srec'].copy()
        cyear = ystats_df['yr'].max()

        # Identify courses to change in current year: Supps, OSS, DE, OS
        srecr = srec_df['perc'].astype(str)
        pipS = srecr.str.contains(r'[0-9].*S', regex=True, na=False)
        pipOSS = srecr.str.contains('OSS', regex=False, na=False)
        pipDE = srecr == 'DE'
        pipOS = srecr == 'OS'
        
        pip = (srec_df['yt'] == cyear) & (pipS | pipOSS | pipDE | pipOS)

        # Modify: Set 'perc' to 'PA' and 'cre' (credits earned) to 'crt' (credit total)
        srec_df.loc[pip, 'perc'] = 'PA'
        srec_df.loc[pip, 'cre'] = srec_df.loc[pip, 'crt']

        # Simple update to ystats for credit totals
        numscr = srec_df.loc[pip, 'crt'].sum()
        ystats_df.iloc[-1, ystats_df.columns.get_loc('TE')] += numscr
        ystats_df.iloc[-1, ystats_df.columns.get_loc('CE')] += numscr
        
        # Simple addition to force vacwork passed (often required for QUAL)
        # Note: If these courses aren't already in the srec, we must append them.
        vac_courses = [('EEE1000X', cyear), ('EEE3000X', cyear)]
        
        for course_code, year in vac_courses:
            if not ((srec_df['course'] == course_code) & (srec_df['yt'] == year)).any():
                # Create a new row (using a structure that matches the DataFrame schema)
                new_row = {'course': course_code, 'yt': year, 'perc': 'PA', 'symbol': 'PA', 'cre': 0, 'crt': 0, 'title': 'Practical Training'}
                srec_df = pd.concat([srec_df, pd.DataFrame([new_row])], ignore_index=True)

        strecp = strec.copy()
        strecp['srec'] = srec_df
        strecp['ystats'] = ystats_df
        return strecp
    


    # NOTE: These methods belong within the FECCheck class

    def gencondprogs(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """Generates conditional progression outcomes for various scenarios."""

        #if strec['sinfo'][1]=='STMKAY002':  print('hehre')
        
        # Current progression
        pcs_curr = self.getprogressioninfo(strec)
        
        # Progression assuming all courses in current year passed (100% mark implied by PA/UP)
        strec_pY = self.flagyearpassed(strec)
        pcs_pY = self.getprogressioninfo(strec_pY)
        
        # Progression assuming all S2 courses in current year passed
        strec_pS2 = self.flagsem2passed(strec)
        pcs_pS2 = self.getprogressioninfo(strec_pS2)
        
        # Supps passed OS/DE 100% and rest in current year passed 100% (Best Case)
        strec_ps = self.flagsuppspassed(strec) # supps passed at 50%
        strec_psvp = self.flagvacworkpassed(strec_ps)
        strec_pspremb = self.flagpassedwithmark(strec_psvp, {'', 'OS', 'DE'}, 100)
        pcs_pspremb = self.getprogressioninfo(strec_pspremb)
        
        # Supps passed OS/DE 50% and rest in current year passed 50% (Worst Case Pass)
        strec_ps = self.flagsuppspassed(strec) # supps passed at 50%
        strec_pspremw = self.flagpassedwithmark(strec_ps, {'', 'OS', 'DE'}, 50)
        pcs_pspremw = self.getprogressioninfo(strec_pspremw)
        
        # Supps failed OS/DE UF and rest in current year passed 100%
        strec_fs = self.flagsuppsfailed(strec)
        strec_fsde = self.flagfaileduf(strec_fs, {'OS', 'DE'}) # Set OS/DE to UF
        strec_fspremb = self.flagpassedwithmark(strec_fsde, {''}, 100) # Pass remaining non-OS/DE
        pcs_fspremb = self.getprogressioninfo(strec_fspremb)

        # Supps failed OS/DE UF and rest in year failed UF
        strec_fs = self.flagsuppsfailed(strec)
        strec_fsde = self.flagfaileduf(strec_fs, {'OS', 'DE'}) # Set OS/DE to UF
        strec_fsfrem = self.flagfaileduf(strec_fsde, {''})
        pcs_fsfrem = self.getprogressioninfo(strec_fsfrem)
        
        # Store instances
        cpcs = {
            'pcs_curr': pcs_curr,
            'pcs_pY': pcs_pY,
            'pcs_pS2': pcs_pS2,
            'pcs_pspremb': pcs_pspremb,
            'pcs_pspremw': pcs_pspremw,
            'pcs_fspremb': pcs_fspremb,
            'pcs_fsfrem': pcs_fsfrem
        }
        return cpcs

    # ----------------------------------------------------------------
    #   Generate synthetic records for various scenarios
    # ----------------------------------------------------------------

    def flagyearpassed(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """All courses for current year PA (Pass)"""
        srec_df = strec['srec'].copy(deep=True)

        cyear = strec['ystats']['yr'].max()
        pip = srec_df['yt'] == cyear
        
        srec_df.loc[pip, 'perc'] = 'PA'
        srec_df.loc[pip, 'symbol'] = 'PA'
        srec_df.loc[pip, 'cre'] = srec_df.loc[pip, 'crt']
        
        strecp = strec.copy() 
        strecp['srec'] = srec_df
        return strecp

    def flagsem2passed(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """All S2 courses for current year PA (Pass)"""
        srec_df = strec['srec'].copy(deep=True)
        
        cyear = strec['ystats']['yr'].max()
        pip = srec_df['yt'] == cyear
        course_suffixes = srec_df['course'].str[7]
        pip = pip & course_suffixes.isin(['S', 'C'])
        
        srec_df.loc[pip, 'perc'] = 'PA'
        srec_df.loc[pip, 'symbol'] = 'PA'
        srec_df.loc[pip, 'cre'] = srec_df.loc[pip, 'crt']
        
        strecp = strec.copy()
        strecp['srec'] = srec_df
        return strecp

    def flagsuppspassed(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """All supps passed for current year (at 50% mark)"""
        srec_df = strec['srec'].copy(deep=True) 
        ystats_df = strec['ystats'].copy(deep=True)
        
        # Supps for year
        cyear = strec['ystats']['yr'].max()
        ia = (srec_df['yt'] == cyear) & (srec_df['symbol'] == 'FS')
        if not ia.any():
            return strec.copy()
    
        crsv = srec_df.loc[ia, 'crt']  # credits
        
        # Original mark (stripping 'S' if present)
        ressv_str = srec_df.loc[ia, 'perc'].str.rstrip('S')
        try:
            psv_orig = pd.to_numeric(ressv_str)
        except:
            psv_orig = 49  # no idea what to do here
        
        # New mark: 50% (standard pass mark for a supp)
        mark_new = 50
        
        # --- Update srec (course record) ---
        srec_df.loc[ia, 'perc'] = 'UP' # Unofficial Pass (Supp)
        srec_df.loc[ia, 'symbol'] = 'SP' # Supp Pass
        srec_df.loc[ia, 'cre'] = srec_df.loc[ia, 'crt'] # Earned full credits
        
        # --- Update ystats (GPA/Credit record) ---
        
        # Find the row index (ri) corresponding to the start of the current year (Term 1)
        ri = ystats_df[ystats_df['yr'] == cyear].index.min()
        
        # Term GPA Update
        G_term = ystats_df.loc[ri, 'Term'] # weighted GPA for term
        W_term_orig = ystats_df.loc[ri, 'TE'] # Term Credit Total (TE)
        
        # The MATLAB logic: G_new = (G_orig * W_orig - sum(crsv * psv_orig) + sum(crsv * mark_new)) / (W_orig)
        # However, the MATLAB code for W is incorrect: W = ystats{ri,{'TE'}} + sum(crsv);
        # A more standard weighted average update (assuming TE is already total credits for the term *including* failed ones):
        # The change in cumulative grade points (CGP): sum(crsv * (mark_new - psv_orig))
        
        # MATLAB Term Fix (replicated):
        W_term_new = W_term_orig + crsv.sum()
        if W_term_new != 0:
            G_term_new = (W_term_orig * G_term - (crsv * psv_orig).sum() + (crsv * mark_new).sum()) / W_term_new
        else:
            G_term_new = 0.0
        ystats_df.loc[ri, 'Term'] = G_term_new
        ystats_df.loc[ri, 'TE'] = W_term_new
        
        # Cumulative GPA Fix (for first entry of the year)
        G_cum = ystats_df.loc[ri, 'Cum']
        W_cum_orig = ystats_df.loc[ri, 'CE'] # Cumulative Credit Total (CE)
        
        # MATLAB Cumulative Fix (replicated):
        W_cum_new = W_cum_orig + crsv.sum()
        if W_cum_new != 0:
            G_cum_new = (W_cum_orig * G_cum - (crsv * psv_orig).sum() + (crsv * mark_new).sum()) / W_cum_new
        else:
            G_cum_new = 0.0
        ystats_df.loc[ri, 'Cum'] = G_cum_new
        ystats_df.loc[ri, 'CE'] = W_cum_new
        
        # Propagate change forward if required (i.e., if there is a Term 2 entry)
        rv = ystats_df[ystats_df['yr'] == cyear].index
        if len(rv) == 2:
            # Term 2 entry is rv[1]
            ri_t2 = rv[1]
            G_t2 = ystats_df.loc[ri_t2, 'Term']
            W_t2 = ystats_df.loc[ri_t2, 'TE']
            
            # New cumulative CGP: (CE_T1_new * Cum_T1_new) + (TE_T2_orig * Term_T2_orig)
            cs_new = ystats_df.loc[ri, 'CE'] * ystats_df.loc[ri, 'Cum'] + W_t2 * G_t2
            
            # New cumulative denominator
            W_cum_t2_new = ystats_df.loc[ri, 'CE'] + W_t2
            
            if W_cum_t2_new != 0:
                ystats_df.loc[ri_t2, 'Cum'] = cs_new / W_cum_t2_new
            else:
                ystats_df.loc[ri_t2, 'Cum'] = 0.0
            ystats_df.loc[ri_t2, 'CE'] = W_cum_t2_new # Must also update CE for Term 2 entry

        strecp = strec.copy()
        strecp['ystats'] = ystats_df
        strecp['srec'] = srec_df
        return strecp

    def flagsuppsfailed(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """All supps failed for current year (Symbol set to SF)."""
        srec_df = strec['srec'].copy(deep=True)
        
        # Supps for year: Symbol is 'FS' (Fail-Supp eligible)
        cyear = strec['ystats']['yr'].max()
        ia = (srec_df['yt'] == cyear) & (srec_df['symbol'] == 'FS')
        
        if ia.any():
            # Strip the 'S' off the percentage/result code (e.g., '45S' -> '45')
            srec_df.loc[ia, 'perc'] = srec_df.loc[ia, 'perc'].str.replace('S', '', regex=False)
            srec_df.loc[ia, 'symbol'] = 'SF' # Supp Fail
            # Credits earned ('cre') remains 0 for fails

        strecp = strec.copy()
        strecp['srec'] = srec_df
        return strecp

    def flagpassedwithmark(self, strec: Dict[str, Any], cvalc: List[str], mark: int) -> Dict[str, Any]:
        """Replace matching course codes (cvalc) with 'mark' in current year."""
        srec_df = strec['srec'].copy(deep=True)
        ystats_df = strec['ystats'].copy(deep=True)
        
        # Entries to change: Current year and 'perc' value in the target list
        cyear = strec['ystats']['yr'].max()
        ia = (srec_df['yt'] == cyear) & (srec_df['perc'].isin(cvalc))
        if not ia.any():
            return strec.copy()
        
        # Credits and marks for the change
        crsv = srec_df.loc[ia, 'crt']
        psv = mark * np.ones(crsv.shape)
        
        # --- Update srec (course record) ---
        srec_df.loc[ia, 'perc'] = str(mark)
        srec_df.loc[ia, 'symbol'] = 'PA'
        srec_df.loc[ia, 'cre'] = srec_df.loc[ia, 'crt']
        
        # --- Update ystats (GPA/Credit record) ---
        
        # Find the row index (ri) corresponding to the start of the current year (Term 1)
        ri = ystats_df[ystats_df['yr'] == cyear].index.min()
        
        # Term GPA Update
        G_term = ystats_df.loc[ri, 'Term']
        W_term_orig = ystats_df.loc[ri, 'TE']
        
        W_term_new = W_term_orig + crsv.sum()
        if W_term_new != 0:
            G_term_new = (W_term_orig * G_term + (crsv * psv).sum()) / W_term_new
        else:
            G_term_new = 0.0
        ystats_df.loc[ri, 'Term'] = G_term_new
        ystats_df.loc[ri, 'TE'] = W_term_new

        # Cumulative GPA Fix (for first entry of the year)
        G_cum = ystats_df.loc[ri, 'Cum']
        W_cum_orig = ystats_df.loc[ri, 'CE']
        
        W_cum_new = W_cum_orig + crsv.sum()
        if W_cum_new != 0:
            G_cum_new = (W_cum_orig * G_cum + (crsv * psv).sum()) / W_cum_new
        else:
            G_cum_new = 0.0
        ystats_df.loc[ri, 'Cum'] = G_cum_new
        ystats_df.loc[ri, 'CE'] = W_cum_new

        # Propagate change forward if required (Term 2 entry)
        rv = ystats_df[ystats_df['yr'] == cyear].index
        if len(rv) == 2:
            ri_t2 = rv[1]
            G_t2 = ystats_df.loc[ri_t2, 'Term']
            W_t2 = ystats_df.loc[ri_t2, 'TE']
            
            cs_new = ystats_df.loc[ri, 'CE'] * ystats_df.loc[ri, 'Cum'] + W_t2 * G_t2
            W_cum_t2_new = ystats_df.loc[ri, 'CE'] + W_t2
            
            if W_cum_t2_new != 0:
                ystats_df.loc[ri_t2, 'Cum'] = cs_new / W_cum_t2_new
            else:
                ystats_df.loc[ri_t2, 'Cum'] = 0.0
            ystats_df.loc[ri_t2, 'CE'] = W_cum_t2_new

        strecp = strec.copy()
        strecp['ystats'] = ystats_df
        strecp['srec'] = srec_df
        return strecp

    def flagfaileduf(self, strec: Dict[str, Any], cvalc: List[str]) -> Dict[str, Any]:
        """Replace matching course codes (cvalc) with 'UF' (Ungraded Fail) in current year."""
        srec_df = strec['srec'].copy(deep=True)
        
        # Entries to change
        cyear = strec['ystats']['yr'].max()
        ia = (srec_df['yt'] == cyear) & (srec_df['perc'].isin(cvalc))
        
        srec_df.loc[ia, 'perc'] = 'UF'
        srec_df.loc[ia, 'symbol'] = 'F' # Assuming UF implies a fail symbol
        srec_df.loc[ia, 'cre'] = 0 # Earned credits is zero
        
        strecp = strec.copy()
        strecp['srec'] = srec_df
        return strecp
    
    def flagvacworkpassed(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        # Flag vacwork passed, appending if necessary
        srec_df = strec['srec'].copy(deep=True)
        
        vac_courses = ['EEE1000X', 'EEE3000X']
        current_year = srec_df['yt'].max() 
        new_rows_to_add = []
        courses_updated = []
        
        for course_code in vac_courses:
            course_mask = (srec_df['course'] == course_code) & (srec_df['yt'] == current_year)
        
            if course_mask.any():
                srec_df.loc[course_mask, 'perc'] = 'PA'
                srec_df.loc[course_mask, 'symbol'] = 'PA'
                courses_updated.append(course_code)
                
            else:
                is_passed_anywhere = (srec_df['course'] == course_code) & (srec_df['perc'] == 'PA')
                
                if not is_passed_anywhere.any():
                    new_record = {
                        'course': course_code, 
                        'yt': current_year, 
                        'perc': 'PA', 
                        'symbol': 'PA', 
                        'cre': 0.0, 
                        'crt': 0.0, 
                        'coursen': 'Practical Training'
                    }
                    new_rows_to_add.append(new_record)


        if new_rows_to_add:
            new_df = pd.DataFrame(new_rows_to_add)
            final_cols = list(srec_df.columns)
            srec_df = pd.concat([srec_df, new_df[final_cols]], ignore_index=True)
            #print(f"Appended 'PA' status for {len(new_rows_to_add)} vacation work courses.")
        if courses_updated:
            pass
            #print(f"Updated existing records in the current year to 'PA' for {', '.join(courses_updated)}.")
        
        strecp = strec.copy()
        strecp['srec'] = srec_df
        return strecp
    
    # ----------------------------------------------------------------
    #   Utilities to identify student status
    # ----------------------------------------------------------------
    def vacworkpassed(self, srec_df: pd.DataFrame) -> bool:
        """Vacation work passed?"""
        # Checks if EEE1000X and EEE3000X are passed ('PA')
        courses_to_check = ['EEE1000X', 'EEE3000X']
        
        for course in courses_to_check:
            ii = srec_df[srec_df['course'].str.contains(course, na=False)]
            # If the course is in the record, check if it was ever marked 'PA'
            if not ii.empty and not (ii['perc'] == 'PA').any():
                return False
        return True

    def aspectstudent(self, strec: Dict[str, Any]) -> bool:
        """Student on aspect if now or ever on aspect programme code (8 in 3rd position)."""
        preg = strec['ystats']['preg']
        aspect = (preg.str[2] == '8').any()
        
        return aspect

    def credpassed(self, strec: Dict[str, Any], cyear: int) -> float:
        """Calculate total credits passed for a specific year."""
        srec_df: pd.DataFrame = strec['srec']
        
        # Passed indicators: mark >= 50 OR is 'PA'/'UP'/'50C'
        srecr = srec_df['perc'].astype(str)
        pip50 = pd.to_numeric(srecr, errors='coerce') >= 50
        pipPA = srecr == 'PA'
        pipUP = srecr == 'UP'
        pipCon = srecr == '50C'
        
        pip = pip50 | pipPA | pipUP | pipCon
        
        # Sum credits earned (cre) for the target year (cyear)
        crp = srec_df[(srec_df['yt'] == cyear) & pip]['cre'].sum()
        return crp

    def getsrecp(self, srec_df: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray]:
        """Flags for courses passed and returns passed records (srecp) and index map (pipmap)."""
        
        srecr = srec_df['perc'].astype(str)
        pip50 = pd.to_numeric(srecr, errors='coerce') >= 50
        pipPA = srecr == 'PA'
        pipUP = srecr == 'UP'
        pipCon = srecr == '50C'
        pipCX = srecr == 'CX'
        pipEX = srecr == 'EX'
        pipCR = srecr == 'CR'
        
        # Courses in record passed
        pip = pip50 | pipPA | pipUP | pipCon | pipCX | pipEX | pipCR
        
        # pipmap: 1-based index (for MATLAB compatibility, but we'll use 0-based index here)
        pipmap = srec_df.index[pip].values + 1
        srecp_df = srec_df[pip]  # passed
        
        return srecp_df, pipmap

    def getqualinfo(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """Gathers all information required to check for qualification."""
        ystats_df = strec['ystats']
        srec_df = strec['srec']
        
        # Aspect
        aspect = self.aspectstudent(strec)
        
        # Certificate for core completed
        tcert = self.gentcert(strec)
        
        # Total credits passed (using the 'cre' column)
        totalcr = srec_df['cre'].sum()
        
        # GPA
        fyreg = ystats_df['yr'].min()
        wgpa = ystats_df.iloc[-1]['Wghtd'] # weighted GPA
        cgpa = ystats_df.iloc[-1]['Cum'] # cumulative GPA
        
        gpa = cgpa
        if fyreg < 2016:
            gpa = wgpa

        # Number of credits in curriculum for student
        yfdreg = self.firstdeptreg(strec)
        if yfdreg>=2025:  rcurcr = 560
        else:  rcurcr = 576
            
        # Duration
        cyear = ystats_df['yr'].max()
        
        # Number of years registered in department (eedur)
        ia = ystats_df['preg'].isin(EEE_PROGS)
        eeyrs = ystats_df[ia]['yr']
        eedur = eeyrs.nunique()
        
        # Get 4022 pass mark
        res4022 = -1
        # Passed indicators
        srecr = srec_df['perc'].astype(str)
        pip50 = pd.to_numeric(srecr, errors='coerce') >= 50
        pipPA = srecr == 'PA'
        pipUP = srecr == 'UP'
        pipCon = srecr == '50C'
        pip = pip50 | pipPA | pipUP | pipCon
        
        ii = srec_df['course'].str.contains('EEE4022', na=False) & pip
        
        if ii.sum() == 1:
            res4022 = pd.to_numeric(srec_df[ii]['perc'].iloc[0], errors='coerce')
        elif ii.sum() > 1:
            print("Warning: Multiple EEE4022 passes found.")
        
        # Return object with results
        qres = {
            'aspect': aspect,
            'tcert': tcert,
            'rcurcr': rcurcr,
            'totalcr': totalcr,
            'gpa': gpa,
            'eedur': eedur,
            'res4022': res4022
        }
        return qres
    

    # NOTE: These methods belong within the FECCheck class

    # ----------------------------------------------------------------
    #   Utilities to support getprogressioninfo()
    # ----------------------------------------------------------------
    
    def isqual(self, qres: Dict[str, Any]) -> Tuple[bool, str]:
        """Student is qualifier (and honours)?"""
        qualf = False
        hons = ''
        
        tcert_df: pd.DataFrame = qres.get('tcert')
        
        # Return if not qualifier
        # 1. Not all core requirements satisfied (tcert.Sat is False for any row)
        # 2. Total credits passed is less than rcurcr
        if tcert_df is None or not tcert_df['Sat'].all() or qres['totalcr'] < qres['rcurcr']:
            return qualf, hons
            
        qualf = True
        
        # Required minimum time for honours
        mtime = 5 if qres['aspect'] else 4
        
        # First class honours
        gpa_rounded = round(qres['gpa'])
        if gpa_rounded >= 75 and qres['res4022'] >= 75 and qres['eedur'] <= mtime:
            hons = 'FCH'
            return qualf, hons
            
        # Honours
        if gpa_rounded >= 65 and qres['res4022'] >= 60 and qres['eedur'] <= mtime:
            hons = 'HONS'
            return qualf, hons
            
        return qualf, hons
    
    def getnumstrikes(self, strec: Dict[str, Any]) -> int:
        """Calculate number of previous progression defaults."""
        ystats_df: pd.DataFrame = strec.get('ystats')
        if ystats_df is None or ystats_df.empty: return 0
        
        STRIKE_CODES = {'FECR', 'RACC', 'RENN'}
        
        ia = ystats_df['preg'].isin(EEE_PROGS)
        
        ee_ystats = ystats_df[ia]
        ib = ee_ystats['pcode'].isin(STRIKE_CODES)
        
        num = ib.sum()
        return int(num)
        
    def transferstudent(self, strec: Dict[str, Any]) -> int:
        """Student transferred into department? (0 no, 1 internal, 2 external, 3 problem)"""
        tfer = -1
        srec_df: pd.DataFrame = strec.get('srec')
        ystats_df: pd.DataFrame = strec.get('ystats')
        
        if srec_df is None or ystats_df is None or ystats_df.empty: return -1
        if ystats_df.iloc[-1]['preg'] not in EEE_PROGS:  return -1  # not currently in EEE

        eee_reg_mask = ystats_df['preg'].isin(EEE_PROGS)
        eee_registrations = ystats_df[eee_reg_mask]
        first_eee_index = eee_registrations.index.min()
        last_eee_index = eee_registrations.index.max()
        middle_registrations = ystats_df.loc[first_eee_index:last_eee_index]

        # Student left department then returned?
        if not middle_registrations['preg'].isin(EEE_PROGS).all():
            return 3 
        
        # Started at UCT in different department
        is_internal_transfer = (eee_registrations['yr'].min() > ystats_df['yr'].min())
        if is_internal_transfer:
            return 1
        
        # External transfers have block credits ('CR', 'CX', 'EX') in first year at UCT
        first_eee_year = eee_registrations['yr'].min()
        srec_first_year = srec_df[srec_df['yt'] == first_eee_year]
        if srec_first_year['perc'].isin(['CR', 'CX', 'EX']).any():
            return 2
        
        # First registration is EEE and no transfer detected
        return 0
        
    def onesemesterreg(self, strec: Dict[str, Any]) -> bool:
        """Current registration for single semester? (Semester 1 only or Semester 2 only)"""
        srec_df: pd.DataFrame = strec.get('srec')
        ystats_df: pd.DataFrame = strec.get('ystats')
        
        if srec_df is None or ystats_df is None or ystats_df.empty: return False
        
        cyear = ystats_df['yr'].max()
        lycreg = srec_df[srec_df['yt'] == cyear]['course']
        if lycreg.empty: return False
        
        # Extract the 8th character (index 7) of the course code for the suffix
        csuff = lycreg.str[7]
        
        fflag = csuff.isin(['F', 'A']).any() # F = Sem 1, A = Full Year
        sflag = csuff.isin(['S', 'C']).any() # S = Sem 2, C = Full Year
        wflag = csuff.isin(['W']).any() # Winter Term
        
        # Single semester registration logic
        if (fflag and not sflag and not wflag) or (not fflag and sflag and not wflag):
            return True
            
        return False
    
    def firstdeptreg(self, strec: Dict[str, Any]) -> int:
        ystats_df: pd.DataFrame = strec.get('ystats')

        ia = ystats_df['preg'].isin(EEE_PROGS)
        ee_registrations = ystats_df[ia]
        yfdreg = ee_registrations['yr'].min()
        
        return yfdreg
    
    def firstdeptprogcode(self, strec: Dict[str, Any]) -> str:
        ystats_df: pd.DataFrame = strec.get('ystats')

        ia = ystats_df['preg'].isin(EEE_PROGS)
        ee_registrations = ystats_df[ia]
        first_year = ee_registrations['yr'].min()
        ri = ystats_df[ystats_df['yr'] == first_year].index.min()
        first_pcode = ystats_df.loc[ri, 'pcode']
        
        return str(first_pcode)
    
    def unbrokendeptreg(self, strec: Dict[str, Any]) -> bool:
        ystats_df: pd.DataFrame = strec.get('ystats')

        ia = ystats_df['preg'].isin(EEE_PROGS)
        ee_registrations = ystats_df[ia].copy()
        reg_years = ee_registrations['yr'].unique()
        year_diffs = np.diff(reg_years)
        is_unbroken = (year_diffs == 1).all()

        return is_unbroken
    
    def unbrokendeptregdur(self, strec: Dict[str, Any]) -> int:
        ystats_df: pd.DataFrame = strec.get('ystats')

        ia = ystats_df['preg'].isin(EEE_PROGS)
        ee_registrations = ystats_df[ia].copy()
        years = ee_registrations['yr'].dropna().unique().astype(int)
        years.sort()
        
        current_year = years[-1]
        duration = 0
        for year in reversed(years):
            expected_year = current_year - duration
            
            if year == expected_year:  duration += 1
            else:  break
            
        return duration
        
    # ----------------------------------------------------------------
    #   Primary method for determining progression
    # ----------------------------------------------------------------
    
    def getprogressioninfo(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """Core logic for determining the student's progression status."""

        ystats_df = strec['ystats']
        srec_df = strec['srec']
        cyear = ystats_df['yr'].max()

        #if strec['sinfo'][1]=='STMKAY002':  print('hehre')

        # Important student info
        aspect = self.aspectstudent(strec)
        tfer = self.transferstudent(strec)
        nstrikes = self.getnumstrikes(strec)
        yfreg = ystats_df['yr'].min()  # first UCT registration
        yfdreg = self.firstdeptreg(strec)  # first departmental registration
        ubdreg = self.unbrokendeptreg(strec)
        ssreg = self.onesemesterreg(strec)
        
        leavf = False
        if strec.get('leavmess'):
            leavf = True
            
        # Get qualifier status and stats
        qres = self.getqualinfo(strec)
        qualf, hons = self.isqual(qres)
        eedur = qres['eedur']
        ubdrdur = self.unbrokendeptregdur(strec)

        # First progression code in department
        fdpcode = self.firstdeptprogcode(strec) 
        
        # Previous progression code
        lpcode = 'NONE'
        prev_year_stats = ystats_df[ystats_df['yr'] == cyear - 1]
        if not prev_year_stats.empty:
            lpcode = prev_year_stats.iloc[0]['pcode']
            
        # Credits earned in current and previous year
        ccrp = self.credpassed(strec, cyear)
        lcrp = self.credpassed(strec, cyear - 1)
        
        # Calculate N+1 and N+2 credit requirements
        N = 5 if aspect else 4
        creds_needed = max(0, qres['rcurcr'] - qres['totalcr'])
        
        # N+1
        rem_years_np1 = (N + 1) - eedur
        if rem_years_np1 > 0:
            np1crpy = round(creds_needed / rem_years_np1, 1)
        else:
            np1crpy = 9999.0 if creds_needed > 0 else 0.0
            
        # N+2
        rem_years_np2 = (N + 2) - eedur
        if rem_years_np2 > 0:
            np2crpy = round(creds_needed / rem_years_np2, 1)
        else:
            np2crpy = 9999.0 if creds_needed > 0 else 0.0

        # Limits for decisions
        # Define thresholds for Normal (4-year) versus Aspect (5-year) students
        if not aspect:
            ret_limit = 116 if qres['rcurcr'] >= 576 else 112
            limits = {
                'FU_RENN': 66,
                'FU_FECR': 96,
                'TU_FECR': 96,
                'RET_FECR': ret_limit,
            }
        else:
            ret_limit = 96 if qres['rcurcr'] >= 576 else 92
            limits = {
                'FU_RENN': 48,   # First year entering RENN limit
                'FU_FECR': 60,   # First year entering FECR limit
                'TU_FECR': 60,   # First year transferee FECR limit
                'RET_FECR': ret_limit,  # Returning FECR limit
            }

        # Progression code decision tree
        pc = 'CONT' # Default to CONT
        pmess = ''
        
        if qualf:
            pc = 'QUAL'
            pmess = hons
        elif leavf:
            pc = 'LEAV'
            pmess = strec['leavmess']
        
        # First Year Checks
        elif yfreg == cyear:
            if ccrp < limits['FU_RENN']:
                pc = 'RENN'
                pmess = f"{ccrp:.0f}<{limits['FU_RENN']:.0f} (first year)"
            elif ccrp < limits['FU_FECR']:
                pc = 'FECR'
                pmess = f"{ccrp:.0f}<{limits['FU_FECR']:.0f} (first year)"
            else: # ccrp >= fulim
                pc = 'CONT'
                pmess = f"{ccrp:.0f}>={limits['FU_FECR']:.0f} (first year)"
        
        # Returning/Transfer Checks
        elif (tfer in [1, 2]) and (ubdrdur == 1):
            if ccrp < limits['TU_FECR']:
                if nstrikes == 0:
                    pc = 'FECR'
                    pmess = f"{ccrp:.0f}<{limits['TU_FECR']:.0f} (transf, first default)"
                else:
                    pc = 'RENN'
                    pmess = f"{ccrp:.0f}<{limits['TU_FECR']:.0f} (transf, previous defaults)"
            else: # ccrp >= tulim
                pc = 'CONT'
                pmess = f"{ccrp:.0f}>={limits['TU_FECR']:.0f} (transf)"

        else:
            if ccrp < limits['RET_FECR']:
                if nstrikes == 0:
                    pc = 'FECR'
                    pmess = f"{ccrp:.0f}<{limits['RET_FECR']:.0f} (ret, first default)"
                else:
                    pc = 'RENN'
                    pmess = f"{ccrp:.0f}<{limits['RET_FECR']:.0f} (ret, previous defaults)"
            else: # ccrp >= tulim
                pc = 'CONT'
                pmess = f"{ccrp:.0f}>={limits['RET_FECR']:.0f} (ret)"
                
        # Flag supps and others outstanding
        srecr = srec_df['perc'].astype(str)
        pipS = srecr.str.contains(r'[0-9].*S', regex=True, na=False)
        pipOSS = srecr.str.contains('OSS', regex=False, na=False)
        pipDE = srecr == 'DE'
        pipOS = srecr == 'OS'
        
        pip = (srec_df['yt'] == cyear) & (pipS | pipOSS | pipDE | pipOS)
        
        suppdes = srec_df[pip]['course'].tolist()
        suppdecr = srec_df[pip]['crt'].sum()
        
        # Missing core
        ii = (qres['tcert']['Sat'] == False)
        cmissing = qres['tcert'][ii]['Req'].tolist()
        
        # Courses failed current year (symbol 'F' or percentage 'UF')
        pip_failed = (srec_df['yt'] == cyear) & ((srec_df['symbol'] == 'F') | (srec_df['perc'] == 'UF'))
        nfcy = pip_failed.sum()
        ccyfailed = srec_df[pip_failed]['course'].tolist()
        
        # Store results
        pcs = {
            'qualf': qualf, 'hons': hons,
            'pc': pc, 'pmess': pmess,
            'aspect': aspect, 'tfer': tfer,
            'nstrikes': nstrikes, 'yfreg': yfreg, 'yfdreg': yfdreg, 'ubdreg': ubdreg,
            'ssreg': ssreg, 'leavf': leavf,
            'ccrp': ccrp, 'lcrp': lcrp, 'totalcr': qres['totalcr'], 'rcurcr': qres['rcurcr'],
            'np1crpy': np1crpy, 'np2crpy': np2crpy,
            'gpa': qres['gpa'], 'eedur': qres['eedur'], 'res4022': qres['res4022'],
            'tcert': qres['tcert'],
            'suppdes': suppdes, 'suppdecr': suppdecr,
            'cmissing': cmissing,
            'nfcy': int(nfcy), 'ccyfailed': ccyfailed
        }
        return pcs
        
    def genfecdecision(self, strec: Dict[str, Any]) -> Dict[str, Any]:
        """Generates the final FEC progression decision based on current and best-case scenarios."""
        srec_df: pd.DataFrame = strec.get('srec')
        ystats_df: pd.DataFrame = strec.get('ystats')
        if srec_df is None or ystats_df is None or srec_df.empty:
            return {'pc': 'ERR', 'pmess': 'No records', 'suppdecr': 0, 'cmissing': [], 'nfcy': 0, 'cfcy': ''}
            
        cyear = ystats_df['yr'].max()
        
        # Current progression code with message (worst case)
        pcs = self.getprogressioninfo(strec)
        
        # Process pseudo record for all passed (best case)
        strecp = self.genstrecp(strec)
        pcsp = self.getprogressioninfo(strecp)
        
        # Flag supps and others outstanding (for current record) - Replicated for output fields
        srecr = srec_df['perc'].astype(str)
        pipS = srecr.str.contains(r'[0-9].*S', regex=True, na=False)
        pipOSS = srecr.str.contains('OSS', regex=False, na=False)
        pipDE = srecr == 'DE'
        pipOS = srecr == 'OS'
        pip = (srec_df['yt'] == cyear) & (pipS | pipOSS | pipDE | pipOS)
        
        suppdes = srec_df[pip]['course'].tolist()
        suppdecr = srec_df[pip]['crt'].sum()
        
        # Complex coding if supp outcomes important (Worst vs Best Case)
        pc = pcs['pc']
        pmess = pcs['pmess']
        
        if pcs['pc'] != pcsp['pc']:
            if pcsp['pc'] == 'QUAL':
                pc = 'QUAS' # Qualify assuming Supps/DE passed
                pmess = pcsp['hons']
            elif pcs['pc'] == 'RENN' and pcsp['pc'] == 'CONT':
                pc = 'SUPP' # Requires supplement to continue
                pmess = f"RENN ({pcs['pmess']}) OR CONT({pcsp['pmess']})"
            elif pcs['pc'] == 'FECR' and pcsp['pc'] == 'CONT': 
                pc = 'FECP' # Possible to continue with passing supps
                pmess = f"FECR ({pcs['pmess']}) OR CONT({pcsp['pmess']})"
            elif pcs['pc'] == 'RENN' and pcsp['pc'] == 'FECR': 
                pc = 'FECP' # Possible to FECR with passing supps
                pmess = f"RENN ({pcs['pmess']}) OR FECR({pcsp['pmess']})"
            else:
                # Debugging hook
                print(f"Decision logic mismatch: {pcs['pc']} vs {pcsp['pc']}")
                
        # Missing core
        tcert_df: pd.DataFrame = pcs['tcert']
        ii = (tcert_df['Sat'] == False)
        cmissing = tcert_df[ii]['Req'].tolist()
        
        # Courses failed current year
        pip_failed = (srec_df['yt'] == cyear) & ((srec_df['symbol'] == 'F') | (srec_df['perc'] == 'UF'))
        
        nfcy = pip_failed.sum()
        cfcy = ','.join(srec_df[pip_failed]['course'].tolist())
        
        # Return
        pcres = {
            'pc': pc,
            'pmess': pmess,
            'suppdes': suppdes,
            'suppdecr': suppdecr,
            'cmissing': cmissing,
            'nfcy': int(nfcy),
            'cfcy': cfcy,
            'pcs': pcs,
            'pcsp': pcsp
        }
        return pcres

    def gentcert(self, strec: Dict[str, Any]) -> pd.DataFrame:
        """Determines if core degree requirements have been completed (Certificate)."""
        srec_df: pd.DataFrame = strec['srec']
        srecp_df, pipmap = self.getsrecp(srec_df) # Passed records
        
        pdefs = self.pdefs
        pgs = pdefs['pgs']
        cequivs = pdefs['cequivs']
        
        bprog = strec['sinfo'][3] # acadprog (col 4 in MATLAB)
        bprogb = bprog[:2] + '0' + bprog[3:] # Standardize to non-Aspect for lookup
        
        pg_list = [p for p in pgs if p.get('code') == bprogb]
        if not pg_list:
            return pd.DataFrame({'Req': [], 'Sat': [], 'Satev': []})
        pg = pg_list[0]
        cclist = pg['cclist']
        
        # Course index in cclist that has been passed
        cclist_passed_mask = np.zeros(len(cclist), dtype=bool)
        # Map from cclist index to srecp (passed course) index
        
        tcert_data = []

        # --- Helper for checking a core requirement (direct or equivalent) ---
        def check_course_satisfied(req_course):
            is_satisfied = False
            sat_evidence = []
            srecp_indices = []

            # 1. Direct Course Match
            try:
                # Get the index of the passed course in srecp
                srecp_match_indices = srecp_df[srecp_df['course'] == req_course].index.tolist()
                if srecp_match_indices:
                    is_satisfied = True
                    srecp_indices.extend(srecp_match_indices)
            except:
                pass # Course not found

            # 2. Equivalences Check
            if not is_satisfied:
                for equiv_list in cequivs:
                    if equiv_list[0] == req_course:
                        for item in equiv_list[1:]:
                            try:
                                srecp_match_indices = srecp_df[srecp_df['course'] == item].index.tolist()
                                if srecp_match_indices:
                                    is_satisfied = True
                                    srecp_indices.extend(srecp_match_indices)
                                    break
                            except:
                                pass
                        if is_satisfied: break

            # Build evidence string (using the original srec index via pipmap)
            # Find the original index for evidence string
            if srecp_indices:
                for idx in srecp_indices:
                    original_srec_index = srecp_df.index[srecp_df.index == idx].values[0]
                    sat_evidence.append(f"{srec_df.loc[original_srec_index, 'course']}({int(srec_df.loc[original_srec_index, 'yt'])})")

            return is_satisfied, ','.join(sat_evidence)

        # --- Check Core ---
        core = pg['core']
        
        for core_req in core:
            is_satisfied, sat_evidence = check_course_satisfied(core_req)
            tcert_data.append([core_req, is_satisfied, sat_evidence])
            
            # Update the cclist_passed_mask for use in elective checks later
            if is_satisfied and core_req in cclist:
                 cclist_passed_mask[cclist.index(core_req)] = True

        # --- Check Elective Core (by Number of Courses) ---
        for i, item in enumerate(pg.get('necore', [])):
            required_num = item[0]
            clist = item[1:]
            
            passed_count = 0
            sat_evidence = []
            
            # Use a set to prevent counting the same passed course multiple times if listed in multiple necore items
            passed_courses_in_list = set()
            
            for req_course in clist:
                is_satisfied, evidence = check_course_satisfied(req_course)
                if is_satisfied:
                    # We need to track the unique courses that satisfied the requirement
                    # The evidence string contains course(year), we'll parse the course code.
                    course_code = req_course # Simplified tracking, assuming no equivs here for count
                    if course_code not in passed_courses_in_list:
                        passed_courses_in_list.add(course_code)
                        sat_evidence.append(evidence) # Add evidence string. Note: This can lead to comma-separated evidence strings
            
            passed_count = len(passed_courses_in_list)
            satf = passed_count >= required_num
            tcert_data.append([f"ECnum{i+1}", satf, ','.join(sat_evidence)])

        # --- Check Elective Core (by Credits) ---
        for i, item in enumerate(pg.get('cecore', [])):
            required_credits = item[0]
            clist = item[1:]
            
            # Filter passed records for those in the elective core list
            sreci_df = srecp_df[srecp_df['course'].isin(clist)]
            
            nce = sreci_df['cre'].sum()  # number of credits earned
            
            sat_evidence = []
            for _, row in sreci_df.iterrows():
                sat_evidence.append(f"{row['course']}({int(row['yt'])})")
                
            satf = nce >= required_credits
            tcert_data.append([f"ECcred{i+1}", satf, ','.join(sat_evidence)])
            
        tcert_df = pd.DataFrame(tcert_data, columns=['Req', 'Sat', 'Satev'])
        return tcert_df
    
    # NOTE: These methods belong within the FECCheck class

    # ----------------------------------------------------------------
    #   Output results to Excel sheets
    # ----------------------------------------------------------------
    
    header_comments_map = {
        'pc': "Progression code to be reported",
        'pmess': "Message explaining reported progression code",
        'aspect': "At some stage student was registered under ASPECT code",
        'tfer': "Transferring student (0 no, 1 internal, 2 external, 3 problem)",
        'eedur': "Number of years registered in department", 
        'ubdreg': "Unbroken registration in department since entering department",
        'nstrikes': "Number of strikes already received", 
        'ssreg': "Last year of registration was just for single semester", 
        'leavf': "Currently on LOA",
        'crpp': "Number of credits passed previous (last) year", 
        'crpc': "Number of credits passed current (this) year", 
        'totcr': "Total number of credits passed", 
        'rcurcr': "Required number of credits in programme",
        'np1crpy': "Avg credits/year to finish in N+1 years",
        'np2crpy': "Avg credits/year to finish in N+2 years",
        'gpa': "Current GPA",
        'coresat': "Flag for all core degree requirements met",
        'res4022': "Result (percentage) for EEE4022 (-1 if not complete)",
        'supp/decr': "Total OS/Supp/DE credits outstanding",
        'supp/des': "List of courses for which OS/Supp/DE outstanding",
        'cmissing': "List of courses/requirements outstanding",
        'nfcy': "Number of courses failed current year",
        'cfcy': "List of courses failed current year"
    }
        
    def writenotes(self, fname: str) -> None:
        """Write notes sheet to Excel"""

        notes_data = [
            "Sheets:", "Curr - current record", "PY - all current year courses PA",
            "PS2 - all second (S2) semester courses PA", 
            "PsPremB - Passed supps (OS/DE 100%) and passed remaining (100%) - best case pass",
            "PsPremW - Passed supps (OS/DE 50%) and and passed remaining (50%) - worst case pass",
            "FsPremB - Failed supps (DE/OS UF) and best case passes for current year",
            "FsFrem - Failed supps (OS/DE UF) and rest in year failed (UF)"
            "Legacy - original output before disaggregation",
            "", "Fields:"
        ]

        for key, value in self.header_comments_map.items():
            notes_data.append(f"{key}: {value}")

        notes_df = pd.DataFrame({'Notes': notes_data})

        try:
            with pd.ExcelWriter(fname, engine='xlsxwriter') as writer:
                notes_df.to_excel(writer, sheet_name='Notes', index=False)
            print(f"Notes sheet written to {fname}.")
        except Exception as e:
             print(f"Failed to write notes sheet to Excel: {e}")
        pass

    def writeprogtable(self, stinfo: List[Dict[str, Any]], sfname: str, fname: str, shname: str) -> None:
        """Write progression instance to sheet"""

        output_data = []
        for strec in stinfo:
            if 'cpcs' in strec and sfname in strec['cpcs']:
                pcs = strec['cpcs'][sfname]
                
                # Coresat is a flag: True if all elements in pcs['tcert']['Sat'] are True
                coresat = pcs['tcert']['Sat'].all() if pcs['tcert'] is not None else False

                output_data.append({
                    'campusid': strec['sinfo'][1],
                    'name': strec['sinfo'][0],
                    'acadprog': strec['sinfo'][3],
                    'pc': pcs['pc'],
                    'pmess': pcs['pmess'],
                    'aspect': pcs['aspect'],
                    'tfer': pcs['tfer'],
                    'eedur': pcs['eedur'],
                    'ubdreg': pcs['ubdreg'],
                    'nstrikes': pcs['nstrikes'],
                    'ssreg': pcs['ssreg'],
                    'leavf': pcs['leavf'],
                    'crpp': pcs['lcrp'],
                    'crpc': pcs['ccrp'],
                    'totcr': pcs['totalcr'],
                    'rcurcr': pcs['rcurcr'],
                    'np1crpy': pcs['np1crpy'],
                    'np2crpy': pcs['np2crpy'],
                    'gpa': pcs['gpa'],
                    'coresat': 1.0 if coresat else 0.0,
                    'res4022': pcs['res4022'],
                    'supp/decr': pcs['suppdecr'],
                    'supp/des': ','.join(pcs['suppdes']),
                    'cmissing': ','.join(pcs['cmissing']),
                    'nfcy': pcs['nfcy'],
                    'cfcy': ','.join(pcs['ccyfailed']),
                })
        
        otab = pd.DataFrame(output_data)
        column_order = list(otab.columns)
        
        try:
            with pd.ExcelWriter(fname, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                otab.to_excel(writer, sheet_name=shname, index=False)
                worksheet = writer.sheets[shname]

                for i, header_key in enumerate(column_order):
                    col_letter = get_column_letter(i + 1)
                    cell_address = f'{col_letter}1'
                    description = self.header_comments_map.get(header_key)
                            
                    if description:
                        comment_text = f"{description}"
                        header_comment = Comment(text=comment_text, author="Progression Report")
                        worksheet[cell_address].comment = header_comment

            print(f"Progression table for {shname} written to {fname}.")
        except Exception as e:
             print(f"Failed to write progression table for {shname} to Excel: {e}")
        pass


    def writeoutputtable(self, stinfo: List[Dict[str, Any]], fname: str, shname: str) -> None:
        """Write final progression (pcres) to sheet (legacy)"""
        
        output_data = []
        for strec in stinfo:
            pcres = strec.get('pcres')
            if pcres is None: continue
            
            # Format suppnames
            suppnames = ','.join(pcres['suppdes'])
            
            # Format cmissingstr
            cmissing = pcres['cmissing']
            if len(cmissing) > 4:
                cmissingstr = 'More than 4'
            else:
                cmissingstr = ','.join(cmissing)

            # Coresat is a flag: True if all elements in pcs['tcert']['Sat'] are True
            coresat = pcres['pcs']['tcert']['Sat'].all() if pcres['pcs']['tcert'] is not None else False

            output_data.append({
                'campusid': strec['sinfo'][1],
                'name': strec['sinfo'][0],
                'acadprog': strec['sinfo'][3],
                'pc': pcres['pc'],
                'pmess': pcres['pmess'],
                'aspect': pcres['pcs']['aspect'],
                'tfer': pcres['pcs']['tfer'],
                'ubdreg': pcres['pcs']['ubdreg'],
                'eedur': pcres['pcs']['eedur'],
                'nstrikes': pcres['pcs']['nstrikes'],
                'ssreg': pcres['pcs']['ssreg'],
                'leavf': pcres['pcs']['leavf'],
                'crpp': pcres['pcs']['lcrp'],
                'crpc': pcres['pcs']['ccrp'],
                'totcr': pcres['pcs']['totalcr'],
                'rcurcr': pcres['pcs']['rcurcr'],
                'np1crpy': pcres['pcs']['np1crpy'],
                'np2crpy': pcres['pcs']['np2crpy'],
                'gpa': pcres['pcs']['gpa'],
                'coresat': 1.0 if coresat else 0.0,
                'res4022': pcres['pcs']['res4022'],
                'supp/decr': pcres['suppdecr'],
                'supp/des': suppnames,
                'cmissing': cmissingstr,
                'cfcy': pcres['cfcy'],
            })
        
        otab = pd.DataFrame(output_data)
        #print(otab)
        
        try:
            with pd.ExcelWriter(fname, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                otab.to_excel(writer, sheet_name=shname, index=False)
            print(f"Final output table for {shname} written to {fname}.")
        except Exception as e:
             print(f"Failed to write final output table for {shname} to Excel: {e}")
        pass


if __name__ == '__main__':
    crsname = '/Users/nicolls/proj/eleceng_matlab/feccheck/2024/CSV Electrical Engineering_20240214.csv'
    FECCheck(crsname, 15)