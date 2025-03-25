"""
File: constants.py
Author: Alex Mees
Date: 2025-03-13
Description: file to organize global constants used in the program
License: MIT
"""


#Pattern Matching Constants
COMMON_DELIMITERS = [',',';',':',' ','\t','-','|'] #delimiters format list used when trying to auto-detecting them
DATA_TYPE_SAMPLE_SIZE = 10 #the maximum amount of data that will be sampled when trying to autodetect data types
WORLD_COUNTRIES = {
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", 
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", 
    "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", 
    "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", 
    "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", 
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", 
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", 
    "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", 
    "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", 
    "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", 
    "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", 
    "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", 
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", 
    "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", 
    "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", 
    "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", 
    "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", 
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", 
    "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", 
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", 
    "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
} #to check for geographic data
M_MONTH_NAMES = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
MM_MONTH_NAMES = ['january','february','march','april','may','june','july','august','september','october','november','december']



BLOCKED_WORD_LIST = {'bad word1', 'bad word 2', 'bad word 3'} #built in BLOCKED WORDS for testing
COMMON_BLOCKED_WORD_BYPASSES = [
    ["a", "@"], ["a", "4"], ["a", "∂"],
    ["b", "8"], ["b", "|3"],
    ["c", "("], ["c", "{"], ["c", "<"],
    ["e", "3"], ["e", "€"],
    ["g", "6"], ["g", "9"],
    ["h", "#"], ["h", "|-|"],
    ["i", "1"], ["i", "!"], ["i", "|"],
    ["l", "1"], ["l", "|"],
    ["o", "0"], ["o", "°"],
    ["s", "$"], ["s", "5"],
    ["t", "7"], ["t", "+"],
    ["z", "2"]
] #common intentional letter swaps to bypass blocked words.


COMMON_DICTIONARY_REPLACEMENTS = ["docotor",  
        "docter",  
        "doctr",  
        "dr.",    
        "Dr..",  
        "dr",   
        "Dr,", 
        "Dotor",  
        "Docor",  
        "Doktor"]

