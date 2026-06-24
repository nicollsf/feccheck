#!/usr/bin/env python3
import json
import sys
import argparse
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "timetable_schedule.json")

PROGRAM_NAMES = {
    "EB009": "Mainstream Electrical Engineering (EB009)",
    "EB011": "Mainstream Mechatronics (EB011)",
    "EB022": "Mainstream Electrical & Computer Engineering (EB022)",
    "EB809": "ASPECT Electrical Engineering (EB809)",
    "EB811": "ASPECT Mechatronics (EB811)",
    "EB822": "ASPECT Electrical & Computer Engineering (EB822)"
}

def load_data():
    if not os.path.exists(DATABASE_PATH):
        print(f"Error: Database file not found at {DATABASE_PATH}.", file=sys.stderr)
        print("Please parse the Excel file first.", file=sys.stderr)
        sys.exit(1)
    with open(DATABASE_PATH, "r") as f:
        return json.load(f)

def clean_year(yr_str):
    # Map '1' to '1ST YEAR', etc.
    yr_str = str(yr_str).upper().strip()
    if yr_str in ['1', '1ST']:
        return '1ST YEAR'
    elif yr_str in ['2', '2ND']:
        return '2ND YEAR'
    elif yr_str in ['3', '3RD']:
        return '3RD YEAR'
    elif yr_str in ['4', '4TH']:
        return '4TH YEAR'
    elif yr_str in ['5', '5TH']:
        return '5TH YEAR'
    return yr_str

def main():
    parser = argparse.ArgumentParser(
        description="Query the 2026 EEE Course Timetable Schedule database.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples of use:
  python3 query_timetable.py --program EB009 --period 1
  python3 query_timetable.py --course MAM1020F
  python3 query_timetable.py --program EB022 --year 3 --semester 1
  python3 query_timetable.py --day MONDAY --period 3
        """
    )
    parser.add_argument("-p", "--program", help="Filter by program code (e.g., EB009, EB011, EB022, EB809, etc.)")
    parser.add_argument("-y", "--year", help="Filter by year (e.g., 1, 2, 3, 4, 5 or 1ST YEAR)")
    parser.add_argument("-s", "--semester", type=int, choices=[1, 2], help="Filter by semester (1 or 2)")
    parser.add_argument("-d", "--day", help="Filter by day (MONDAY, TUESDAY, etc.)")
    parser.add_argument("-t", "--period", help="Filter by period (1-9 or M)")
    parser.add_argument("-c", "--course", help="Filter by course code (e.g., EEE1008F)")
    
    args = parser.parse_args()
    
    # Check if any filters are specified
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)
        
    data = load_data()
    filtered = []
    
    target_year = clean_year(args.year) if args.year else None
    target_program = args.program.upper().strip() if args.program else None
    target_day = args.day.upper().strip() if args.day else None
    target_period = args.period.upper().strip() if args.period else None
    target_course = args.course.upper().strip() if args.course else None
    
    for slot in data:
        if target_program and slot["program"].upper() != target_program:
            continue
        if target_year and slot["year"].upper() != target_year:
            continue
        if args.semester and slot["semester"] != args.semester:
            continue
        if target_day and slot["day"].upper() != target_day:
            continue
        if target_period and slot["period"].upper() != target_period:
            continue
        if target_course and target_course not in slot["course_code"].upper():
            continue
        filtered.append(slot)
        
    if not filtered:
        print("No matching classes found.")
        sys.exit(0)
        
    # Sort results for display
    def sort_key(slot):
        prog = slot["program"]
        yr = slot["year"]
        sem = slot["semester"]
        per = slot["period"] or ""
        day = slot["day"]
        
        # Day index
        days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
        d_idx = days.index(day) if day in days else 99
        
        # Period index
        if per == 'M':
            p_val = 5.5
        else:
            try:
                p_val = float(per)
            except ValueError:
                p_val = 99.0
                
        return (prog, yr, sem, p_val, d_idx)
        
    filtered.sort(key=sort_key)
    
    # Print formatted output
    header = f"{'Program':<8} | {'Year':<8} | {'Sem':<3} | {'Period':<6} | {'Time':<8} | {'Day':<9} | {'Course':<9} | {'Details':<15}"
    print(header)
    print("-" * len(header))
    for slot in filtered:
        details_str = slot["details"] or ""
        p_name = slot["program"]
        print(f"{p_name:<8} | {slot['year']:<8} | {slot['semester']:<3} | {slot['period']:<6} | {slot['time']:<8} | {slot['day']:<9} | {slot['course_code']:<9} | {details_str:<15}")

if __name__ == "__main__":
    main()
