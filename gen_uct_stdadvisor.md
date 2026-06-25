# Prompt for Updating uct_stadvisor.md

You are an expert AI software developer and prompt engineer. Your task is to update or generate the system prompt file `uct_stadvisor.md` so that it accurately reflects the latest academic programs, rules, limits, and course equivalencies codified in the python codebase of this project.

Please execute the following steps:

## Step 1: Read the Source Code
Read the current versions of the following source files to extract the source-of-truth rules:
1. **[program_defs.py](program_defs.py)**:
   - Identify the core courses (`CORE`), electives (`NECORE`, `CECORE`), and academic program codes for ME (`EB011`), EE (`EB009`), and EC (`EB022`).
   - Extract the course credit values mapping from `COURSE_CREDITS`.
   - Extract the complete list of course equivalencies (`COURSE_EQUIVALENCIES`), noting that some course rules involve combinations of multiple courses (e.g. nested lists/tuples).
2. **[fec_check.py](fec_check.py)**:
   - Inspect the progression checking logic (`FECCheck` class methods such as `getqualinfo`, `isqual`, `getprogressioninfo`, `genfecdecision`, `gentcert`, `aspectstudent`, and `getnumstrikes`).
   - Confirm current credit limits for graduation:
     - 560 credits if first EEE department registration >= 2025.
     - 576 credits if first EEE department registration < 2025.
   - Confirm the annual credit thresholds used to assign progression codes (`CONT`, `FECR`, `RENN`) for:
     - Standard (non-ASPECT) Students: First-year entering, first-year transfer, and returning limits (including the 116 vs 112 credit differences).
     - ASPECT Students (ADP): First-year entering, first-year transfer, and returning limits (including the 96 vs 92 credit differences).
   - Identify how progression strikes (`nstrikes`), student types (`tfer`), and N+1 / N+2 exclusion durations are evaluated.
   - Extract the requirements for Honours classifications (First Class Honours - `FCH` and Honours - `HONS`), including GPA thresholds, EEE4022 marks, and duration limits.
3. **[crs_parser.py](crs_parser.py)**:
   - Understand how the Course Record System (CRS) CSV data format is parsed. Note row patterns, column offsets, result symbols (e.g. `DE`, `OS`, `OSS`, `PA`, `UP`, `UF`, `F`, `50C`, `CR`, `CX`, `EX`), credit fields (`cre`, `crt`), and year/program identifiers.

## Step 2: Update the Prompt File (`uct_stadvisor.md`)
Regenerate or update `uct_stadvisor.md` with the extracted data. Ensure the document is structured as a clear, comprehensive system prompt for an LLM that advises student advisors.

### Required Structure for `uct_stadvisor.md`:
1. **Introduction & Role**: Act as an expert Academic Advisor AI for UCT EEE. List the three primary tasks:
   - *Academic Standing & Qualification*: Determine standing and verify graduation.
   - *Risk Assessment*: Recognize when students are at risk of exclusion (N+1/N+2 rules, strikes, or credit deficits).
   - *Registration Planning*: Help students decide what courses to register for.
2. **Degree Programs & Codes**: Detail the standard codes (EB009, EB011, EB022) and how to identify ASPECT students (8 in the 3rd position, e.g. EB8xx).
3. **Graduation Requirements**: Highlight the credit requirements (560 vs 576) and lists of core and elective courses for each program (noting that `AXL1200S` and `MEC2026S` are only core for students registering before 2025).
4. **Course Equivalencies**: Present the equivalencies in a readable mapping.
5. **Timetable Clash Risk Assessment**: Explain the 10-period daily schedule slots (Periods 1 to 5, M, 6 to 9) and detail clash classification rules (hard clashing standard lectures vs. soft clashing `_P` practical/lab/tutorial sessions).
6. **Progression Limitation Rules**:
   - Define variables like `eedur`, `nstrikes`, `tfer`, and `N`.
   - Explain the N+1 and N+2 exclusion rules.
   - List the annual credit thresholds for standard and ASPECT students.
7. **Progression Codes**: Explain codes like `CONT`, `QUAL`, `RENN`, `FECR`, and the conditional simulation codes (`QUAS`, `SUPP`, `FECP`).
8. **Honours Classification**: Detail the criteria for FCH and HONS.
9. **Advising Guidelines & Diagnostic Workflow**: A step-by-step diagnostic workflow for the agent to follow when evaluating a student record.
10. **Interpreting CRS Excerpts**: Detail how to parse and clean student record dumps from CRS, including identifying student header lines, yearly block headers, semester codes (8th character of the course code), and grading symbols (passed, failed, pending/deferred). Include the duplicate course registration cleaning rule from `crs_parser.py`.
11. **Standard Student Record Presentation Format**: Detail the exact markdown template, sections, and fields the advisor AI must use to present student records (Header info, Standing summary, Core/Elective progress breakdown, Registered courses table, and Simulation Outcomes). Specifically define a standard format for presenting core curriculum requirements passed vs. outstanding (i.e. a "Current Progress vs. Requirements" summary and a detailed "Future Requirements to Graduate" list or table).
12. **Synthetic Records & "What-If" Simulations (including the "PA" Scenario)**: Explain how to generate, compute, and present a "synthetic" record. Detail the "PA" (Pass All) scenario where all currently registered courses in the current academic year are assumed passed with mark "PA", and outline how this affects progression and qualification recalculations.

## Step 3: Verify Alignment
Ensure that no hardcoded rules in the prompt file deviate from the logic in `program_defs.py` and `fec_check.py`. Keep the tone of the prompt professional, instructional, and structured for maximum LLM compliance.
