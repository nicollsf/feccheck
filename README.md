# feccheck

<<<<<<< HEAD
Python code for "estimating" student progression status under various scenarios.

This tool is specifically designed for the Electrical Engineering department (EEE) to automate and simulate Faculty Examination Committee (FEC) progression decisions.

## System Overview

The codebase is divided into three primary modules:

1. **`fec_check.py` (Core Logic & Output)**
   - Defines the `FECCheck` class.
   - Manages the entire data flow: taking parsed student records, determining if they have satisfied core requirements (`gentcert`), and simulating multiple progression scenarios.
   - Runs "What-If" scenarios (e.g., what happens to a student's status if they pass all their current courses, or if they pass/fail their supplementary exams).
   - Outputs an Excel file with separate sheets for each simulated scenario (e.g., `Curr`, `PY`, `PS2`, `PsPremB`, `FsFrem`) and a final legacy output table.

2. **`crs_parser.py` (Data Ingestion)**
   - Responsible for parsing the raw multi-line CSV dumps from the university's CRS (Course Record System).
   - Extracts basic student info (`sinfo`), yearly summary statistics (`ystats`), and granular course records (`srec`).
   - Includes an `apply_update` feature to overlay manual/updated marks from an Excel file (e.g., late results) onto the existing student records before processing.

3. **`program_defs.py` (Curriculum Rules)**
   - Contains the hardcoded curriculum rules for programs: Mechanical-Electrical (`EB011`), Electrical (`EB009`), and Electrical-Computer (`EB022`).
   - Defines core courses (`CORE`), elective courses by number (`NECORE`), and elective courses by credit total (`CECORE`).
   - Provides a comprehensive `COURSE_EQUIVALENCIES` list (e.g., mapping old course codes to new ones, or listing acceptable alternatives like `MAM1020F` vs `MAM1000W`).

## Key Concepts & Scenarios

The system checks various thresholds (e.g., N+1, N+2 rules, total credits, GPA) to assign progression codes:
* **CONT**: Continue
* **QUAL**: Qualify (Graduating)
* **RENN / FECR**: Progression defaults (Renew / Readmission required)
* **SUPP / FECP / QUAS**: Conditional states depending on the outcome of Supplementary/Deferred exams.

The simulations generated in the Excel output include:
* `Curr`: Current progression status.
* `PY`: Assumes all current year courses are passed.
* `PS2`: Assumes all second-semester courses are passed.
* `PsPremB` / `PsPremW`: Best/worst case scenarios if supplementary/deferred exams are passed.
* `FsPremB` / `FsFrem`: Scenarios if supplementary exams are failed.

## Notes for Developers and AI Assistants

* **MATLAB Legacy**: This codebase is a port of a legacy MATLAB script. You may notice artifacts of this history, such as 1-based indexing comments, variables named similarly to MATLAB cell arrays/structs, and certain logic patterns preserved to maintain strict output parity with the old system.
* **Primary Data Structure (`stinfo`)**: Data is heavily passed around as a list of dictionaries (`stinfo`). Each student record typically contains:
  - `sinfo`: Basic array of student metadata (ID, Name, Academic Program).
  - `ystats`: A `pandas.DataFrame` containing yearly aggregations (GPA, Term Credits, Cum Credits).
  - `srec`: A `pandas.DataFrame` detailing every course registration, mark (`perc`), symbol, and credits earned.
* **Data Modification**: Helper methods in `FECCheck` (like `flagsuppspassed` or `flagpassedwithmark`) create deep copies of a student's `ystats` and `srec` DataFrames, mutate them to simulate outcomes, and recalculate intermediate statistics like Term/Cumulative GPAs.
* **Dependencies**: Heavy reliance on `pandas` for tabular data manipulation, and `openpyxl`/`xlsxwriter` for formatted Excel reporting with header comments.
=======
Python code for estimating student progression status under different scenarios.
>>>>>>> 1a1f2e0a2c465e8e2a3e2afe84fc5dd413a5cebd
