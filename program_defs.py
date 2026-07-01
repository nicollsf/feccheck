from typing import List, Dict, Union, Any

# --- Programme Definitions ---

ME_CODE = 'EB011'
EE_CODE = 'EB009'
EC_CODE = 'EB022'

# --- 2026 Core & Electives (Curriculum Year >= 2026) ---
ME_CORE_2026 = [
    'CSC1015F', 'EEE1008F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 
    'CSC1016S', 'EEE1009S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048S', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'PHY2010S', 
    'EEE3088F', 'EEE3090F', 'EEE3091F', 'EEE3092F', 'MEC2047F', 
    'EEE3094S', 'EEE3096S', 'EEE3099S', 'MEC2045S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
ME_NECORE_2026 = [
    [2, 'EEE4117F', 'EEE4118F', 'EEE4119F'] 
]
ME_CECORE_2026 = [
    [48, 'EEE4117F', 'EEE4118F', 'EEE4119F', 'EEE4114F', 'EEE4120F', 'HUB4049F']
]

EE_CORE_2026 = [
    'CSC1015F', 'EEE1008F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 
    'CSC1016S', 'EEE1009S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048S', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'PHY2010S', 
    'EEE3088F', 'EEE3089F', 'EEE3090F', 'EEE3091F', 'EEE3092F', 
    'EEE3093S', 'EEE3094S', 'EEE3098S', 'EEE3100S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
EE_NECORE_2026 = [
    [1, 'EEE4126F', 'EEE4118F', 'EEE4121F']
]
EE_CECORE_2026 = [
    [48, 'EEE4126F', 'EEE4118F', 'EEE4121F', 'EEE4114F', 'EEE4117F', 'HUB4049F']
]

EC_CORE_2026 = [
    'CSC1015F', 'EEE1008F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 
    'CSC1016S', 'EEE1009S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048S', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'PHY2010S', 
    'CSC2001F', 'EEE3088F', 'EEE3089F', 'EEE3090F', 'EEE3092F', 
    'EEE3096S', 'EEE3097S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
EC_NECORE_2026 = [
    [2, 'CSC2002S', 'EEE3093S', 'EEE3094S'], 
    [2, 'EEE4114F', 'EEE4118F', 'EEE4120F', 'EEE4121F']
]
EC_CECORE_2026 = [
    [48, 'EEE4114F', 'EEE4118F', 'EEE4120F', 'EEE4121F',
    'CSC3002F', 'CSC3003S', 'CSC3021F', 'CSC3022F', 'CSC3022H', 'CSC3023F', 'HUB4049F']
]

# --- 2025 Core & Electives (Curriculum Year == 2025) ---
ME_CORE_2025 = [
    'CSC1015F', 'EEE1006F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 
    'ASL1200S', 'CSC1016S', 'EEE1007S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048F', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'CON2026S', 'PHY2010S', 
    'EEE3088F', 'EEE3090F', 'EEE3091F', 'EEE3092F', 'MEC2047F', 
    'EEE3094S', 'EEE3096S', 'EEE3099S', 'MEC2045S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
ME_NECORE_2025 = ME_NECORE_2026
ME_CECORE_2025 = [
    [48, 'EEE4117F', 'EEE4118F', 'EEE4119F', 'EEE4114F', 'EEE4120F', 'HUB4045F', 'HUB2005F', 'EEE4123C']
]

EE_CORE_2025 = [
    'CSC1015F', 'EEE1006F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 
    'ASL1200S', 'CSC1016S', 'EEE1007S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048F', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'CON2026S', 'PHY2010S', 
    'EEE3088F', 'EEE3089F', 'EEE3090F', 'EEE3091F', 'EEE3092F', 
    'EEE3093S', 'EEE3094S', 'EEE3098S', 'EEE3100S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
EE_NECORE_2025 = EE_NECORE_2026
EE_CECORE_2025 = [
    [48, 'EEE4126F', 'EEE4118F', 'EEE4121F', 'EEE4114F', 'EEE4117F', 'HUB4045F', 'HUB2005F', 'EEE4123C']
]

EC_CORE_2025 = [
    'CSC1015F', 'EEE1006F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 
    'ASL1200S', 'CSC1016S', 'EEE1007S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048F', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'CON2026S', 'PHY2010S', 
    'CSC2001F', 'EEE3088F', 'EEE3089F', 'EEE3090F', 'EEE3092F', 
    'EEE3096S', 'EEE3097S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
EC_NECORE_2025 = EC_NECORE_2026
EC_CECORE_2025 = [
    [48, 'EEE4114F', 'EEE4118F', 'EEE4120F', 'EEE4121F',
    'CSC3002F', 'CSC3003S', 'CSC3021F', 'CSC3022F', 'CSC3022H', 'CSC3023F', 'HUB4045F', 'HUB2005F', 'EEE4123C']
]

# --- 2022-2024 Core & Electives (Curriculum Year <= 2024) ---
ME_CORE_2022_2024 = ME_CORE_2025
ME_NECORE_2022_2024 = ME_NECORE_2025
ME_CECORE_2022_2024 = [
    [48, 'EEE4117F', 'EEE4118F', 'EEE4119F', 'EEE4114F', 'EEE4120F', 'HUB4045F', 'HUB2005F', 'EEE4123C', 'EEE2051L']
]

EE_CORE_2022_2024 = EE_CORE_2025
EE_NECORE_2022_2024 = EE_NECORE_2025
EE_CECORE_2022_2024 = [
    [48, 'EEE4126F', 'EEE4118F', 'EEE4121F', 'EEE4114F', 'EEE4117F', 'HUB4045F', 'EEE4123C', 'EEE4122C', 'EEE4105C']
]

EC_CORE_2022_2024 = EC_CORE_2025
EC_NECORE_2022_2024 = EC_NECORE_2025
EC_CECORE_2022_2024 = [
    [48, 'EEE4114F', 'EEE4118F', 'EEE4120F', 'EEE4121F',
    'CSC3002F', 'CSC3003S', 'CSC3021F', 'CSC3022F', 'CSC3022H', 'CSC3023F', 'HUB4045F', 'EEE4122C', 'EEE4105C']
]

# Combine all programme specifications into a single configurations list.
# Match occurs by 'code' and student's entry year ('start_year' <= yfdreg <= 'end_year').
PROGRAM_SPECS: List[Dict[str, Any]] = [
    # Mechatronics (ME)
    {
        'prog': 'ME', 
        'code': ME_CODE,
        'start_year': 2026,
        'end_year': 9999,
        'core': ME_CORE_2026,  
        'necore': ME_NECORE_2026,  
        'cecore': ME_CECORE_2026
    },
    {
        'prog': 'ME', 
        'code': ME_CODE,
        'start_year': 2025,
        'end_year': 2025,
        'core': ME_CORE_2025,  
        'necore': ME_NECORE_2025,  
        'cecore': ME_CECORE_2025
    },
    {
        'prog': 'ME', 
        'code': ME_CODE,
        'start_year': 0,
        'end_year': 2024,
        'core': ME_CORE_2022_2024,  
        'necore': ME_NECORE_2022_2024,  
        'cecore': ME_CECORE_2022_2024
    },
    # Electrical Engineering (EE)
    {
        'prog': 'EE', 
        'code': EE_CODE,
        'start_year': 2026,
        'end_year': 9999,
        'core': EE_CORE_2026,  
        'necore': EE_NECORE_2026,  
        'cecore': EE_CECORE_2026
    },
    {
        'prog': 'EE', 
        'code': EE_CODE,
        'start_year': 2025,
        'end_year': 2025,
        'core': EE_CORE_2025,  
        'necore': EE_NECORE_2025,  
        'cecore': EE_CECORE_2025
    },
    {
        'prog': 'EE', 
        'code': EE_CODE,
        'start_year': 0,
        'end_year': 2024,
        'core': EE_CORE_2022_2024,  
        'necore': EE_NECORE_2022_2024,  
        'cecore': EE_CECORE_2022_2024
    },
    # Electrical and Computer Engineering (EC)
    {
        'prog': 'EC', 
        'code': EC_CODE,
        'start_year': 2026,
        'end_year': 9999,
        'core': EC_CORE_2026,  
        'necore': EC_NECORE_2026,  
        'cecore': EC_CECORE_2026
    },
    {
        'prog': 'EC', 
        'code': EC_CODE,
        'start_year': 2025,
        'end_year': 2025,
        'core': EC_CORE_2025,  
        'necore': EC_NECORE_2025,  
        'cecore': EC_CECORE_2025
    },
    {
        'prog': 'EC', 
        'code': EC_CODE,
        'start_year': 0,
        'end_year': 2024,
        'core': EC_CORE_2022_2024,  
        'necore': EC_NECORE_2022_2024,  
        'cecore': EC_CECORE_2022_2024
    }
]

# Standard credit values for core and elective courses (source of truth for advising)
COURSE_CREDITS: Dict[str, int] = {
    'ASL1200S': 16,
    'AXL1001S': 16,
    'AXL1200S': 8,
    'AXL1301S': 16,
    'CAS1001S': 16,
    'CAS2001S': 16,
    'CML4607F': 10,
    'CML4607Z': 10,
    'COMPSTUD': 18,
    'CON2026S': 8,
    'CSC1015F': 18,
    'CSC1015S': 18,
    'CSC1016S': 18,
    'CSC2001F': 24,
    'CSC2002S': 24,
    'CSC3002F': 36,
    'CSC3003S': 36,
    'CSC3021F': 36,
    'CSC3022F': 36,
    'CSC3022H': 36,
    'CSC3023F': 36,
    'EEE1000X': 0,
    'EEE1006F': 12,
    'EEE1007S': 12,
    'EEE1008F': 12,
    'EEE1009S': 12,
    'EEE2044S': 16,
    'EEE2045F': 16,
    'EEE2046F': 16,
    'EEE2046S': 16,
    'EEE2047S': 16,
    'EEE2048F': 8,
    'EEE2048S': 8,
    'EEE2051L': 8,
    'EEE3000X': 0,
    'EEE3088F': 8,
    'EEE3089F': 16,
    'EEE3090F': 16,
    'EEE3091F': 16,
    'EEE3092F': 16,
    'EEE3093S': 16,
    'EEE3094S': 16,
    'EEE3096S': 16,
    'EEE3097S': 8,
    'EEE3098S': 8,
    'EEE3099S': 8,
    'EEE3100S': 16,
    'EEE4006C': 8,
    'EEE4022F': 40,
    'EEE4022S': 40,
    'EEE4051C': 8,
    'EEE4086F': 16,
    'EEE4087F': 16,
    'EEE4088F': 8,
    'EEE4089F': 16,
    'EEE4090F': 16,
    'EEE4093F': 16,
    'EEE4099F': 16,
    'EEE4104C': 8,
    'EEE4105C': 10,
    'EEE4113F': 16,
    'EEE4114F': 16,
    'EEE4117F': 16,
    'EEE4118F': 16,
    'EEE4119F': 16,
    'EEE4120F': 16,
    'EEE4121F': 16,
    'EEE4122C': 8,
    'EEE4123C': 8,
    'EEE4124C': 8,
    'EEE4125C': 16,
    'EEE4126F': 16,
    'END1019L': 18,
    'END1019P': 18,
    'END1019Z': 18,
    'HUB2005F': 8,
    'HUB4045F': 12,
    'HUB4049F': 16,
    'MAM1000W': 36,
    'MAM1020F': 18,
    'MAM1020S': 18,
    'MAM1021F': 18,
    'MAM1021S': 18,
    'MAM2083F': 16,
    'MAM2083S': 16,
    'MAM2084F': 16,
    'MAM2084S': 16,
    'MEC1003F': 8,
    'MEC1009F': 16,
    'MEC1009S': 16,
    'MEC2023F': 16,
    'MEC2026S': 8,
    'MEC2045S': 16,
    'MEC2047F': 16,
    'MEC4063C': 8,
    'PHY1012F': 18,
    'PHY1012S': 18,
    'PHY1013F': 18,
    'PHY1013S': 18,
    'PHY2010S': 16,
}

# Additional courses not yet specified that contribute to core requirements.
ADDITIONAL_AVAILABLE_COURSES: List[str] = []

# Equivalent courses structure: the first element is the required course, 
# and the rest are courses that satisfy that requirement. An inner list 
# means ALL courses inside must be satisfied.
#
# Note on suffix variants: Where a course code doesn't end with a term suffix 
# (e.g., F: first semester, S: second semester, W: whole year, A: first term, 
# C: third term, Z: unspecified term, etc.), it is considered equivalent to all 
# other variants where the term suffix is specified.
CourseEquivsList = List[List[Union[str, List[str]]]]

COURSE_EQUIVALENCIES: CourseEquivsList = [
    ['AXL1200S', 'AXL1001S', 'CAS1001S', 'CAS2001S', 'AXL1301S', 'ASL1200S'],
    ['ASL1200S', 'AXL1200S', 'AXL1001S', 'CAS1001S', 'CAS2001S', 'AXL1301S'],
    ['CSC1015F', 'CSC1015S', 'EEE1003W'],
    ['CSCxxxxx', 'CSC3022H', 'CSC3023F'],
    ['EEE1005W', 'EEE1004W', ['EEE1006F', 'EEE1007S']],
    ['EEE1007S', 'EEE1009S', 'EEE1005W'],
    ['EEE1006F', 'EEE1008F', 'EEE1005W'],
    ['EEE1009S', 'EEE1007S'],
    ['EEE1008F', 'EEE1006F'],
    ['MAM1020F', 'MAM1020S', 'MAM1023F', 'MAM1023S', 'MAM1017F', 'MAM1017S', 'MAM1003W', 'MAM1000W', 'END1017F', 'END1017S', 'END1007W', 'END1020F', 'END1020S'],
    ['MAM1021S', 'MAM1021F', 'MAM1024F', 'MAM1024S', 'MAM1018S', 'MAM1018F', 'MAM1003W', 'MAM1000W', 'END1018S', 'END1007W', 'END1021S'],
    ['MAM1042S', 'MAM1045S', 'CSC1016S'],
    ['PHY1012F', 'PHY1012S', 'PHY1014F', 'PHY1014S', 'PHY1010W', 'PHY1011W', 'PHY1031F'],
    ['PHY1013S', 'PHY1013F', 'PHY1015F', 'PHY1015S', 'PHY1010W', 'PHY1011W', 'PHY1032S'],
    ['EEE2036S', 'EEE2036F', 'MAM2081W', 'EEE2036SEWA', 'STA2004F', 'STA2030S', 'EEE3092F'],
    ['EEE2038W', 'EEE2032F'],
    ['EEE3069W', 'EEE3069WEWA', 'EEE3094S'],
    ['EEE2039W', 'EEE2037W', 'EEE2033S'],
    ['MAM2083F', 'MAM2083S', 'MAM2080W', 'MAM2085F', 'MAM2085S'],
    ['MAM2084S', 'MAM2084F', 'MAM2080W'],
    ['MAM2084F', 'MAM2084S'],
    ['EEE1006F', 'EEE1005W'],
    ['EEE1007F', 'EEE1005W'],
    ['EEE3017W', 'EEE3064W'],
    ['EEE2035F', 'EEE2047S'],
    ['EEE2047S', 'EEE2035F'],
    ['EEE3055W', 'EEE3055F'],
    ['EEE3073S', 'EEE2048F'],
    ['EEE3031S', 'EEE3091F'],
    ['MEC2026S', 'MEC2026F', 'CON2026S'],
    ['CON2026S', 'MEC2026S', 'MEC2026F'],
    ['MEC2023F', 'MEC2023S', 'MEC2047F', 'MEC2047S'],
    ['EEE2044S', 'EEE2038W'],
    ['EEE2045F', 'EEE2040F'],
    ['EEE2046F', 'EEE2046S'],
    ['EEE3090F', 'EEE3068F'],
    ['EEE3091F', 'EEE3031S'],
    ['EEE2048F', 'EEE2048S', 'EEE3073S'],
    ['EEE2048S', 'EEE2048F'],
    ['EEE3092F', 'EEE3086F'],
    ['EEE3093S', 'EEE3083F', 'EEE3084W', 'EEE3085S'],
    ['EEE3094S', 'EEE3069W', 'EEE3081F', 'EEE3082S'],
    ['EEE3096S', 'EEE3074W'],
    ['EEE3100S', 'EEE3057S'],
    ['EEE4114F', 'EEE4001F'],
    ['EEE4006C', 'EEE4006F', 'EEE4125C'],
    ['EEE4113F', 'EEE4036C', 'EEE4036A'],
    ['EEE4051C', 'EEE4051F', 'EEE4125C'],
    ['EEE4120F', 'EEE4084F'],
    ['EEE4086F', 'EEE4086F'],
    ['EEE4121F', 'EEE4087F'],
    ['EEE4122C', 'EEE4088F'],
    ['EEE4125C', ['EEE4006C', 'EEE4051C']],
    ['EEE4115F', 'EEE4089F'],
    ['EEE4116F', 'EEE4090F'],
    ['EEE4118F', 'EEE4093F'],
    ['EEE4117F', 'EEE4099F'],
    ['EEE4123C', 'EEE4104C'],  
    ['EEE4126F', 'EEE4115F'],
    ['MEC1009F', 'MAM1042S'],
    ['MEC1009F', 'MEC1009S'],
    ['MEC2049F', 'MEC2025F'],
    ['MEC2047F', 'MEC2023F', 'MEC2023S', 'MEC2047S'],
    ['EEE4022S', 'EEE4022F'],
    ['EEE4036C', 'EEE4036A', 'EEE4113C'],
    ['MEC4022Z', 'MEC4044Z', 'MEC4054Z'],
    ['MEC3035S', 'MEC3035F'],
    ['MEC4063C', 'MEC4044Z', 'MEC4054Z', 'EEE4124C'],
    ['EEE4124C', 'MEC4063C'],
    ['COMPSTUD', 'ACC1006F', 'AGE1002S', 'ANS2401L', 'AST1000F', 'AXL1100S', 'AXL1400F', 'AXL1401S', 'BIO1004S', 'BUS1007S', 'BUS1036F', 'BUS1036S', 'BUS2010F', 'BUS2010S', 'ECO1006F', 'ECO1007F', 'ECO1007S', 'ECO1010F', 'ECO1010S', 'ECO1011F', 'ECO1011S', 'ECO2007S', 'EGS1003S', 'ELL1016S', 'END1019L', 'END1019P', 'END1019Z', 'END1023S', 'FAM1000L', 'FAM1000S', 'FAM1001P', 'FTX1005S', 'FTX2000S', 'GEO1009F', 'HST1014S', 'HST2034P', 'MUZ1339H', 'MUZ1381H',  'PHI1010S', 'PHI1024F', 'PHI1025F', 'PHI2012F', 'PHI2040S', 'PHI2043F', 'PHI2043P', 'PHI2043S', 'PSY1004F', 'REL1006S', 'SLL1002F', 'SLL1002L', 'SLL1002P', 'SLL1002S', 'SLL1016S', 'SLL1018S', 'SLL1058F', 'SLL1060F', 'SLL1062F', 'SLL1062L', 'SLL1063S', 'SLL1064F', 'SLL1097S', 'SLL1101F', 'SLL2060F', 'SLL3060F', 'SOC1005J'],
    ['CML4607F', 'CML4607Z'],
    ['CML4607F', 'MEC4022Z']
]





# Prerequisites
# For each entry taking the first course requires that all the courses that
# follow have been done.  If any element contains a set then at least one
# in the set must have been done.
#
# Second-year students may not register for EEE3073S
# EEE4022:  All 1st, 2nd, 3rd year core courses and 32 credits max
# MEC2025F:  or DP for MAM1003W and PHY1010W
# MEC2026S:  third year
# MEC3031S:  and MEC2020W or equivalent
# MEC3035S:  MAM2082F?
# MEC4063C:  third year
COURSE_PREREQUISITES: List[List[Union[str, List[str]]]] = [
    ['MAM1021', 'MAM1020'],
    ['PHY1013', ['PHY1012', 'PHY1014']],
    ['EEE2035F', 'MAM1021'],
    ['EEE2038W', 'MAM1021', 'PHY1013'],
    ['EEE2039W', ['CSC1015', 'CSC1017', 'MAM1021', 'PHY1013']],
    ['MAM2083', ['MAM1003W', 'MAM1020'], 'MAM1021'],
    ['MAM2084', 'MAM1021'],
    ['MEC2043F', 'PHY1012', 'PHY1013'],
    ['EEE3017W', 'EEE2039W'],
    ['EEE3031S', 'EEE2038W'],
    ['EEE3061W', 'EEE2038W', 'EEE2039W', 'EEE2031S'],
    ['EEE3068F', 'EEE2038W', 'EEE2039W'],
    ['EEE3069W', 'MAM2084', 'EEE2035F', 'EEE2038W', 'EEE2039W'],
    ['MEC2023', 'MAM1021', 'MAM1042S', 'PHY1012', 'PHY1013'],
    ['MEC2025F', 'MAM1042S', 'MAM1020', 'PHY1012S'],
    ['MEC3031S', 'MEC2023', 'MEC2025F'],
    ['EEE4006F', 'EEE3073S'],
    ['EEE4036C', 'EEE3083F', ['EEE3069W', 'EEE3086F', 'EEE3057S']],
    ['EEE4051F', 'EEE2038W', 'EEE2039W', 'EEE3073S', 'MAM2084'],
    ['EEE4093F', 'EEE3069W'],
    ['EEE4099F', ['EEE3031S', 'EEE3057S']],
    # 2026 Core & Service Course Prerequisites (from EEE_cdesc.pdf)
    ['EEE2041F', ['PHY1013', 'PHY1004', 'PHY1032'], ['MAM1021', 'MAM1004', 'MAM1008', 'MAM1000W']],
    ['EEE2042S', ['MAM1021', 'MAM1004', 'MAM1008', 'MAM1000W'], ['PHY1013', 'PHY1004', 'PHY1032'], 'EEE2041F'],
    ['EEE2044S', ['MAM1020', 'MAM1023'], ['PHY1013', 'PHY1015'], 'EEE1007S'],
    ['EEE2045F', 'EEE1006F'],
    ['EEE2046F', 'EEE1006F', 'CSC1015F'],
    ['EEE2046S', 'EEE1006F', 'CSC1015F'],
    ['EEE2047S', ['MAM1021', 'MAM1024']],
    ['EEE2050F', 'CSC1015F', 'EEE2042S'],
    ['EEE3088F', ['EEE2045F', 'EEE2046F', 'EEE2046S']],
    ['EEE3089F', 'PHY2010S', 'MAM2083'],
    ['EEE3090F', 'EEE2045F', 'EEE2047S'],
    ['EEE3091F', 'EEE2044S'],
    ['EEE3092F', 'EEE2047S', 'MAM2083'],
    ['EEE3093S', ['EEE2046F', 'EEE2046S']],
    ['EEE3094S', 'EEE2045F', 'EEE2047S', 'MAM2084'],
    ['EEE3095S', 'EEE2050F'],
    ['EEE3096S', ['EEE2046F', 'EEE2046S']],
    ['EEE3097S', 'EEE3088F'],
    ['EEE3098S', 'EEE3088F'],
    ['EEE3099S', 'EEE3088F'],
    ['EEE3100S', 'EEE2044S'],
    ['EEE4022S', ['EEE4114F', 'EEE4126F', 'EEE4117F', 'EEE4118F', 'EEE4121F', 'EEE4120F', 'EEE4119F']],
    ['EEE4022F', ['EEE4114F', 'EEE4126F', 'EEE4117F', 'EEE4118F', 'EEE4121F', 'EEE4120F', 'EEE4119F']],
    ['EEE4113F', ['EEE3097S', 'EEE3098S', 'EEE3099S']],
    ['EEE4114F', ['EEE3092F', 'EEE3094S']],
    ['EEE4117F', 'EEE3091F'],
    ['EEE4118F', 'EEE3094S'],
    ['EEE4119F', 'MEC2047F', 'MEC2045S', 'EEE3094S'],
    ['EEE4120F', 'EEE3096S'],
    ['EEE4121F', 'EEE3093S'],
    ['EEE4124C', 'EEE3088F'],
    ['EEE4125C', ['EEE3097S', 'EEE3098S', 'EEE3099S']],
    ['EEE4126F', 'EEE3100S']
]

# Corequisites
COURSE_COREQUISITES: List[List[Union[str, List[str]]]] = [
    ['PHY1012F', ['MAM1020F', 'MAM1020S']],
    ['PHY1012S', ['MAM1020F', 'MAM1020S']],
    ['PHY1013F', ['MAM1020F', 'MAM1020S']],
    ['PHY1013S', ['MAM1020F', 'MAM1020S']],
    ['EEE2035F', ['MAM2083F', 'MAM2083S']],
    ['EEE4006F', 'EEE4051F']
]

# Timetable Semester 1 (slots x days grid)
TIMETABLE_SEMESTER_1: List[List[List[str]]] = [
    # Slot 1 (Period 1)
    [
        ['EEE4117F', 'MAM1020F', 'MAM1023F', 'MAM2083F', 'MAM2085F'],  # Monday
        ['EEE4119F_P', 'EEE4126F', 'MAM1020F', 'MAM1023F', 'MAM2083F', 'MAM2085F'],  # Tuesday
        ['EEE4117F', 'MAM1020F', 'MAM1023F', 'MAM2083F', 'MAM2085F'],  # Wednesday
        ['EEE4126F', 'MAM1020F', 'MAM1023F', 'MAM2083F', 'MAM2085F'],  # Thursday
        ['EEE4117F_P', 'MAM1020F', 'MAM1023F', 'MAM2083F', 'MAM2085F']  # Friday
    ],
    # Slot 2 (Period 2)
    [
        ['CSC2001F', 'CSC3002F', 'PHY1012F'],  # Monday
        ['CSC2001F', 'CSC3002F', 'PHY1012F'],  # Tuesday
        ['CSC2001F', 'CSC3002F', 'PHY1012F'],  # Wednesday
        ['CSC2001F', 'CSC3002F', 'PHY1012F'],  # Thursday
        ['CSC2001F', 'CSC3002F', 'EEE4126F_P', 'PHY1012F']  # Friday
    ],
    # Slot 3 (Period 3)
    [
        ['EEE1008F', 'EEE2045F', 'EEE3090F', 'EEE4119F', 'EEE4121F'],  # Monday
        ['EEE2045F_P', 'EEE3088F', 'EEE4118F', 'PHY1014F'],  # Tuesday
        ['EEE2045F_P', 'EEE3091F', 'EEE4119F', 'EEE4121F', 'PHY1014F'],  # Wednesday
        ['EEE1008F', 'EEE2045F', 'EEE3090F', 'EEE4118F'],  # Thursday
        ['EEE3090F_P', 'EEE3091F', 'EEE4120F', 'PHY1014F']  # Friday
    ],
    # Slot 4 (Period 4)
    [
        [],  # Monday
        ['CSC1015F_P', 'PHY1014F_P'],  # Tuesday
        ['PHY1014F_P'],  # Wednesday
        [],  # Thursday
        ['PHY1014F_P']  # Friday
    ],
    # Slot 5 (Period 5)
    [
        ['EEE4118F_P', 'MEC1009F', 'MEC2047F'],  # Monday
        ['CML4607F', 'CSC1015F_P', 'MEC1009F', 'MEC2047F'],  # Tuesday
        ['CML4607F', 'MEC1009F', 'MEC2047F'],  # Wednesday
        ['CML4607F', 'MEC1009F', 'MEC2047F', 'PHY1014F'],  # Thursday
        ['CML4607F']  # Friday
    ],
    # Slot 6 (Period M)
    [
        ['HUB4049F'],  # Monday
        ['HUB4049F'],  # Tuesday
        ['HUB4049F'],  # Wednesday
        [],  # Thursday
        []  # Friday
    ],
    # Slot 7 (Period 6)
    [
        ['EEE1008F_P', 'EEE3089F', 'EEE4120F', 'MEC1003F_P', 'MEC1009F_P', 'MEC2047F_P', 'PHY1014F'],  # Monday
        ['EEE2046F', 'EEE3092F', 'EEE4114F', 'MAM1020F_P', 'MAM1023F_P', 'MAM2085F_P'],  # Tuesday
        ['CSC1015F', 'EEE3089F', 'EEE4113F', 'MAM2083F_P', 'PHY1014F_P'],  # Wednesday
        ['EEE2046F', 'EEE3092F', 'EEE4114F', 'PHY1012F_P', 'PHY1014F_P'],  # Thursday
        ['CSC2001F_P', 'EEE1008F_P', 'EEE3090F_P', 'EEE4113F_P', 'MEC1003F']  # Friday
    ],
    # Slot 8 (Period 7)
    [
        [],  # Monday
        [],  # Tuesday
        [],  # Wednesday
        [],  # Thursday
        []  # Friday
    ],
    # Slot 9 (Period 8)
    [
        ['EEE3089F_P'],  # Monday
        ['EEE2046F_P', 'EEE3092F_P', 'EEE4120F_P'],  # Tuesday
        ['EEE3088F_P'],  # Wednesday
        ['EEE2046F_P', 'EEE3091F_P', 'EEE4120F_P'],  # Thursday
        []  # Friday
    ],
    # Slot 10 (Period 9)
    [
        [],  # Monday
        [],  # Tuesday
        [],  # Wednesday
        ['PHY1012F_P'],  # Thursday
        []  # Friday
    ]
]

# Timetable Semester 2 (slots x days grid)
TIMETABLE_SEMESTER_2: List[List[List[str]]] = [
    # Slot 1 (Period 1)
    [
        ['MAM1021S', 'MAM1024S'],  # Monday
        ['MAM1021S', 'MAM1024S', 'MAM2084S'],  # Tuesday
        ['MAM1021S', 'MAM1024S', 'MAM2084S'],  # Wednesday
        ['MAM1021S', 'MAM1024S', 'MAM2084S'],  # Thursday
        ['MAM1021S', 'MAM1024S', 'MAM2084S']  # Friday
    ],
    # Slot 2 (Period 2)
    [
        ['CSC2002S', 'PHY1013S', 'PHY2010S'],  # Monday
        ['CSC2002S', 'PHY1013S', 'PHY2010S'],  # Tuesday
        ['CSC2002S', 'PHY1013S', 'PHY2010S'],  # Wednesday
        ['CSC2002S', 'PHY1013S', 'PHY2010S'],  # Thursday
        ['CSC2002S', 'PHY1013S', 'PHY2010S']  # Friday
    ],
    # Slot 3 (Period 3)
    [
        ['EEE1009S', 'EEE2047S', 'EEE3094S'],  # Monday
        ['EEE2044S', 'EEE3096S', 'EEE3100S', 'PHY1015S'],  # Tuesday
        ['EEE2044S', 'EEE3096S', 'EEE3100S', 'PHY1015S'],  # Wednesday
        ['EEE1009S', 'EEE2047S', 'EEE3094S'],  # Thursday
        ['EEE2048S', 'EEE3097S', 'EEE3098S', 'PHY1015S']  # Friday
    ],
    # Slot 4 (Period 4)
    [
        [],  # Monday
        ['PHY1015S_P'],  # Tuesday
        ['PHY1015S_P'],  # Wednesday
        [],  # Thursday
        ['PHY1015S_P']  # Friday
    ],
    # Slot 5 (Period 5)
    [
        [],  # Monday
        ['CSC1016S', 'MEC2045S'],  # Tuesday
        ['MEC2045S'],  # Wednesday
        ['MEC2045S', 'PHY1015S'],  # Thursday
        []  # Friday
    ],
    # Slot 6 (Period M)
    [
        [],  # Monday
        [],  # Tuesday
        [],  # Wednesday
        [],  # Thursday
        []  # Friday
    ],
    # Slot 7 (Period 6)
    [
        ['CSC2002S_P', 'EEE1009S_P', 'EEE2044S_P', 'MEC2045S_P', 'PHY1015S'],  # Monday
        ['EEE3093S', 'EEE4125C', 'MAM1021S_P', 'MAM1024S_P', 'MAM2084S_P'],  # Tuesday
        ['CSC1016S_P', 'EEE3094S_P', 'PHY1015S_P'],  # Wednesday
        ['EEE3093S', 'EEE3099S', 'EEE4125C', 'PHY1013S_P', 'PHY1015S_P'],  # Thursday
        ['EEE1009S_P', 'EEE3096S_P', 'PHY2010S_P']  # Friday
    ],
    # Slot 8 (Period 7)
    [
        [],  # Monday
        [],  # Tuesday
        [],  # Wednesday
        [],  # Thursday
        []  # Friday
    ],
    # Slot 9 (Period 8)
    [
        [],  # Monday
        ['EEE3093S_P'],  # Tuesday
        [],  # Wednesday
        ['EEE3100S_P'],  # Thursday
        []  # Friday
    ],
    # Slot 10 (Period 9)
    [
        [],  # Monday
        [],  # Tuesday
        [],  # Wednesday
        [],  # Thursday
        []  # Friday
    ]
]

# Full weekly timetable (vertically concatenated slot rows)
TIMETABLE: List[List[List[str]]] = TIMETABLE_SEMESTER_1 + TIMETABLE_SEMESTER_2