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
              "prefix":True, 
              "simple":False, 
              "protocol":False, 
              "host":False, 
              "tld":False, 
              "path":False, 
              "file":False, 
              "params":False, 
              "dns":False, 
    }
    for o in options:
        parts = o.split("=")
        if parts[0] == "-np":
            result["prefix"]=False
        if parts[0] == "-simple":
            result["simple"]=True
        if parts[0] == "-protocol":
            result["protocol"]=True
        if parts[0] == "-host":
            result["host"]=True
        if parts[0] == "-tld":
            result["tld"]=True
        if parts[0] == "-path":
            result["path"]=True
        if parts[0] == "-file":
            result["file"]=True
        if parts[0] == "-params":
            result["params"]=True
        if parts[0] == "-dns":
            result["dns"]=True
        if parts[0] == "-columns":
            cols = parts[1].split(",")
            result["columns"]=cols

    if len(result["columns"])>1:
        result["prefix"] = True # Force prefix for multiple columns

    return result

#############################################################
def print_usage(args):
    """ Command line application usage instrutions. """
    print("USAGE ")
    print(args[0], " [ARGS] <PATH TO DATASET>")
    print("  <PATH TO DATASET> - Supported file types: csv, tsv, xls, xlsx, odf")
    print(" [ARGS] In most cases these are switches that turn on the feature type")
    print("  -columns=<COMMA SEPARATED LIST>. REQUIRED")
    print("  -simple            Default: False. Features derived from the URL string: length, depth, components")
    print("  -host              Default: False. Features about the host including subdoamin and registration (requires internet).")
    print("  -tld               Default: False. Features about the top level domain (TLD)")
    print("  -protocol          Default: False. Features from the URL protocol.")
    print("  -path              Default: False. Features derived from the path between host and file")
    print("  -file              Default: False. Features derived from the final file type")
    print("  -params            Default: False. Features derived from any query string parameters in the URL")
    print("  -dns               Default: False. Features derived from the DNS records (requires internet).")
    print("  -np                Deactivate use of column name prefix. Only works for a single column.")
    print("")


##########################################################################################
if __name__ == '__main__':
    main()


