import re
def format_finder_fun(text):
    proposed_position_search= re.search(r"Proposed Position",text)
    name_searcg = re.search(r"Name of Expert",text)
    address_pattern_search = re.search(r"Current Residential Address",text)
    dob_pattern_search = re.search(r"Date of Birth",text)
    citizenship_pattern_search = re.search(r"Citizenship",text)
    telephone_pattern_search=re.search(r"Telephone No",text)
    if proposed_position_search and name_searcg and address_pattern_search and dob_pattern_search and citizenship_pattern_search and telephone_pattern_search:
        return 'adb'
    
    position_pattern=re.search(r"Position Title and No",text)
    name_pattern = re.search(r"Name of Expert",text)
    dob_pattern = re.search(r"Date of Birth",text)
    citizenship_pattern = re.search(r"Country of Citizenship",text)
    if position_pattern and name_pattern and dob_pattern and citizenship_pattern:
        return 'world_bank'
    
    else:
        return 'other'
    
