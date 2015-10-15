# -*- coding: utf-8 -*-
# Derived from EEG-open22.py, but with graphing capability removed
# In version EEG_generate_h5_10.py, began adding functionality for saving absolute values
"""
Created on Sun Jan  4 13:42:48 2015
EEG_generate_h5.py deriived from EEG_generate_h5_12.py October 15, 2015

@author: David Trowbridge
"""
import numpy as np
from pandas import DataFrame
import pandas as pd
import datetime
#import time
#import tkinter as Tk
"""
The purpose of this program is to convert the EEG data in the CSV file
created by Muse Player (from an original .muse file) into a set of .h5
files that can be used by the program Phys_Viewer.py.

The .CSV file must be named 'rec<N>.CVS' where N is an integer 
(e.g., 'rec25.CSV') and located in the hard-wired directory C:\MuseRec

Files generated by this program are saved in the same directory as
as the file EEG_generate_h5.py. They are,
rec25_eeg.abs.h5   (absolute power values, range [-1:+1])
rec25_eeg.raw.h5   (raw EEG voltages)
rec25_eeg.rel.h5   (relative power values, range [0:1])
rec25_eeg.user.h5  (blink, jaw clench, concentration and mellow)

IMPORTANT: After these files are generated, they must be MOVED into the 
directory C:\MedRec or else they will not be found by Phy_Viewer.py

Note: a separate file conversion program, Cardio_generate_h5.py
works similarly, starting with a .TXT file exported by Logger Pro
and generating files for ECG and respiration,
rec25_breath.h5   (pressures from Vernier Respiration Monitor)
rec25_cardio.h5   (millivolt signal from Vernier Electrocardiogram)

When EEG_generate_h5.py runs, type the desired session name at the prompt,
'CSV filename (without extension)' e.g., 'rec25'

"""
path = 'C:\\MuseRec\\'

print('path: '+path)
session = input('CSV filename (without extension): ')

#start()
lines = [x.rstrip() for x in open(path+session+'.CSV')] # a list of strings

print('Number of lines: '+str(len(lines)))
print('First line: '+str(lines[0]))
#print('Time to open CSV file: '+str(time.clock()-start_time)+' seconds')
#elapsed_time('Time to open CSV file and prepare list of lines')

#description = input('Description: ')
description = ''

#start()
line_strings = [] # a list of lists of strings
for i in range(len(lines)):
    line_strings.append(lines[i].split(','))
#print('len(line_strings) = '+str(len(line_strings)))
#print('line_strings[0] = '+str(line_strings[0]))
#print('line_strings[1] = '+str(line_strings[1]))
#elapsed_time('Time to split strings at comma delimiters')
    
timezero = float(line_strings[0][0])

duration = float(line_strings[len(lines)-1][0]) - timezero

recordingtime = datetime.datetime.fromtimestamp(int(timezero)
    ).strftime('%Y-%m-%d %H:%M:%S')
    

du = [] # list of delta band absolute values
tu = [] # list of theta band absolute values
au = [] # list of alpha band absolute values
bu = [] # list of beta band absolute values
gu = [] # list of gamma band absolute values
dv = [] # list of delta band relative values
tv = [] # list of theta band relative values
av = [] # list of alpha band relative values
bv = [] # list of beta band relative values
gv = [] # list of gamma band relative values
xv = [] # list of left/right (x) acceleration values
kv = [] # list of blink values
jv = [] # list of jaw clench values
cv = [] # list of concentration values
mv = [] # list of mellow values
eeg = [] # list of eeg values

"""
Col0 = [row[0] for row in dv]

for row in dv:
    del row[0]
"""

#start()
#acceptacc = False
#for i in range(508800):
for i in range(len(line_strings)):
    ms = int(1000*(float(line_strings[i][0])-timezero)) ## computer millisocond time value
    if 'delta_absolute' in line_strings[i][1]:
        du.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'theta_absolute' in line_strings[i][1]:
        tu.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'alpha_absolute' in line_strings[i][1]:
        au.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'beta_absolute' in line_strings[i][1]:
        bu.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'gamma_absolute' in line_strings[i][1]:
        gu.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'delta_relative' in line_strings[i][1]:
        dv.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'theta_relative' in line_strings[i][1]:
        tv.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'alpha_relative' in line_strings[i][1]:
        av.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'beta_relative' in line_strings[i][1]:
        bv.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'gamma_relative' in line_strings[i][1]:
        gv.append([ms/1000.0, float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])
    elif 'blink' in line_strings[i][1]:
        kv.append([ms/1000.0, (float(line_strings[i][2]))*0.5]) # Max value of blink (1) will be displayed in graph as 0.5
    elif 'jaw_clench' in line_strings[i][1]:
        jv.append([ms/1000.0, (float(line_strings[i][2]))*0.35]) # Max value of jaw_clench (1) will be displayed in graph as 0.5
    elif 'concentration' in line_strings[i][1]:
        cv.append([ms/1000.0, (float(line_strings[i][2]))*0.6]) # Max value of concentration will be displayed in graph as 0.75
    elif 'mellow' in line_strings[i][1]:
        mv.append([ms/1000.0, (float(line_strings[i][2]))*0.6]) # Max value of mellow will be displayed in graph as 0.75
    elif ('eeg' in line_strings[i][1]) and not ('quantization' in line_strings[i][1]):
        eeg.append([float(line_strings[i][2]), float(line_strings[i][3]), float(line_strings[i][4]), float(line_strings[i][5])])

print('len(du) = '+str(len(du)))
print('len(tu) = '+str(len(tu)))
print('len(au) = '+str(len(au)))
print('len(bu) = '+str(len(bu)))
print('len(gu) = '+str(len(gu)))
print('len(dv) = '+str(len(dv)))
print('len(tv) = '+str(len(tv)))
print('len(av) = '+str(len(av)))
print('len(bv) = '+str(len(bv)))
print('len(gv) = '+str(len(gv)))

r_ulen = len(du) - 10 #range is reduced by 10 to avoid IndexError when data for other freq bands has fewer indices
r_urange = range(r_ulen)
r_vlen = len(dv) - 10 #range is reduced by 10 to avoid IndexError when data for other freq bands has fewer indices
r_vrange = range(r_vlen)

for i in r_urange: # Compute mean values for 4 sensors; append to list of values
    du[i].append((du[i][1]+du[i][2]+du[i][3]+du[i][4])/4.0) 
    tu[i].append((tu[i][1]+tu[i][2]+tu[i][3]+tu[i][4])/4.0) 
    au[i].append((au[i][1]+au[i][2]+au[i][3]+au[i][4])/4.0) 
    bu[i].append((bu[i][1]+bu[i][2]+bu[i][3]+bu[i][4])/4.0) 
    gu[i].append((gu[i][1]+gu[i][2]+gu[i][3]+gu[i][4])/4.0) 

for i in r_vrange: # Compute mean values for 4 sensors; append to list of values
    dv[i].append((dv[i][1]+dv[i][2]+dv[i][3]+dv[i][4])/4.0) 
    tv[i].append((tv[i][1]+tv[i][2]+tv[i][3]+tv[i][4])/4.0) 
    av[i].append((av[i][1]+av[i][2]+av[i][3]+av[i][4])/4.0) 
    bv[i].append((bv[i][1]+bv[i][2]+bv[i][3]+bv[i][4])/4.0) 
    gv[i].append((gv[i][1]+gv[i][2]+gv[i][3]+gv[i][4])/4.0) 


ut = [du[i][0] for i in np.arange(r_ulen)]
vt = [dv[i][0] for i in np.arange(r_vlen)]

# Absolute values
r_du = np.arange(r_ulen)
udelta_df = DataFrame({
'dlb': [du[i][1] for i in r_du],
'dlf': [du[i][2] for i in r_du],
'drf': [du[i][3] for i in r_du],
'drb': [du[i][4] for i in r_du],
'd_m': [du[i][5] for i in r_du]}, 
index = ut, columns=['dlb','dlf','drf','drb','d_m'])

r_tu = np.arange(r_ulen)
utheta_df = DataFrame({
'tlb': [tu[i][1] for i in r_tu],
'tlf': [tu[i][2] for i in r_tu],
'trf': [tu[i][3] for i in r_tu],
'trb': [tu[i][4] for i in r_tu],
't_m': [tu[i][5] for i in r_tu]}, 
index = ut, columns=['tlb','tlf','trf','trb','t_m'])

r_au = np.arange(r_ulen)
ualpha_df = DataFrame({
'alb': [au[i][1] for i in r_au],
'alf': [au[i][2] for i in r_au],
'arf': [au[i][3] for i in r_au],
'arb': [au[i][4] for i in r_au],
'a_m': [au[i][5] for i in r_au]}, 
index= ut, columns=['alb','alf','arf','arb','a_m'])

r_bu = np.arange(r_ulen)
ubeta_df = DataFrame({
'blb': [bu[i][1] for i in r_bu],
'blf': [bu[i][2] for i in r_bu],
'brf': [bu[i][3] for i in r_bu],
'brb': [bu[i][4] for i in r_bu],
'b_m': [bu[i][5] for i in r_bu]}, 
index= ut, columns=['blb','blf','brf','brb','b_m'])

r_gu = np.arange(r_ulen)
ugamma_df = DataFrame({
'glb': [gu[i][1] for i in r_gu],
'glf': [gu[i][2] for i in r_gu],
'grf': [gu[i][3] for i in r_gu],
'grb': [gu[i][4] for i in r_gu],
'g_m': [gu[i][5] for i in r_gu]}, 
index= ut, columns=['glb','glf','grf','grb','g_m'])

# Relative values
r_dv = np.arange(r_vlen)
delta_df = DataFrame({
'dlb': [dv[i][1] for i in r_dv],
'dlf': [dv[i][2] for i in r_dv],
'drf': [dv[i][3] for i in r_dv],
'drb': [dv[i][4] for i in r_dv],
'd_m': [dv[i][5] for i in r_dv]}, 
index = vt, columns=['dlb','dlf','drf','drb','d_m'])

r_tv = np.arange(r_vlen)
theta_df = DataFrame({
'tlb': [tv[i][1] for i in r_tv],
'tlf': [tv[i][2] for i in r_tv],
'trf': [tv[i][3] for i in r_tv],
'trb': [tv[i][4] for i in r_tv],
't_m': [tv[i][5] for i in r_tv]}, 
index = vt, columns=['tlb','tlf','trf','trb','t_m'])

r_av = np.arange(r_vlen)
alpha_df = DataFrame({
'alb': [av[i][1] for i in r_av],
'alf': [av[i][2] for i in r_av],
'arf': [av[i][3] for i in r_av],
'arb': [av[i][4] for i in r_av],
'a_m': [av[i][5] for i in r_av]}, 
index= vt, columns=['alb','alf','arf','arb','a_m'])

r_bv = np.arange(r_vlen)
beta_df = DataFrame({
'blb': [bv[i][1] for i in r_bv],
'blf': [bv[i][2] for i in r_bv],
'brf': [bv[i][3] for i in r_bv],
'brb': [bv[i][4] for i in r_bv],
'b_m': [bv[i][5] for i in r_bv]}, 
index= vt, columns=['blb','blf','brf','brb','b_m'])

r_gv = np.arange(r_vlen)
gamma_df = DataFrame({
'glb': [gv[i][1] for i in r_gv],
'glf': [gv[i][2] for i in r_gv],
'grf': [gv[i][3] for i in r_gv],
'grb': [gv[i][4] for i in r_gv],
'g_m': [gv[i][5] for i in r_gv]}, 
index= vt, columns=['glb','glf','grf','grb','g_m'])

"""
t_xv = [xv[i][0] for i in np.arange(len(xv))]
r_xv = np.arange(len(xv))
sway_df = DataFrame({
'x': [xv[i][1] for i in r_xv]},
index=t_xv, columns=['x'])
"""

r_kv = np.arange(r_vlen)
print('len(kv) = '+str(len(kv)))
blink_df = DataFrame({
'k': [kv[i][1] for i in r_kv]},
index=vt, columns=['k'])

r_jv = np.arange(r_vlen)
print('len(jv) = '+str(len(jv)))
jaw_df = DataFrame({
'j': [jv[i][1] for i in r_jv]},
index=vt, columns=['j'])

r_cv = np.arange(r_vlen)
print('len(cv) = '+str(len(cv)))
concentration_df = DataFrame({
'c': [cv[i][1] for i in r_cv]},
index=vt, columns=['c'])

r_mv = np.arange(r_vlen)
print('len(mv) = '+str(len(mv)))
mellow_df = DataFrame({
'm': [mv[i][1] for i in r_mv]},
index=vt, columns=['m'])

r_eeg = np.arange(len(eeg))
eeg_df = DataFrame({
'lb': [eeg[i][0] for i in r_eeg],
'lf': [eeg[i][1] for i in r_eeg],
'rf': [eeg[i][2] for i in r_eeg],
'rb': [eeg[i][3] for i in r_eeg]},
columns=['lb','lf','rf','rb'])

def save_data():
    """
    This code works when it is within the function save_data()
    Outside the function, there is a problem with the pd.concat()
    function which results in Spyder crashing (unresponsive)
    after the .h5 files have been saved.
    """
    absolute_df = pd.concat({
        'delta': udelta_df,
        'theta': utheta_df,
        'alpha': ualpha_df,
        'beta': ubeta_df,
        'gamma': ugamma_df},
        axis=1, join='inner', keys=['delta','theta','alpha','beta','gamma'])
#    print('absolute_df')
#    print(absolute_df)
    
    absolute_store = pd.HDFStore(session+'_eeg_abs.h5')
    absolute_store['abs_data'] = absolute_df
    absolute_store.close() # This is important!
    
    relative_df = pd.concat({
        'delta': delta_df,
        'theta': theta_df,
        'alpha': alpha_df,
        'beta': beta_df,
        'gamma': gamma_df},
        axis=1, join='inner', keys=['delta','theta','alpha','beta','gamma'])
#    print('relative_df')
#    print(relative_df)
    
    relative_store = pd.HDFStore(session+'_eeg_rel.h5')
    relative_store['rel_data'] = relative_df
    relative_store.close() # This is important!
    
    user_df = pd.concat({
#        'x': sway_df,
        'k': blink_df,
        'j': jaw_df,
        'c': concentration_df,
        'm': mellow_df},
        axis=1, keys=['k','j','c','m'])
#    print('user_df')
#    print(user_df)
        
    user_store = pd.HDFStore(session+'_eeg_user.h5')
    user_store['user_data'] = user_df
    user_store.close() # This is important!
    
    r_eeg = np.arange(len(eeg))
    raw_df = DataFrame({
    'lb': [eeg[i][0] for i in r_eeg],
    'lf': [eeg[i][1] for i in r_eeg],
    'rf': [eeg[i][2] for i in r_eeg],
    'rb': [eeg[i][3] for i in r_eeg]},
    columns=['lb','lf','rf','rb'])

    raw_store = pd.HDFStore(session+'_eeg_raw.h5')
    raw_store['raw_data'] = raw_df
    raw_store.close() # This is important!
    
save_data()

