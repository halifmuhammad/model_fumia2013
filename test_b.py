import json,itertools,pytest
from os.path import exists
from numpy.random import random
from boolean3_addon import attr_cy, to_logic
from pdb import set_trace
from boolean3_addon import to_logic 
from os.path import exists,dirname
import pandas as pd
from tqdm import tqdm 

import model_fumia2013
from model_fumia2013 import rule
from model_fumia2013.rule import *


def test_32ic(force, progress):
    
    if exists(chk_with_32cond) and force == False:
        return;

    import engine 

    inputs = [ {
        'State_Mutagen' : State_Mutagen, 
        'State_GFs': State_GFs,
        'State_Nutrients': State_Nutrients,
        'State_TNFalpha': State_TNFalpha,
        'State_Hypoxia': State_Hypoxia,
        'State_Gli': False,
        } for State_Mutagen,State_GFs,State_Nutrients,State_TNFalpha, \
            State_Hypoxia in itertools.product([False,True], repeat=5)]

    results = []

    for sim_input in tqdm(inputs, ascii=True):
        on_states = [] 
        off_states = [] 
        for lbl in sim_input:
            if sim_input[lbl] == True: 
                on_states.append(lbl)
            else: 
                off_states.append(lbl)

        res = attr_cy.parallel(engine, steps=steps, samples=samples, 
                                repeats=repeats, on_states=on_states,
                                off_states=off_states)
        res = attach_phenotype({'input_condition': sim_input, 'simul_result': res})        
        
        results.append(res)
    
    json.dump(results, open(chk_with_32cond, 'w'), indent=4)


def test_32ic_summary(force, progress):
    
    if exists(output_b1_summary) and force == False:
        return;

    with open(chk_with_32cond,'r') as fin:
        res32 = json.load(fin)

    df0 = pd.DataFrame([], columns=['input','phenotype','ratio'])
    inplabels = [
        'State_Mutagen',
        'State_GFs',
        'State_Nutrients',
        'State_TNFalpha',
        'State_Hypoxia' 
        ]
    k = 0 
    for res in res32:
        res = attach_phenotype(res)
        inpcond = res['input_condition']        
        inputstring = "".join(["1" if inpcond[x] else "0" for x in inplabels])
        attrs = res['simul_result']['attractors']
        for att in attrs: 
            phenotype = attrs[att]['phenotype']
            ratio = attrs[att]['ratio']
            df0.loc[k] = {
                'input':inputstring,
                'phenotype':phenotype,
                'ratio': ratio
                }
            k += 1
                
    df0.groupby(['input','phenotype']).sum().to_csv(output_b1_summary)


fumia_model = join(dirname(model_fumia2013.__file__),
    'output-a1-fumia-model-processed-weighted-sum.txt')

chk_with_32cond = join(dirname(model_fumia2013.__file__), 
    'chk-with-32ic.json')

output_b1_summary = join(dirname(model_fumia2013.__file__), 
    'output-b1-32ic-summary.csv')

with open(fumia_model, 'r') as fobj:
    lines = fobj.readlines()
    lines2 = [] 
    for lin in lines: 
        lin = lin.strip()
        if lin[0] == '#': 
            continue 
        right = lin.split('=')[1].strip()
        if right == 'input':            
            lines2.append( lin.split('=')[0].strip() + '=' + 'False') 
        else: 
            lines2.append(lin)

    modeltext = "\n".join(lines2)

attr_cy.build(modeltext, pyx='engine.pyx', weighted_sum=True)

import pyximport; pyximport.install()

template = {
    'State_Mutagen' : False,
    'State_GFs': False,
    'State_Nutrients': False,
    'State_TNFalpha': False,
    'State_Hypoxia': False,
    'State_Gli': False,
    }

steps = 60
samples = 10
repeats = 100

