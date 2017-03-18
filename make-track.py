#!/usr/bin/env python

'''
This script will make custom UCSC tracks
resources:
https://genome.ucsc.edu/
https://genome.ucsc.edu/goldenpath/help/bigBed.html
https://genome.ucsc.edu/goldenpath/help/hgTracksHelp.html
https://genome.ucsc.edu/goldenpath/help/customTrack.html

https://genome.ucsc.edu/cgi-bin/hgCustom
'''


# ~~~~ LOAD PACKAGES ~~~~~~ #
import sys
import os
import argparse

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

def get_data_type(input_file):
    import os
    file_name, extension = os.path.splitext(input_file)
    # dictionary of types recognized
    data_types = {
    # file extension : (type, URL parameter)
    ".bw": ("bigWig","bigDataUrl"),
    ".bed": ("BED", "url"),
    ".bb": ("bigBed", "bigDataUrl"),
    ".vcf": ("VCF", "bigDataUrl"),
    ".bam": ("BAM", "bigDataUrl"),
    ".bg": ("bedGraph", "url")
    # GFF, GTF
    }
    if extension in data_types.keys():
        return(data_types[extension])
    else:
        print("File type not recognized for file:\n{}\nExiting...".format(input_file))
        sys.exit()

def get_URL_param(file_type):
    # list of file extensions for 'bigData' filetypes
    bigData_ext = ['.bw', '.bam', '.cram', '.bb', '.vcf'] #  BAM, CRAM, bigBed, bigWig or VCF


# ~~~~ GET SCRIPT ARGS ~~~~~~ #
parser = argparse.ArgumentParser(description='UCSC Custom Track Creator.')
# required positional args
parser.add_argument("input_files", nargs='+', help="path to the file(s) to create tracks from") # , nargs='?'

# required flags
parser.add_argument("-url", default = 'http://somewhere.com/somedir/', type = str, dest = 'url', metavar = 'URL', help="Externally accessible URL base to use for the files")

# optional flags
parser.add_argument("-p", default = None, dest = 'params_file', metavar = 'extra params file', help="File containing extra parameters to include")


args = parser.parse_args()
input_files = args.input_files
params_file = args.params_file

if __name__ == "__main__":
    print(input_files)
    for file in input_files:
        print(get_data_type(file))
    print(str(params_file))
