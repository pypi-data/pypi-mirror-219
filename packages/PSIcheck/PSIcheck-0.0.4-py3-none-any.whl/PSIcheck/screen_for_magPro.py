import pandas as pd
import glob
import re
import os
import numpy as np
from Bio import SeqIO

# putative magnetosome gene patterns 
pattern1 = re.compile(r'[M][am][mdns][A-Z0-9]+')   
pattern2 = re.compile(r'[Mm]agnetosome')
pattern3 = re.compile(r'ferrous iron transporter [AB]')
pattern4 = re.compile(r'[A-Z]+[0-9._]+')
pattern5 = re.compile(r' [0-9][\.e][0-9\-]+')
# evalue<0.001

def check_putative_mgc_id_acc(psiblasted_txt): 
    ##screen putative magnetosome protein and return the dictionary
    with open(psiblasted_txt, 'r') as f:
        list_ = []
        for line in f:
            putative_magpro_condition = pattern1.search(line) or pattern2.search(line) or pattern3.search(line)
            if 'Query=' in line:
                list_.append(line)
            elif pattern4.match(line):
                if putative_magpro_condition:
                    list_.append(line)

    list_.append('blank line')

    genome_name = os.path.basename(psiblasted_txt).replace('.txt','')
    mgc_dict = {}
    idlist=[]
    namelist=[]
    acclist=[]
    evallist=[]
    namelist_tmp = []
    acclist_tmp = []
    evallist_tmp = []
    for i in range(len(list_)-1):
        if 'Query=' in list_[i]:
            if ('Query=' not in list_[i+1]) & ('blank' not in list_[i+1]):
                id = re.search('LOCUSTAG_[0-9]+', list_[i]).group()
                idlist.append(id)
                if namelist_tmp:
                    namelist.append(namelist_tmp)
                if acclist_tmp:
                    acclist.append(acclist_tmp)
                if evallist_tmp:
                    evallist.append(evallist_tmp)
                namelist_tmp = []
                acclist_tmp = []
                evallist_tmp = [] 
        elif pattern4.match(list_[i]) and pattern5.search(list_[i]):
            list_tmp = [i for i in list_[i].split(' ') if i.strip()]
            name_tmp = ' '.join(list_tmp[1:-2])
            p1 = pattern1.search(name_tmp)
            p3 = pattern3.search(name_tmp)
            p2 = pattern2.search(name_tmp)
            if p1:
                name = p1.group()
            elif p3:
                name = p3.group()
            elif p2:
                name = name_tmp
            namelist_tmp.append(name)
            acclist_tmp.append(list_tmp[0])
            evallist_tmp.append(pattern5.search(list_[i]).group().strip())
    if namelist_tmp:
        namelist.append(namelist_tmp)
    if acclist_tmp:
        acclist.append(acclist_tmp)
    if evallist_tmp:
        evallist.append(evallist_tmp)     
    mgc_dict = {'genomes': genome_name,
                'locustag' : idlist,
               'pro_name': namelist,
               'accession': acclist,
               'e-value': evallist} 
    return mgc_dict

def get_all_putative_mgc_csv(list_psiblasted_txts):
    df_list = []
    for txt in list_psiblasted_txts:
        df_tmp = pd.DataFrame.from_dict(check_putative_mgc_id_acc(txt)).explode(['pro_name','accession', 'e-value'])
        df_list.append(df_tmp)
    df_all = pd.concat(df_list)
    return df_all

def get_identity_value(df_all, list_psiblasted_txts):
    identities = {
        'genomes':[],
        'locustag':[],
        'accession':[],
        'identity':[],
        'e-value':[]
    }

    for txt in list_psiblasted_txts:# for each genome
        with open(txt) as f:
            content = f.read()
            query_elements = content.split('Query= ')
        genome = os.path.basename(txt).replace('.txt', '')
        df_genome_tmp = df_all[df_all.genomes == genome].copy()
        locs = df_genome_tmp.locustag.unique().tolist()
        for loc in locs:# for each locus
            ele = [i for i in query_elements if loc in i][0]
            align_fea_list = re.findall(r'(>[\s\S]+?), Positives ' ,ele)
            for acc in df_genome_tmp[df_genome_tmp.locustag == loc].accession.tolist():# for each match
                found = False
                for j in align_fea_list:
                    if acc in j:
                        found = True
                        iden = j.strip(')').split('(')[-1]
                        expect = re.search(r',  Expect = ([0-9e\-\.]+), Method: ', j).group(1)
                        identities['genomes'].append(genome)
                        identities['locustag'].append(loc)
                        identities['accession'].append(acc)
                        identities['identity'].append(iden)
                        identities['e-value'].append(expect)
                        break
                if not found:
                    identities['genomes'].append(genome)
                    identities['locustag'].append(loc)
                    identities['accession'].append(acc)
                    identities['identity'].append(np.nan)
                    identities['e-value'].append('in the list-like area')

    df_iden = pd.DataFrame(identities)
    return df_iden

def concat_df_all_iden(df_all, df_iden):
    df_all.set_index(['genomes','locustag','accession'],inplace = True)
    df_iden.set_index(['genomes','locustag','accession'], inplace=True)
    if not (df_all.index == df_iden.index).all():
        raise ValueError('The identitiy dataframe seems to have a different index with all_dataframe')
    df_all['identity'] = df_iden.identity
    df_all.reset_index(inplace=True)
    return df_all

def use_eval_iden_criteria(df_all):
    # first screen by iden>=0.3 and eval <0.001
    df_all['eval_float'] = df_all['e-value'].apply(float)
    def p2f(x):
        if type(x) == str:
            return float(x.strip('%'))/100
        else:
            return x
    iden_float = df_all.identity.apply(p2f)
    df_all['iden_float'] = iden_float
    df_meet_criteria = df_all[(df_all.eval_float < 0.001) & (df_all.iden_float >= 0.3)].copy()

    # then compare multiple matches for each locustag, choose the highest identity then the lowest evalue
    df_meet_criteria.sort_values(['genomes', 'locustag', 'iden_float','eval_float'], ascending=[True, True, False, True], inplace=True)
    df_meet_criteria.drop_duplicates(subset=['genomes', 'locustag'], inplace=True)
    return df_meet_criteria
           
def get_file_path(psi_res_path):
    list_psiblasted_txts = glob.glob(f'{psi_res_path}/*.txt')
    return list_psiblasted_txts

def check_and_reform(psi_res_path):
    list_psiblasted_txts = get_file_path(psi_res_path)
    num_of_files = len(list_psiblasted_txts)
    df_all_tmp = get_all_putative_mgc_csv(list_psiblasted_txts)
    df_iden = get_identity_value(df_all_tmp, list_psiblasted_txts)
    df_all = concat_df_all_iden(df_all_tmp, df_iden)
    df_meet_criteria = use_eval_iden_criteria(df_all)
    csv_file = os.path.join(psi_res_path,'PSIcheck_output.csv')
    df_meet_criteria.to_csv(csv_file,index=False)
    print(f'{num_of_files} file(s) checked! Thank you!')
    return csv_file

def modify_magPro_name_inGenbank(psi_out_csv, sliced_mgc_gbks_path):
    # This function will rename the checked magnetosome proteins accordding to csv file, 
    # and change the unmag-protein name to 'hypothetical protein'
    psi_out_csv = pd.read_csv(psi_out_csv)
    g = psi_out_csv.groupby('genomes')
    for n,df_tmp in g:
        loc_pro_dict = dict(zip(df_tmp.locustag.tolist(), df_tmp.pro_name.tolist()))
        gbk_file_name = n+'.gbk'
        gbk_file_path = os.path.join(sliced_mgc_gbks_path, gbk_file_name) 
        gbk_records = SeqIO.parse(gbk_file_path, 'genbank') # read in genbank file
        modified_records = []
        for record in gbk_records:
            for f in record.features:
                ftype = f.type
                if ftype == 'CDS':
                    floc = f.qualifiers['locus_tag'][0]
                    if floc in loc_pro_dict:
                        f.qualifiers['product'][0] = loc_pro_dict[floc]
                    else:
                        f.qualifiers['product'][0] = 'hypothetical protein'
            modified_records.append(record)
        modified_gbk_path = gbk_file_path.replace('.gbk','_renamed.gbk')
        SeqIO.write(modified_records, modified_gbk_path, 'genbank')

         