# AI Induction Primer: FEC Check

Welcome to the `feccheck` project. Please read this document to understand the codebase architecture, data structures, and business logic before making changes.

## 1. Project Purpose
This project automates and simulates progression decisions for the Faculty Examination Committee (FEC) in the Electrical Engineering (EEE) department. 

Because university progression rules are complex, students often register irrationally (e.g., believing they will graduate when they are missing core requirements). This tool runs "What-If" simulations to predict a student's progression status under various scenarios (e.g., what if they pass all current courses? What if they fail their supplementary exams?).

## 2. Codebase Architecture
The project is divided into four main Python files:

1. **`runme.py`**: The entry point. Loads the CSV, runs the parser, initializes the checker, and triggers the output generation.
2. **`crs_parser.py`**: Ingests legacy, multi-line, report-like CSV dumps from the university's Course Record System (CRS). It structures this messy data into Pandas DataFrames.
3. **`program_defs.py`**: Contains the hardcoded curriculum rules for three programs: ME (`EB011`), EE (`EB009`), and EC (`EB022`). It defines core courses (`core`), list-based electives (`necore`), credit-based electives (`cecore`), and course equivalencies.
4. **`fec_check.py`**: The core logic engine (`FECCheck` class). It evaluates graduation eligibility (`isqual`), simulates progression scenarios (`gencondprogs`), and writes the results to an Excel workbook with multiple sheets.

## 3. Core Data Structures
The data flows through the system primarily as a list of dictionaries called `stinfo` (Student Info). A typical student record (`strec`) contains:

* **`sinfo`**: A list of basic demographic and program info (e.g., ID, Name, Academic Program).
* **`ystats`**: A `pandas.DataFrame` containing yearly aggregations. Key columns: `yr` (Year), `Term` (Term GPA), `Cum` (Cumulative GPA), `TE` (Term Credits), `CE` (Cumulative Credits), `pcode` (Progression Code).
* **`srec`**: A `pandas.DataFrame` detailing every course registration. Key columns: `course` (Code), `yt` (Year Taken), `perc` (Mark/Result), `symbol` (Result Symbol), `cre` (Credits Earned), `crt` (Credits Total).

## 4. Key Business Logic & Scenarios

### Progression Codes
* **`CONT`**: Continue (Good standing).
* **`QUAL`**: Qualify (Graduating). Requires all core/elective rules met AND total credits > required curriculum credits (usually 560 or 576).
* **`FECR` / `RENN`**: Academic exclusion or readmission required (due to failing N+1/N+2 rules or low credits).
* **`SUPP` / `FECP` / `QUAS`**: Conditional states depending on passing supplementary exams.

### Simulation Scenarios (Excel Tabs)
* **`Curr`**: Current actual status.
* **`PY`**: Predicts status assuming the student passes *all* currently registered courses (100% pass rate). Used heavily for "Curriculum Cleanup" to detect false graduation hopes.
* **`PS2`**: Assumes all 2nd-semester courses are passed.
* **`PsPremB` / `PsPremW`**: Best/Worst case passes if supplementary exams are passed.
* **`FsPremB` / `FsFrem`**: Scenarios if supplementary exams are failed.

## 5. Important Quirks & Guidelines for AI Agents

1. **MATLAB Legacy**: This codebase was ported from a legacy MATLAB script. You will see artifacts like variable names (`ia`, `ib`, `pip`), 1-based indexing comments, and logic structured sequentially rather than in highly nested objects. Respect the existing code style unless explicitly asked to refactor.
2. **Pandas Mutability**: The simulation methods in `fec_check.py` (e.g., `flagsuppspassed`, `flagpassedwithmark`) work by creating `deep=True` copies of a student's `ystats` and `srec` DataFrames, mutating the marks to simulate a pass/fail, and recalculating the GPAs/credits. Be very careful with pandas `.loc` vs `.iloc` when modifying these frames.
3. **Course Equivalencies**: Course equivalencies in `program_defs.py` are complex. A requirement might be satisfied by a single alternative string (e.g., `'MAM1000W'`), or a *list* of courses that must ALL be passed (e.g., `['EEE4006C', 'EEE4051C']`). Always account for nested lists when doing equivalency lookups.
4. **Duplicate Course Dumps**: The raw CRS CSV sometimes prints the exact same year of courses multiple times if a student is dual-registered or changing programs. `crs_parser.py` drops these duplicates to prevent credit-count inflation.