#!bin/env/python
import argparse
import os
import pandas as pd
import re

parser = argparse.ArgumentParser()

parser.add_argument("-i", dest="input", help="input file generated by running contact_diffs.py", required=True)
parser.add_argument("-o", dest="output", help="output file name", required=True)
args = parser.parse_args()

def compare_files(test_file):
    with open(test_file) as parsed_file:
        C_sites = []
        for line in parsed_file:
            #match = re.search(r'501',line)
            match = re.search(r'44|45|46|47|48|49|50|51|52|53|54|273|275|276|277|278|279|280|285|296|297|299|300|304|305|308|309|310',line)
            if match:
                print(line)
                C_sites.append(line)
    return C_sites

C_adj = compare_files(args.input)
#print(rbs_adj)
diff_df = pd.DataFrame(C_adj)
diff_df.to_csv(args.output)

