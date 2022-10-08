# ###################################################################################
# Plot URL Imprtance
#
# ###################################
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import pandas as pd
import sys
import os

def add_global(axes, ypos, alph):
   myy = ypos-0.25
   axes.add_patch(mpatches.FancyBboxPatch((3.15, myy), 16.1, 0.2,
       boxstyle=mpatches.BoxStyle("Round", pad=0.05), alpha=alph, color='grey')
   )


def add_protocol(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((3.3, myy), 2.0, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_subdomain(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((6.0, myy), 0.8, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_domain(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((7.4, myy), 1.7, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_tld(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((9.7, myy), 0.4, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_path(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((10.7, myy), 2.3, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_file(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((13.7, myy), 1.6, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_params(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((16, myy), 3.1, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_keys(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((16, myy), 1.7, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

def add_vals(axes, ypos, alph):
   myy = ypos-0.4
   axes.add_patch(mpatches.FancyBboxPatch((18, myy), 1.7, 0.4,
       boxstyle=mpatches.BoxStyle("Round", pad=0.2), alpha=alph, color='green')
   )

####################################################################
def get_plotable_features(file, fnames, importance, prefix=""):
    df = pd.read_csv(file)
    max_val = df[importance].max()
    df[importance] = df[importance]/(1.3*max_val)
    def map_to_group(x):
        x = x[len(prefix):]
        parts = x.split("_")
        if parts[0] in ["protocol", "subdomain", "domain", "tld", "path", "file", "params", "keys", "values"]:
            return parts[0]
        return "global" 
    df['fgroup'] = df[fnames].apply(map_to_group)
    grouped = df.groupby('fgroup')[importance].sum().reset_index()
    return dict(grouped.values)

####################################################################
def main(files, prefix, fnames, imports):
    fig, ax = plt.subplots( figsize=(8, 6))
    plt.gca().invert_yaxis()
    ax.plot([0, 20],[0, 20], alpha=0.0)
    example_url = "protocol://sub.domain.tld/path/way/file.ext?query=done"
    plt.text(3, 2, example_url, ha="left", family='sans-serif', size=11)
    ystart = 4
    for f in files:
        path_parts = f.split("/")
        fname = path_parts[len(path_parts)-1]
        name_parts = fname.split(".")
        plt.text(0, ystart, name_parts[0], ha="left", family='sans-serif', size=11)
        plotables = get_plotable_features(f, fnames, imports, prefix)
        if plotables.__contains__("global"):
            add_global(ax, ystart, plotables["global"])
        if plotables.__contains__("protocol"):
            add_protocol(ax, ystart, plotables["protocol"])
        if plotables.__contains__("path"):
            add_path(ax, ystart, plotables["path"])
        if plotables.__contains__("params"):
            add_params(ax, ystart, plotables["params"])
        if plotables.__contains__("domain"):
            add_domain(ax, ystart, plotables["domain"])
        if plotables.__contains__("subdomain"):
            add_subdomain(ax, ystart, plotables["subdomain"])
        if plotables.__contains__("tld"):
            add_tld(ax, ystart, plotables["tld"])
        if plotables.__contains__("file"):
            add_file(ax, ystart, plotables["file"])
        ystart += 2

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

########################################################################
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='URL Feature Importance Plotter')
    my_parser.add_argument('prefix',
                       metavar='prefix',
                       type=str,
                       help='String prefix for the column names')
    my_parser.add_argument('features',
                       metavar='features',
                       type=str,
                       help='Name of the column with the feature names')
    my_parser.add_argument('importance',
                       metavar='importance',
                       type=str,
                       help='Name of the column with the feature importance')

    my_parser.add_argument('data',
                       metavar='data',
                       type=str,
                       help='comma separated list of CSV files containing feature importance for URL features')

    args = my_parser.parse_args()
    data = args.data
    pfix = args.prefix
    fnames = args.features
    imports = args.importance

    files = data.split(",")
    for f in files:
       if not os.path.isfile(f):
          print(" ERROR")
          print(" The input file '%s' does not exist" % f)
          sys.exit()

    main(files, pfix, fnames, imports)

