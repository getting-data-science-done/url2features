# -*- coding: utf-8 -*-
 
""" url2features.main: provides entry point main()."""
 
import pandas as pd
import sys
import os

from .process import load_complete_dataframe
from .process import process_file_in_chunks
from .process import initialise_profile
from .process import print_profiles
from .process import print_output

from .featurize import generate_feature_function

from .config import max_filesize
 
def main():
    """Main url2features application entry point.
       parses out CL options and determine the size of the file.
       Then process the file for the requested features
    """
    if len(sys.argv) < 2:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        params = get_cmd_line_params(sys.argv)

        if not os.path.exists(params["dataset"]):
            print("ERROR: Dataset does not exist")
            print_usage(sys.argv)
            exit(1)

        initialise_profile()
        feature_func = generate_feature_function(params)

        filesize = os.stat(params["dataset"]).st_size
        if filesize<max_filesize:
            df = load_complete_dataframe( params["dataset"] )
            simple = feature_func(df)
            print_output( simple )
        else:
            process_file_in_chunks(params["dataset"], feature_func)

        print_profiles()


#############################################################
def get_cmd_line_params(argv):
    """ parse out the option from an array of command line arguments """
    data = argv[-1]
    options = argv[1:-1]
    result = {"dataset":data,
              "columns":[], 
              "simple":False, 
              "domain":False, 
              "extension":False, 
              "ip":False, 
              "file":False, 
    }
    for o in options:
        parts = o.split("=")
        if parts[0] == "-simple":
            result["simple"]=True
        if parts[0] == "-domain":
            result["domain"]=True
        if parts[0] == "-file":
            result["file"]=True
        if parts[0] == "-ip":
            result["ip"]=True
        if parts[0] == "-extension":
            result["extension"]=True
        if parts[0] == "-columns":
            cols = parts[1].split(",")
            result["columns"]=cols

    return result

#############################################################
def print_usage(args):
    """ Command line application usage instrutions. """
    print("USAGE ")
    print(args[0], " [ARGS] <PATH TO DATASET>")
    print("  <PATH TO DATASET> - Supported file types: csv, tsv, xls, xlsx, odf")
    print(" [ARGS] In most cases these are switches that turn on the feature type")
    print("  -columns=<COMMA SEPARATED LIST>. REQUIRED")
    print("  -simple            Default: False. Features derived from the URL string: length, depth")
    print("  -domain            Default: False. Features from the domain registration (requires internet).")
    print("  -file              Default: False. Features derived from the final file.")
    print("  -ip                Default: False. Features derived from the IP address (requires internet).")
    print("  -extension         Default: False. Features about the domain extension and structure.")
    print("")


##########################################################################################
if __name__ == '__main__':
    main()


