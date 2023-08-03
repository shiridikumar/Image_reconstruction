import pandas as pd
import numpy as np
import random 

def generate_dna_sequences(n):
    dna_sequences = []
    nucleotides = ['A', 'C', 'G', 'T']      
    for _ in range(n):
        k=random.randint(500,1500)
        sequence = ''.join(random.choices(nucleotides, k=k))
        dna_sequences.append(sequence)

    return dna_sequences

# n = int(input("Enter the number of DNA sequences to generate: "))
n=10000
sequences = generate_dna_sequences(n)
df=pd.DataFrame()
df["id"]=range(1,len(sequences)+1)
df["seq"]=sequences
df.set_index("id",inplace=True)
df.to_csv("D3.csv")