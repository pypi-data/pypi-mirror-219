"""Read tydex file and extract relevant data."""
import re

import pandas as pd


def read_tydex_file(file_path):
    """Read a tydex file and return a structured representation of its content.

    :param file_path: The path to the tydex file.
    :type file_path: str
    :return: dict, A dictionary containing the file including Header, Comments,  
             Constants,MeasurChannels, MeasurChannelsNotes and MeasurData.
    """
    # open file
    fid = open(file_path, 'r')
    
    # Initialize tydex structure
    tydex_struct = {} # The resulting structured representation
    tydex_struct['Header'] = ""
    tydex_struct['Comments'] = ""
    tydex_struct['Constants'] = pd.DataFrame()
    tydex_struct['MeasurChannels'] = pd.DataFrame()
    tydex_struct['MeasurChannelsNotes'] = ""
    tydex_struct['MeasurData'] = pd.DataFrame()
    
    # Initialize data holders
    constants_dump = []
    channels_dump = []
    data_dump = []
    
    # Initialize flags
    read_entries_header = False
    read_entries_comments = False
    read_entries_constants = False
    read_entries_channels = False
    read_entries_data = False
    
    # Iterate over each line in the file
    for line in fid:
        current_line = line.strip()
        
        # Parse header
        # If current line is the start of header, set the flag to True
        if current_line == '**HEADER':
            read_entries_header = True
        # If current line is the start of comments, set the flag to False
        elif current_line == '**COMMENTS':
            read_entries_header = False
        
        # If the flag is True, append the current line to header
        if read_entries_header:
            tydex_struct['Header'] += current_line + "\n"
        
        # Parse comments
        # If current line is the start of comments, set the flag to True
        if current_line == '**COMMENTS':
            read_entries_comments = True
        # If current line is the start of constants, set the flag to False
        elif current_line == '**CONSTANTS':
            read_entries_comments = False
        
        # If the flag is True, append the current line to comments
        if read_entries_comments:
            tydex_struct['Comments'] += current_line + "\n"
        
        # Parse constants
        # If current line is the start of constants, set the flag to True
        if current_line == '**CONSTANTS':
            read_entries_constants = True
        # If current line is the start of measurement channels, set the flag to False
        elif current_line == '**MEASURCHANNELS':
            read_entries_constants = False
        
        # If the flag is True&the current line is not empty,append current line to constants list
        if read_entries_constants and current_line != "**CONSTANTS" and current_line:
            constants_dump.append(current_line)
        
        # Parse channels
        # If current line is the start of measurement channels, set the flag to True
        if current_line == '**MEASURCHANNELS':
            read_entries_channels = True
        # If current line is the start of measurement data, set the flag to False
        elif current_line == '**MEASURDATA':
            read_entries_channels = False
        
        if read_entries_channels and current_line != "**MEASURCHANNELS" and current_line:
             # If current line starts with "!", it's a note of measurement channels
            if current_line.startswith('!'):# Otherwise, append the current line to channels list
                tydex_struct['MeasurChannelsNotes'] = current_line
            else:
                channels_dump.append(current_line)
        
        # Parse data
        if current_line == '**MEASURDATA':
            # If current line is the start of measurement data, set the flag to True
            read_entries_data = True
        
        if (read_entries_data and current_line != "**MEASURDATA" 
                and any(char.isdigit() for char in current_line)):
            # If the flag is True and the current line contains a digit, indicating it's a data line
  
            # Split the string
            tempStr = current_line.strip().split()
            # Convert to array
            tempArray = list(map(float, tempStr))
            # Add the array to data holder
            data_dump.append(tempArray)
    
    # Create constants table
    temp_constants_table = []
    for i in range(len(constants_dump)): # Iterate through each constant string
        str = constants_dump[i] # Get the current constant string
        split_str = re.split('^(.{10})(.{30})(.{10})(.*)$', str.strip())
        # Split the string using regex
        temp_constants_table.append(split_str[1:5]) # Add the splitted result to the list
    
    tydex_struct['Constants'] = pd.DataFrame(
        temp_constants_table, 
        columns=['Name', 'Description', 'Unit', 'Value']
    )

    
    # Create measurement channels table
    temp_channels_table = []
    for i in range(len(channels_dump)): # Iterate through each channel string
        str = channels_dump[i] # Get the current channel string
        split_str = re.split('^(.{10})(.{30})(.{10})(.*)$', str.strip())
        # Convert to float
        split_str[4] = float(split_str[4])
        temp_channels_table.append(split_str[1:5])
    
    # Convert channels table to DataFrame and add to tydex structure
    tydex_struct['MeasurChannels'] = pd.DataFrame(
        temp_channels_table,
        columns=['Name', 'Description', 'Unit', 'Conversion_factor']
    )

    
    # Create measuredata table
    tydex_struct['MeasurData'] = pd.DataFrame(data_dump)
    
    # Setting row names
    tydex_struct['MeasurData'].columns = tydex_struct['MeasurChannels']['Name']
    
    # Apply conversion_factor
    for i in range(tydex_struct['MeasurData'].shape[1]): # Iterate through each column
        tydex_struct['MeasurData'].iloc[:, i] *= tydex_struct['MeasurChannels'].iloc[i, 3]
    
    
    return tydex_struct


