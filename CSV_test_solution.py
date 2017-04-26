# Will Geary
# 
# willcgeary@gmail.com

# # Part 1 - CSV Test

# To Do: Write a script to transform input CSV to desired output CSV. 

# *You will find a CSV file available for download here: [test.csv](https://s3.amazonaws.com/data-code-test/test.csv). There are two steps (plus an optional bonus) to this part of the test. Each step concerns manipulating the values for a single field according to the step's requirements. The steps are as follows:*

# ### String cleaning
# *The bio field contains text with arbitrary padding, spacing and line breaks. Normalize these values to a space-delimited string.*

import pandas as pd # pandas library
import re # regular expressions


# Read the csv into a pandas dataframe.

df = pd.read_csv('https://s3.amazonaws.com/data-code-test/test.csv')

print "The data frame is", df.shape[0], "rows and", df.shape[1], "columns."

bios = df['bio'].copy()

# In order to clean up the bio's we need to:
# 
# - Remove white spaces from front and back of each string
# 
# - Remove characters such as: \n, \t, \r
# 
# - Remove extra big spaces such as 'laudantium      earum ducimus'

# Store clean bios in a list
clean_bios = []

# Clean each bio
for bio in bios:
    clean_bio = (re.sub(' +',' ',         # regex to remove consecutive white spaces of length > 1
                    bio                   # select bio
                    .strip()              # trim leading and trailing whitespace
                    .replace("\n", "")    # remove \n
                    .replace("\t", "")    # remove \t
                    .replace("\r", "")))  # remove \r

    clean_bios.append(clean_bio)
    
# Replace bios column with clean bios
df['bio'] = clean_bios




# ### Code Swap
# 
# *There is a supplementary CSV file for download here: [state_abbreviations.csv](https://s3.amazonaws.com/data-code-test/state_abbreviations.csv). This "data dictionary" contains state abbreviations alongside state names. For the state field of the input CSV, replace each state abbreviation with its associated state name from the data dictionary.*

# Read `state_abbreviations.csv` into a data frame:

states = pd.read_csv("https://s3.amazonaws.com/data-code-test/state_abbreviations.csv")
states.head()


# Convert dataframe into a dictionary, with keys = state_abbr and values = state_name

states = dict(zip(states.state_abbr.values, states.state_name.values))

# List of state abbreviations from the dataframe
df_state_abbr = list(df['state'])

# Store corresponding state names in a list
df_state_name = []

# Add corresponding state names to the list
for abbr in df_state_abbr:
    state_name = states[abbr]
    df_state_name.append(state_name)
    
# Replace state abbrev with state name to dataframe
df['state'] = df_state_name

# ### Date offset (bonus)
# 
# *The start_date field contains data in a variety of formats. These may include e.g., "June 23, 1912" or "5/11/1930" (month, day, year). But not all values are valid dates. Invalid dates may include e.g., "June 2018", "3/06" (incomplete dates) or even arbitrary natural language. Add a start_date_description field adjacent to the start_date column to filter invalid date values into. Normalize all valid date values in start_date to ISO 8601 (i.e., YYYY-MM-DD).*

# I will use regular expressions to match three date formats that exist in the `start_date` field.
# 
# The three date formats that we will look for are:
# 
# - 12/31/1991
# - December 31, 1991
# - 1991-12-31


# Regex to match dates in the format: 12/31/1991
regex1 = r'(\d+/\d+/\d+)'

# Regex to match dates in the format: December 3, 1991 or December 31, 1991
regex2 = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9]?(\.[0-9][0-9]?)?,) (?:19[0-9]\d|2\d{3})(?=\D|$)'

# Regex to match dates in the format: 1976-05-17
regex3 = r'(\d+-\d+-\d+)'

# Now, we will use the `dateutil` library to try parsing each date in the column, matching it against each of the three regex formats.
from dateutil import parser

start_dates = list(df['start_date'])
clean_start_dates = []

for date in start_dates:
    try_date_format_1 = re.search(regex1, date)
    try_date_format_2 = re.search(regex2, date)
    try_date_format_3 = re.search(regex3, date)
    
    if try_date_format_1 != None:
        date = parser.parse(try_date_format_1.group(0))
        clean_start_dates.append(date.strftime('%Y-%m-%d'))
        
    elif try_date_format_2 != None:
        date = parser.parse(try_date_format_2.group(0))
        clean_start_dates.append(date.strftime('%Y-%m-%d'))
        
    elif try_date_format_3 != None:
        date = parser.parse(try_date_format_3.group(0))
        clean_start_dates.append(date.strftime('%Y-%m-%d'))
        
    else:
        clean_start_dates.append(None)

# shift old start_date column into start_date_description
df['start_date_description'] = df['start_date'].copy()

# insert clean start dates into start_date column
df['start_date'] = clean_start_dates

# Save the resulting data frame to `solutions.csv`:
df.to_csv("solution.csv")
