#AthMethPre Xiang, S., et al., AthMethPre: a web server for the prediction and query of mRNA m 6 A sites in Arabidopsis thaliana. Molecular BioSystems, 2016. 12(11): p. 3333-3337.
import pandas as pd
import numpy as np
import itertools
import os
import sys

dataset_name="trainset"
gene_type=sys.argv[3]
type_value="U"
if gene_type=="RNA":
    type_value="U"
elif gene_type=="DNA":
    type_value="T"
    
k = int(sys.argv[5])



def read_fasta_file(path):
    '''
    used for load fasta data and transformd into numpy.array format
    '''
    fh=open(m6a_benchmark_dataset)
    seq=[]
    for line in fh:
        if line.startswith('>'):
            continue
        else:
            seq.append(line.strip())
    fh.close()
    matrix_data=np.array([list(e) for e in seq])
    #print matrix_data
    return matrix_data

def AthMethPre_extract_one_line(data_line):
    '''
    extract features from one line, such as one m6A sample
    '''
    A=[0,0,0,1]
    T=[0,0,1,0]
    C=[0,1,0,0]
    G=[1,0,0,0]
    N=[0,0,0,0]
    feature_representation={"A":A,"C":C,"G":G,"N":N}
    feature_representation[type_value]=T
    beginning=0
    end=len(data_line)-1
    one_line_feature=[]
    alphabet='ACNG'
    alphabet+=type_value
    matrix_two=["".join(e) for e in itertools.product(alphabet, repeat=k)] # AA AU AC AG UU UC ...
    feature_two=np.zeros(5**k)
    for index,data in enumerate(data_line):
        if "".join(data_line[index:(index+k)]) in matrix_two and index <= end-1:
            feature_two[matrix_two.index("".join(data_line[index:(index+k)]))]+=1
    sum_two=np.sum(feature_two)
    one_line_feature.extend(feature_two/sum_two)
    return one_line_feature


def AthMethPre_extract_one_line_without(data_line):
    '''
    extract features from one line, such as one m6A sample
    '''
    A=[0,0,0,1]
    U=[0,0,1,0]
    C=[0,1,0,0]
    G=[1,0,0,0]
    N=[0,0,0,0]
    feature_representation={"A":A,"C":C,"G":G,"N":N}
    feature_representation[type_value]=U
    beginning=0
    end=len(data_line)-1
    one_line_feature=[]
    alphabet='ACG'
    alphabet+=type_value
    matrix_two=["".join(e) for e in itertools.product(alphabet, repeat=k)] # AA AU AC AG UU UC ...
    feature_two=np.zeros(4**k)
    for index,data in enumerate(data_line):
        if "".join(data_line[index:(index+k)]) in matrix_two and index <= end-1:
            feature_two[matrix_two.index("".join(data_line[index:(index+k)]))]+=1
    sum_two=np.sum(feature_two)
    one_line_feature.extend(feature_two/sum_two)
    return one_line_feature



def AthMethPre_feature_extraction(matrix_data,fill_NA):
    if fill_NA=="1":
        final_feature_matrix=[AthMethPre_extract_one_line(e) for e in matrix_data]
    elif fill_NA=="0":
        final_feature_matrix=[AthMethPre_extract_one_line_without(e) for e in matrix_data]
    return final_feature_matrix


fill_NA=sys.argv[4]
if fill_NA=="1":
    m6a_benchmark_dataset=sys.argv[1]
    matrix_data=read_fasta_file(m6a_benchmark_dataset)
    final_feature_matrix=AthMethPre_feature_extraction(matrix_data,fill_NA)
    print(np.array(final_feature_matrix).shape)
    pd.DataFrame(final_feature_matrix).to_csv(sys.argv[2],header=None,index=False)
elif fill_NA=="0":
    m6a_benchmark_dataset=sys.argv[1]
    matrix_data=read_fasta_file(m6a_benchmark_dataset)
    final_feature_matrix=AthMethPre_feature_extraction(matrix_data,fill_NA)
    print(np.array(final_feature_matrix).shape)
    pd.DataFrame(final_feature_matrix).to_csv(sys.argv[2],header=None,index=False)



