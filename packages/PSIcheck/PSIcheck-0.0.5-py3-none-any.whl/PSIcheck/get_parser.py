def get_parser():
    import argparse
    
    parser = argparse.ArgumentParser(
             prog="PSIcheck", 
            )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.5', help='show PSIcheck version number and exit')
    parser.add_argument('PsiResultPath', type=str, help='directory stores PSI-Blast results')
    parser.add_argument('-gbk','--GenbankFilesPath', type=str, help='directory stores Genbank files')

    args = parser.parse_args()
    return args

