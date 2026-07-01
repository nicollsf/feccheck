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

1. **MATLAB Legacy**: Respect the sequential structure and existing variables.
2. **Pandas Mutability**: Be careful with mutations of `srec` and `ystats` in simulation functions.
3. **Course Equivalencies**: Ensure course equivalencies are defined symmetrically (e.g., if `AXL1200S` satisfies `ASL1200S`, then `ASL1200S` must also have an equivalency mapping to satisfy `AXL1200S`).
4. **Duplicate Course Dumps**: De-duplicate rows in `crs_parser.py` to prevent credit double-counting.
5. **Curriculum Year Specs**: The checker selects specifications from `program_defs.py` dynamically based on the student's entry year (`yfdreg`), supporting distinct specifications for **2026 or later**, **2025**, and **2018-2024** cohorts.
6. **QUAS for Practical Training**: If a student is *only* missing the 0-credit core courses `EEE1000X` and/or `EEE3000X` but has met all other academic requirements and credits, they are coded as **`QUAS`** with the message `"Outstanding Practical Training"` instead of being subjected to normal credit-based exclusion limits.
7. **Explanatory Comments Column**: The Excel spreadsheets include a trailing `comments` column showing the curriculum spec year applied to the student and a trace of all across-variant course equivalencies used.

## 6. Student Advising Workflow & Priming
In addition to the batch FEC simulations run via Python, the system supports interactive student advising via Gemini:

1. **[uct_stadvisor.md](file:///Users/nicolls/proj/eleceng/feccheck/uct_stadvisor.md)**: A comprehensive, detailed system prompt for an LLM that serves as the instruction set for a Custom Gem or primed chat. It instructs the AI on how to interpret CRS dumps, check requirements, compute academic standing, and recommend registrations.
2. **[advising_workflow_guide.md](file:///Users/nicolls/proj/eleceng/feccheck/advising_workflow_guide.md)**: Guide for EEE advisors explaining how to setup the Custom Gem and conduct daily advising workflow.
3. **[gen_uct_stdadvisor.md](file:///Users/nicolls/proj/eleceng/feccheck/gen_uct_stdadvisor.md)**: Developer specifications detailing how to regenerate/update `uct_stadvisor.md` from the Python source-of-truth logic when rules change.

**Alignment Requirement**: The LLM prompt in `uct_stadvisor.md` must be kept perfectly in sync with the logic in `program_defs.py` and `fec_check.py` to prevent advising discrepancy.