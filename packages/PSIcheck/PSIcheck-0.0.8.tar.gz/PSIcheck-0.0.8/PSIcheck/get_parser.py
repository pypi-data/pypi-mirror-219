def get_parser():
    import argparse
    CBOLD = '\33[1m'
    CEND = '\33[0m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    parser = argparse.ArgumentParser(
             prog="PSIcheck", 
             epilog=f"""

{CBOLD}Usage{CEND}


    {CRED}$ {CGREEN}PSIcheck{CEND} PsiResultPath


Runjia Ji, 2023
"""
            )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.8', help='show PSIcheck version number and exit')
    parser.add_argument('PsiResultPath', type=str, help='directory stores PSI-Blast results')
    parser.add_argument('-gbk','--GenbankFilesPath', type=str, help='directory stores Genbank files')

    args = parser.parse_args()
    return args

