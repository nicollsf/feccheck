import csv, io, re, os
from typing import List, Dict, Tuple, Any, Union, Optional
import pandas as pd
import numpy as np


YSTATS_HEADERS = ['yr', 'tt', 'preg', 'pnam', 'ayosn', 'pcode', 'progc', 'JT', 'JE', 'ST', 'SE', 'TT', 'TE', 'CE', 'Wghtd', 'Term', 'Cum']
SREC_HEADERS = ['course', 'yt', 'perc', 'symbol', 'cre', 'crt', 'coursen']

StudentInfo = Dict[str, Union[Any, pd.DataFrame]]
CourseInfo = List[Tuple[str, str, str]]


def parsecrsinput(
    fname: str,
    maxrec: float = float('inf'),
    enc: str = 'latin-1',
    delim: str = ',',
    ufname: str = ''
) -> Tuple[List[StudentInfo], CourseInfo]:
    """
    Load student CRS info from a custom multi-line, report-like CSV file.
    
    Equivalent to: function [stinfo,cinfo] = parsecrsinput(fname,maxrec,delim,ufname)

    Args:
        fname: Path to the input CSV file.
        maxrec: Maximum number of records to read (inf by default).
        delim: Delimiter character (default is ',').
        ufname: Path to the update file.

    Returns:
        A tuple: (stinfo, cinfo)
        stinfo: List of student record dictionaries.
        cinfo: List of course info tuples.
    """

    stinfo: List[StudentInfo] = []
    cinfo: CourseInfo = []
    
    reccount = 0
    in_record = False
    current_year = 0

    stinfo_curr: StudentInfo = {}

    current_ystats_data: List[List[Any]] = []
    current_srec_data: List[List[Any]] = []

    with open(fname, 'r', newline='', encoding=enc) as f:
        for line in f:
            if not line.strip(): continue

            cleaned_line = re.sub(r'""(.*?)""', r'"\1"', line)  # double quotes to single
            cleaned_line = cleaned_line.strip().rstrip(';')  # strip trailing semicolon
            cleaned_line = cleaned_line.strip('"')  # drop leading and trailing double quotes if necessary
            if not cleaned_line:  continue

            f_obj = io.StringIO(cleaned_line)
            line_reader = csv.reader(f_obj, delimiter=delim, quotechar='"')
            row = next(line_reader)

            if len(row)<=2:  continue

            if re.match(r'[A-Z]{6}[0-9]{3}$', row[2]):
                #print("Located start of record " + row[2])

                # Sometimes the name is split in two?
                combined_field = f"{row[0]},{row[1]}" 
                row = [combined_field] + row[2:]

                reccount += 1
                stinfo_curr = {'sinfo': row}
                current_ystats_data = []
                current_srec_data = []
                sreco = []
                in_record = True
                leavmess = ''

            if in_record is False:  continue

            if re.match(r'[0-9]{4}$', row[0]):
                cyear = int(row[0])
                while len(row)<21: row.append('')
                stats_slice = row[11:21]

                ystatsd = []
                for val in stats_slice:
                    try:  ystatsd.append(float(val))
                    except: ystatsd.append(float('nan'))
                ystatsd_cleaned = [0.0 if str(val) == 'nan' else val for val in ystatsd]
                new_stats_row = [cyear] + row[1:7] + ystatsd_cleaned
                current_ystats_data.append(new_stats_row)

                continue

            if len(row)>1 and row[1]=='Passed:':
                ystats_df = pd.DataFrame(current_ystats_data, columns=YSTATS_HEADERS)
                stinfo_curr['ystats'] = ystats_df
                srec_df = pd.DataFrame(current_srec_data, columns=SREC_HEADERS)
                stinfo_curr['srec'] = srec_df
                
                stinfo.append(stinfo_curr)
                reccount = len(stinfo)
                inrecf = False
                cyear = 0

                if reccount>=maxrec:  break  # Exit the 'for row in reader:' loop entirely
                continue # Skip the rest of the loop and move to the next 'row'

            course_pattern = r'[A-Z]{3}[0-9]{4}.'
            if len(row)>=7 and len(row[1])>=8 and re.match(course_pattern, row[1]):
                try:  ce = float(row[4])
                except ValueError:  ce = 0.0
                try:  cc = float(row[5])
                except ValueError:  cc = 0.0
                    
                new_srec_row = [row[1][:8], cyear, row[2], row[3], ce, cc, row[6]]
                current_srec_data.append(new_srec_row)

            if len(row)>=14 and len(row[8])>=8 and re.match(course_pattern, row[8]):
                try:  ce = float(row[11])
                except ValueError:  ce = 0.0
                try:  cc = float(row[12])
                except ValueError:  cc = 0.0
                    
                new_srec_row = [row[8][:8], cyear, row[9], row[10], ce, cc, row[13]]
                current_srec_data.append(new_srec_row)

    if ufname!='':
        stinfo = apply_update(stinfo, ufname)
    #cinfo = getcinfo(stinfo,cinfo)  
    cinfo = None
            
    return stinfo, cinfo


def apply_update(stinfo, ufname):
    """
    Reads an update file (CSV/Excel) and applies the new course results 
    to the existing student records in the stinfo dictionary.

    Args:
        stinfo (dict): The main dictionary holding all student records.
        ufname (str): The filename/path of the update file.

    Returns:
        dict: The updated stinfo dictionary.
    """

    if not ufname or not os.path.exists(ufname):
        print(f"Update file '{ufname}' not found or path is empty. Skipping update.")
        return stinfo

    try:  
        A = pd.read_excel(ufname)
    except Exception as e:
        print(f"Error reading update file {ufname}: {e}")
        return stinfo

    #A.dropna(axis=0, subset=[A.columns[1]], inplace=True) 
    ustnums = A.iloc[:, 1].astype(str).values  # Convert to NumPy array of strings
     # drop empty lines

    for i, record in enumerate(stinfo):
        student_id = record['sinfo'][1]
        ia = np.isin(ustnums, student_id)
        if not np.any(ia):  continue
        sstab = A[ia].reset_index(drop=True)

        srec_df: pd.DataFrame = record.get('srec', pd.DataFrame())
        ystats_df: pd.DataFrame = record.get('ystats')
        cyear = ystats_df['yr'].max() if ystats_df is not None and not ystats_df.empty else None
        new_rows_to_add = [] # List to hold new rows for appending

        for j in range(len(sstab)):
            ccode = str(sstab.iloc[j, 5]) + str(sstab.iloc[j, 6])
            newres_str = str(sstab.iloc[j, 9]).strip()
            
            match_indices = srec_df[srec_df['course'].str.contains(ccode, na=False)].index
            if match_indices.empty:
                new_row = {
                    'course': ccode, 
                    'yt': cyear, 
                    'perc': newres_str, 
                    'symbol': newres_str,
                    'cre': 0.0, 
                    'crt': 0.0, 
                    'coursen': 'Updated/New Course'
                }
                new_rows_to_add.append(new_row)

            else:
                if(student_id=='NDXVAY001'):
                    print(match_indices)

                ii = max(match_indices) # index in the DataFrame
                srec_df.loc[ii, 'perc'] = newres_str

                if 'symbol' in srec_df.columns:
                    srec_df.loc[ii, 'symbol'] = newres_str

                result_str = srec_df.loc[ii, 'perc'].strip()
                numeric_res = pd.to_numeric(result_str, errors='coerce')

            is_passing = (result_str.endswith('C') or result_str == 'PA' or (not np.isnan(numeric_res) and numeric_res >= 50))
            if is_passing:
                credit_total = srec_df.loc[ii, 'crt']
                srec_df.loc[ii, 'cre'] = credit_total
            else:
                srec_df.loc[ii, 'cre'] = 0.0

        if new_rows_to_add:
            new_df = pd.DataFrame(new_rows_to_add)
            common_cols = list(set(srec_df.columns) & set(new_df.columns))
            srec_df = pd.concat([srec_df, new_df[common_cols]], ignore_index=True)

        record['srec'] = srec_df

    return stinfo


def getcinfo(stinfo: Dict[int, StudentInfo], cinfo: Optional[CourseInfo] = None) -> CourseInfo:
    """
    Extracts unique course and credit information from all student records 
    and identifies courses with inconsistent credit counts.

    Args:
        stinfo (dict): The main dictionary holding all student records.
        cinfo (optional): Placeholder for general course info (not fully used here).

    Returns:
        dict: The updated cinfo (or a dictionary containing the extracted data).
    """
    
    all_srec_dataframes = []
    for record in stinfo:
        srec_df = record.get('srec')
        if isinstance(srec_df, pd.DataFrame) and not srec_df.empty:
            all_srec_dataframes.append(srec_df)

    if not all_srec_dataframes:  return []

    df = pd.concat(all_srec_dataframes, ignore_index=True)
    
    exclusion_values = {'CX', 'CR', 'EX'}
    perc_mask = ~df['perc'].isin(exclusion_values)
    length_mask = df['course'].astype(str).str.len() == 8
    df_filtered = df[perc_mask & length_mask].copy()

    unique_cols = ['course', 'yt', 'crt']
    df_filtered_unique = df_filtered.drop_duplicates(subset=unique_cols, keep='first')
    df_final = df_filtered_unique[unique_cols].copy()
    print(df_final)

    inconsistent_credits_check = df_final.groupby(['course']).agg(
        unique_credit_counts=('crt', 'nunique')
    ).reset_index()
    inconsistent_keys = inconsistent_credits_check.query('unique_credit_counts > 1')
    inconsistent_rows_credits = pd.merge(
        df_final, 
        inconsistent_keys[['course']], 
        on=['course'], 
        how='inner'
    ).sort_values(by=['course', 'yt', 'crt'])

    print("## Courses with Inconsistent Credit Counts ('crt') Across Years ##")
    print("These courses have the same code but were recorded with different credit values.")
    print(inconsistent_rows_credits)

    cinfo = df_final.values.tolist()
    return cinfo



if __name__ == '__main__':
    input_crs = "/Users/nicolls/proj/eleceng_matlab/feccheck/2024/CSV Electrical Engineering_20240214.csv"
    ufname = "/Users/nicolls/proj/eleceng/feccheck/fec2025_updates.xlsx"

    stinfo, cinfo = parsecrsinput(input_crs)
    stinfo2 = apply_update(stinfo, ufname)
    print(".")
