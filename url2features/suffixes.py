# Function for processing the suffix from a domain
#
# Large parts of this code taken from bitquark's dnspop project
# https://github.com/bitquark/dnspop/blob/master/code/suffix_strip.py

from .process import load_file

####################################################################
 
lines = load_file('public_suffix_list.dat').split("\n")

# Build a list of domain suffixes using the public suffix list from publicsuffix.org
# Note that the file is read backwards to prevent, .uk superceding .co.uk, for example
public_suffixes = [('.' + line.replace('*.', '')) for line in reversed(lines) if line != '\n' and line != '' and line[0:2] != '//' and line[0] != '!']

# Domains with > 400k records in the 2016-02-13 Project Sonar Forward DNS data set and which
# don't supercede sub-TLD parts (e.g. .jp is excluded because of .ne.jp, .co.jp, etc)
common_suffixes = [ '.com', '.net', '.ne.jp', '.de', '.org', '.edu', '.nl', '.info', '.biz', '.co.uk', '.cz', '.dk',
                    '.com.cn', '.mil', '.ac.uk', '.ch', '.eu', '.com.br', '.co.za', '.ad.jp', '.ac.cn', '.com.au',
                    '.or.jp', '.net.au', '.asia', '.ac.jp', '.mobi', '.co.jp', '.sk', '.edu.tw', '.net.pl', '.gov' ]

# Create the suffix list
suffixes = common_suffixes + [_.rstrip() for _ in public_suffixes if _.rstrip() not in common_suffixes]


def split_domain_and_suffix(domain):
    """ Strip a domain of its suffix """
    domain = domain.rstrip()
    for suffix in suffixes:
        if domain.endswith(suffix):
            return domain[:-len(suffix)], domain[len(domain)-len(suffix):]
    # Unrecognised suffix
    parts = domain.split(".")
    if len(parts)>1:
        dom = domain[:-(len(parts[-1])+1)]
        return dom, parts[-1]
    else:
        return domain, ""

