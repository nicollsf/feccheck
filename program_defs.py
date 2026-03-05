from typing import List, Dict, Union, Any

# --- Programme Definitions ---

# MATLAB: mecode, mecore, menecore, mececore
ME_CODE = 'EB011'
ME_CORE = [
    'CSC1015F', 'EEE1008F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 'AXL1200S', 
    'CSC1016S', 'EEE1009S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048S', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'MEC2026S', 'PHY2010S', 
    'EEE3088F', 'EEE3090F', 'EEE3091F', 'EEE3092F', 'MEC2047F', 
    'EEE3094S', 'EEE3096S', 'EEE3099S', 'MEC2045S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
# Note: MATLAB `menecore = {{1,'EEE4119F'}}` means: select 1 course from the list (which is just EEE4119F). 
# This looks like a list of requirements: each inner list is a group, where the first element is the number required.
ME_NECORE = [
    [1, 'EEE4119F'] 
]
# Note: MATLAB `mececore = {{48,...}}` means: select courses totaling 48 credits from the list.
ME_CECORE = [
    [48, 'EEE4117F', 'EEE4118F', 'EEE4119F', 'EEE4086F', 'EEE4114F', 
    'EEE4120F', 'EEE4123C', 'HUB4045F']
]

# MATLAB: eecode, eecore, eenecore, eececore
EE_CODE = 'EB009'
EE_CORE = [
    'CSC1015F', 'EEE1008F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 'AXL1200S', 
    'CSC1016S', 'EEE1009S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048S', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'MEC2026S', 'PHY2010S', 
    'EEE3088F', 'EEE3089F', 'EEE3090F', 'EEE3091F', 'EEE3092F', 
    'EEE3093S', 'EEE3094S', 'EEE3098S', 'EEE3100S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
EE_NECORE = [
    [1, 'EEE4126F', 'EEE4118F', 'EEE4121F']
]
EE_CECORE = [
    [48, 'EEE4126F', 'EEE4118F', 'EEE4121F', 'EEE4114F', 'EEE4105C', 
    'EEE4116F', 'EEE4117F', 'EEE4122C', 'EEE4123C', 'HUB4045F']
]

# MATLAB: eccode, eccore, ecnecore, eccecore
EC_CODE = 'EB022'
EC_CORE = [
    'CSC1015F', 'EEE1008F', 'MAM1020F', 'MEC1003F', 'PHY1012F', 'AXL1200S', 
    'CSC1016S', 'EEE1009S', 'MAM1021S', 'PHY1013S', 'EEE1000X', 
    'EEE2045F', 'EEE2046F', 'EEE2048S', 'MAM2083F', 'MEC1009F', 
    'EEE2044S', 'EEE2047S', 'MAM2084S', 'MEC2026S', 'PHY2010S', 
    'CSC2001F', 'EEE3088F', 'EEE3089F', 'EEE3090F', 'EEE3092F', 
    'EEE3096S', 'EEE3097S', 'COMPSTUD', 'EEE3000X', 
    'EEE4113F', 'CML4607F', 'EEE4125C', 'EEE4124C', 'EEE4022S'
]
EC_NECORE = [
    [2, 'CSC2002S', 'EEE3093S', 'EEE3094S'], 
    [1, 'EEE4120F', 'EEE4121F']
]
EC_CECORE = [
    [48, 'EEE4118F', 'EEE4119F', 'EEE4120F', 'EEE4121F', 'EEE4086F', 
    'EEE4114F', 'EEE4105C', 'EEE4122C', 'CSC3002F', 'CSC3003S', 
    'CSC3021F', 'CSC3022F', 'CSC3022H', 'CSC3023F', 'HUB4045F']
]

# MATLAB: Assemble into single structure
# We use a list of dictionaries in Python for the structure array.
PROGRAM_SPECS: List[Dict[str, Any]] = [
    {
        'prog': 'ME', 
        'code': ME_CODE,  
        'core': ME_CORE,  
        'necore': ME_NECORE,  
        'cecore': ME_CECORE
    },
    {
        'prog': 'EE', 
        'code': EE_CODE,  
        'core': EE_CORE,  
        'necore': EE_NECORE,  
        'cecore': EE_CECORE
    },
    {
        'prog': 'EC', 
        'code': EC_CODE,  
        'core': EC_CORE,  
        'necore': EC_NECORE,  
        'cecore': EC_CECORE
    }
]

# MATLAB: caddavail
# Additional courses not yet specified that contribute to core
ADDITIONAL_AVAILABLE_COURSES: List[str] = []

# MATLAB: cequivs
# Equivalent courses structure: the first element is the required course, 
# and the rest are courses that satisfy that requirement. An inner list/tuple 
# means ALL courses inside must be satisfied.

# In Python, a list of lists/tuples works fine for translation.
# Union[str, List[str]] handles the case where a course is replaced by a single course name (str) 
# or by a required group (List[str] or tuple).
CourseEquivsList = List[List[Union[str, List[str]]]]

COURSE_EQUIVALENCIES: CourseEquivsList = [
    ['AXL1200S', 'AXL1001S', 'CAS1001S', 'CAS2001S', 'AXL1301S', 'ASL1200S'],
    ['CSC1015F', 'CSC1015S', 'EEE1003W'],
    ['CSCxxxxx', 'CSC3022H', 'CSC3023F'],
    ['EEE1005W', 'EEE1004W', ['EEE1006F', 'EEE1007S']],
    ['EEE1007S', 'EEE1005W'],
    ['EEE1006F', 'EEE1005W'],
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
    ['MEC2026S', 'MEC2026F'],
    ['MEC2023F', 'MEC2023S'],
    ['EEE2044S', 'EEE2038W'],
    ['EEE2045F', 'EEE2040F'],
    ['EEE2046F', 'EEE2046S'],
    ['EEE3090F', 'EEE3068F'],
    ['EEE3091F', 'EEE3031S'],
    ['EEE2048F', 'EEE3073S'],
    ['EEE2048S', 'EEE2048F'],
    ['EEE3092F', 'EEE3086F'],
    ['EEE3093S', 'EEE3083F', 'EEE3084W', 'EEE3085S'],
    ['EEE3094S', 'EEE3069W', 'EEE3081F', 'EEE3082S'],
    ['EEE3096S', 'EEE3074W'],
    ['EEE3100S', 'EEE3057S'],
    ['EEE4114F', 'EEE4001F'],
    ['EEE4006C', 'EEE4006F'],
    ['EEE4113F', 'EEE4036C', 'EEE4036A'],
    ['EEE4051C', 'EEE4051F'],
    ['EEE4120F', 'EEE4084F'],
    ['EEE4086F', 'EEE4086F'], # Self-reference, redundant but preserved
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
    ['MEC2026S', 'CON2026S'],
    ['MEC2047F', 'MEC2023F', 'MEC2023S', 'MEC2047S'],
    ['EEE4022S', 'EEE4022F'],
    ['EEE4036C', 'EEE4036A', 'EEE4113C'],
    ['EEE4006C', 'EEE4006F'],
    ['EEE4051C', 'EEE4051F'],
    ['EEE4113F', 'EEE4036A', 'EEE4036C'],
    ['MEC4022Z', 'MEC4044Z', 'MEC4054Z'],
    ['MEC3035S', 'MEC3035F'],
    ['MEC4063C', 'MEC4044Z', 'MEC4054Z', 'EEE4124C'],
    ['EEE4124C', 'MEC4063C'],
    ['COMPSTUD', 'ACC1006F', 'AGE1002S', 'ANS2401L', 'AST1000F', 'AXL1100S', 'AXL1400F', 'AXL1401S', 'BIO1004S', 'BUS1007S', 'BUS1036F', 'BUS1036S', 'BUS2010F', 'BUS2010S', 'ECO1006F', 'ECO1007F', 'ECO1007S', 'ECO1010F', 'ECO1010S', 'ECO1011F', 'ECO1011S', 'ECO2007S', 'EGS1003S', 'ELL1016S', 'END1019L', 'END1019P', 'END1019Z', 'END1023S', 'FAM1000L', 'FAM1000S', 'FAM1001P', 'FTX1005S', 'FTX2000S', 'GEO1009F', 'HST1014S', 'HST2034P', 'MUZ1339H', 'MUZ1381H',  'PHI1010S', 'PHI1024F', 'PHI1025F', 'PHI2012F', 'PHI2040S', 'PHI2043F', 'PHI2043P', 'PHI2043S', 'PSY1004F', 'REL1006S', 'SLL1002F', 'SLL1002L', 'SLL1002P', 'SLL1002S', 'SLL1016S', 'SLL1018S', 'SLL1058F', 'SLL1060F', 'SLL1062F', 'SLL1062L', 'SLL1063S', 'SLL1064F', 'SLL1097S', 'SLL1101F', 'SLL2060F', 'SLL3060F', 'SOC1005J'],
    ['CML4607F', 'CML4607Z'],
    ['CML4607F', 'MEC4022Z']
]