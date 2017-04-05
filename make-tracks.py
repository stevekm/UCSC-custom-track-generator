#!/usr/bin/env python
# python 2.7

'''
This script will make custom UCSC tracks from supplied files.

external resources:
https://genome.ucsc.edu/goldenpath/help/hgTracksHelp.html
https://genome.ucsc.edu/goldenpath/help/customTrack.html

submit your tracks here:
https://genome.ucsc.edu/cgi-bin/hgCustom
'''


# ~~~~ LOAD PACKAGES ~~~~~~ #
import sys
import os
import argparse
import datetime

# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
def my_debugger(vars):
    '''
    starts interactive Python terminal at location in script
    very handy for debugging
    call this function with
    my_debugger(globals().copy())
    anywhere in the body of the script, or
    my_debugger(locals().copy())
    within a script function
    '''
    import readline # optional, will allow Up/Down/History in the console
    import code
    # vars = globals().copy() # in python "global" variables are actually module-level
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

def get_track_type(input_file):
    '''
    Match the file extension to a dictionary of known track types for UCSC
    '''
    file_name, extension = os.path.splitext(input_file)
    # recognized data types
    data_types = {
    ".bw":  {"track_type": "bigWig", "url_tag": "bigDataUrl"},
    ".bed": {"track_type": "BED", "url_tag": "url"},
    ".bb":  {"track_type": "bigBed", "url_tag": "bigDataUrl"},
    ".vcf": {"track_type": "VCF", "url_tag": "bigDataUrl"},
    ".bam": {"track_type": "BAM", "url_tag": "bigDataUrl"},
    ".bg":  {"track_type": "bedGraph", "url_tag": "url"}
    }
    if extension in data_types.keys():
        return(data_types[extension])
    else:
        print("File type not recognized for file:\n{}\nExiting...".format(input_file))
        sys.exit()

def initialize_file(string, output_file):
    '''
    Write a string to the file in 'write' mode, overwriting any contents
    '''
    with open(output_file, "w") as myfile:
        myfile.write(string)

def append_string(string, output_file):
    '''
    Append a string to a file
    '''
    with open(output_file, "a") as myfile:
        myfile.write(string + '\n')

def concat_file_lines(file, delim = ' '):
    '''
    Join all lines in file together into a single delimited string
    '''
    file_lines = [line.strip() for line in open(file)]
    file_string = delim.join(file_lines)
    return(file_string)

def timestamp():
    '''
    Return a timestamp string
    '''
    return('{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))

def check_for_default_outputfile(output_file):
    '''
    Return a default value if `output_file` is set to None
    '''
    if output_file == None:
        output_file = "UCSC_custom_tracks-{}.txt".format(timestamp())
    return(output_file)

def make_UCSC_track(input_file, url, params = ''):
    '''
    Build the custom track text from the input file
    '''
    track_type = get_track_type(input_file)
    file_basename = os.path.split(input_file)[1]
    file_url = '{}/{}'.format(url_base, file_basename)
    track_line = 'track type={} name="{}" {}={} {}'.format(track_type['track_type'], file_basename, track_type['url_tag'], file_url, file_params)
    return(track_line)


def save_all_tracks(input_files, output_file, url_base, file_params, stdout_flag):
    '''
    Make the UCSC track for each file in the list
    '''
    # make track for each input file
    for file in input_files:
        track_line = make_UCSC_track(input_file = file, url = url_base, params = file_params)
        append_string(track_line, output_file)
    print('\nUCSC Tracks output to file:\n{}\n'.format(output_file))

# ~~~~ GET SCRIPT ARGS ~~~~~~ #
parser = argparse.ArgumentParser(description='UCSC Custom Track Creator.')
# required positional args
parser.add_argument("input_files", nargs='+', help="path to the file(s) to create tracks from") # , nargs='?'

# required flags
parser.add_argument("-url", default = 'http://somewhere.com/somedir/', type = str, dest = 'url', metavar = 'URL', help="Externally accessible URL base to use for the files")

# optional flags
parser.add_argument("-p", default = None, dest = 'params_file', metavar = 'extra params file', help="File containing extra parameters to include")
parser.add_argument("-o", default = None, dest = 'output_file', metavar = 'output file', help="Output file for tracks. Defaults to timestamped file.")
parser.add_argument("-s", default = False, action='store_true', dest = 'stdout_flag', help="Whether to print the tracks to stdout.")

args = parser.parse_args()
input_files = args.input_files
params_file = args.params_file
url_base = args.url
output_file = args.output_file
stdout_flag = args.stdout_flag

if __name__ == "__main__":
    # trim trailing slash in URL
    if url_base.endswith('/'):
        url_base = url_base[:-1]
    # get params from param file, if present
    if params_file != None:
        file_params = concat_file_lines(params_file)
    else :
        file_params = ''
    if stdout_flag == False:
        # setup output file
        output_file = check_for_default_outputfile(output_file)
        # wipe the output file if present; otherwise 'touch' it
        initialize_file('', output_file)
        # make tracks for each input file
        save_all_tracks(input_files, output_file, url_base, file_params)
    elif stdout_flag == True:
        for file in input_files:
            print(make_UCSC_track(input_file = file, url = url_base, params = file_params))
