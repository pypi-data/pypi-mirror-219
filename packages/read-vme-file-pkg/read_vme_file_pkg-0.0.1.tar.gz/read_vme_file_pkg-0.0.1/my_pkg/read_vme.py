"""Read VME files and extract relevant data."""
import re

import pandas as pd


def read_vme_file(file_path): 
    """Read a vme file and return a structured representation of its content.

    :param file_path: The path to the vme file._
    :type file_path: str
    :return: A dictionary with data extracted from the VME file.
    """
    # open file
    with open(file_path, 'r') as file:
        # initialize dictionary
        vme_dict = {}
        vme_dict['Comments'] = ""
        vme_dict['Constants'] = ""
        vme_dict['Channels'] = []
        vme_dict['ChannelsData'] = {}
        vme_dict['Data'] = []
    
        # initialize flags for different parts of the VME file
        read_entries_comments = False
        read_entries_constants = False
        read_entries_channels = False
        read_entries_data = False
    
        for line in file: # Iterate through each line in the file
            # Remove newline character
            current_line = line.strip()
    
            # Set flag for "**COMMENTS"
            if current_line == '**COMMENTS':
                read_entries_comments = True
            # Remove flag for "**CONSTANTS"
            elif current_line == '**CONSTANTS':
                read_entries_comments = False
    
            # Add to dictionary if flag is true
            if read_entries_comments:
                vme_dict['Comments'] += current_line + "\n"
    
            # Set flag for "**CONSTANTS"
            if current_line == '**CONSTANTS':
                read_entries_constants = True
            # Remove flag for "**CHANNELS"
            elif current_line == '**CHANNELS':
                read_entries_constants = False
    
            # Add to dictionary if flag is true
            if read_entries_constants:
                vme_dict['Constants'] += current_line + "\n"
    
            # Set flag for "**CHANNELS"
            if current_line == '**CHANNELS':
                read_entries_channels = True
            # Set flag for "**DATA"
            elif current_line == '**DATA':
                read_entries_channels = False
    
            # Add to dictionary if flag is true
            if read_entries_channels and (current_line != "**CHANNELS"):
                vme_dict['Channels'].append(current_line)
    
            # Set flag for "**DATA"
            if current_line == '**DATA':
                read_entries_data = True
            # Remove flag for "**END"
            elif current_line == '**END':
                read_entries_data = False
    
            # add to dictionary if flag is true
            if read_entries_data and (current_line != "**DATA") and current_line:
                # Split string
                temp_str = current_line.split()
    
                # Save in array
                temp_array = list(map(float, temp_str))
    
                # Add array to list
                vme_dict['Data'].append(temp_array)
    
        # Delete empty elements from "Channels"
        vme_dict['Channels'] = [channel for channel in vme_dict['Channels'] if channel]
    
        # Create dictionary for ChannelsData and move data
        channel_dict = {}
        for channel in vme_dict['Channels']:
            # Use a regular expression to extract data from the channel
            expression = r'^\s*\d+\s+([\w\s.]+?)\s+(\d+)?\s*\[(.+)\]$'
            match = re.match(expression, channel)
            if match:
                # Extract data from the match object
                temp_description = match.group(1).replace(' ', '').replace('.', '_')
                temp_number = match.group(2)
                temp_unit = match.group(3).strip()
                if not temp_number:
                    temp_number = 1
                else:
                    temp_number = float(temp_number)
                # Add the data to the channels dictionary
                channel_dict[temp_description] = {
                    'Conversion_factor': temp_number, 
                    'Unit': temp_unit
                }
    
        # Add the channels dictionary to the main dictionary
        vme_dict['ChannelsData'] = channel_dict
    
        # Convert Data to DataFrame
        data_df = pd.DataFrame(vme_dict['Data'])
    
        # Rename the columns in the DataFrame based on the channels
        data_df.columns = list(vme_dict['ChannelsData'].keys())
    
        # Apply the conversion factor to the columns in the DataFrame
        for column, conversion in vme_dict['ChannelsData'].items():
            data_df[column] = data_df[column] / conversion['Conversion_factor']
    
        # Prepare the final dictionary to be returned
        ret_dict = {
            'Comments': vme_dict['Comments'],
            'Constants': vme_dict['Constants'],
            'ChannelsData': vme_dict['ChannelsData'],
            'Data': data_df
        }
    
        return ret_dict

#file_path = 'C:/Users/ssy/Desktop/hiwi-test/code/TEST215.24'
#vme_data = read_vme_file(file_path)

# get comments
#comments = vme_data['Comments']

# get constants
#constants = vme_data['Constants']

# get channels_data
#channels_data = vme_data['ChannelsData']

# get data
#data = vme_data['Data']
#print(constants)
#print(channels_data)
#print(data)