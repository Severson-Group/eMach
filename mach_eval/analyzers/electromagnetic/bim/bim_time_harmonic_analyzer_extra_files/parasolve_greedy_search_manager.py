# coding:u8
# parasolve_greedy_search_manager

import os
import sys
import femm
from time import time, sleep
import operator
import subprocess

bool_remove_files = False

def savetofile(id_solver, freq, stack_length):
    femm.mi_probdef(freq, 'millimeters', 'planar', 1e-8, # must < 1e-8
                    stack_length, 18, 1) # The acsolver parameter (default: 0) specifies which solver is to be used for AC problems: 0 for successive approximation, 1 for Newton.
    femm.mi_saveas(dir_femm_temp+'femm_temp_%d.fem'%(id_solver))

def remove_files(list_solver_id, dir_femm_temp, suffix, id_solver_femm_found=None):
    print('Rename femm file for index', id_solver_femm_found, 'with suffix of', suffix, 'Others will be deleted.')
    for id_solver in list_solver_id:
        fname = dir_femm_temp + "femm_temp_%d"%(id_solver) + suffix

        if id_solver == id_solver_femm_found:
            found_file_name = dir_femm_temp + "femm_found" + suffix

            if os.path.exists(found_file_name):
                os.remove(found_file_name) # remove already existing file (due to interrupted run)

            if not os.path.exists(fname):
                raise Exception('FEMM file %s does not exist for id_solver=%d'%(fname, id_solver))

            os.rename(fname, found_file_name)
            if bool_remove_files:
                continue
            else:
                break

        # what if we don't remove temp file??? 2019/7/8
        if bool_remove_files:
            os.remove(fname)

# Inputs to this script
dir_femm_temp        = sys.argv[1]
expected_project_file        = sys.argv[2]
stack_length         = float(sys.argv[3])
freq_begin = float(sys.argv[4])
freq_end = float(sys.argv[5])
no_of_freqs = int(sys.argv[6])
VAREPSILON = float(sys.argv[7]) # difference between 1st and 2nd max torque slip frequencies

femm.openfemm(True)
femm.opendocument(expected_project_file)

list_torque    = []
list_slipfreq  = []
list_solver_id = [] 
list_done_id   = []

count_loop = 0
while True:
    # freq_step can be negative!
    freq_step  = (freq_end - freq_begin) / (no_of_freqs - 1)

    count_done = len(list_done_id)
    if count_done % 5 == 0:
        list_solver_id = list(range(0, count_done+no_of_freqs, 1))

    # parasolve
    procs = []
    print('list_solver_id=', list_solver_id)
    print('list_solver_id[-no_of_freqs:]=', list_solver_id[-no_of_freqs:])
    for i, id_solver in enumerate(list_solver_id[-no_of_freqs:]):
        savetofile(id_solver, freq_begin + i*freq_step, stack_length)

        proc = subprocess.Popen(
            [sys.executable, os.path.dirname(os.path.abspath(__file__)) + '/parasolve_greedy_search.py',
            str(id_solver), '"'+dir_femm_temp+'"'], bufsize=-1
            )
        procs.append(proc)

    # This wait is working if you run this scrirpt from sublime text
    for proc in procs:
        proc.wait() 

    count_sec = 0
    while True:
        sleep(1)
        count_sec += 1
        if count_sec > 120: # two min 
            raise Exception('It is highly likely that exception occurs during the solving of FEMM.')
        
        print('\nbegin waiting for eddy current solver...')
        for id_solver in list_solver_id[-no_of_freqs:]:

            if id_solver in list_done_id:
                continue

            fname = dir_femm_temp + "femm_temp_%d.txt"%(id_solver)
            # print fname
            if os.path.exists(fname):
                with open(fname, 'r') as f:
                    data = f.readlines()
                    # if data == []:
                    #     sleep(0.1)
                    #     data = f.readlines()
                    #     if data == []:
                    #         raise Exception('What takes you so long to write two float numbers?')
                    list_slipfreq.append( float(data[0][:-1]) )
                    list_torque.append(   float(data[1][:-1]) )
                list_done_id.append(id_solver)

        if len(list_done_id) >= no_of_freqs:
            break

    # print('-----------------------')
    # print list_solver_id
    print('slip freq [Hz]:', list_slipfreq)
    print('torque [Nm]:', list_torque)

    # find the 1st max
    list_torque_copy = list_torque[::]
    index_1st, breakdown_torque_1st = max(enumerate(list_torque_copy), key=operator.itemgetter(1))
    breakdown_slipfreq_1st = list_slipfreq[index_1st]
    print('The max is #%d'%index_1st, breakdown_torque_1st, 'Nm')

    # find the 2nd max
    list_torque_copy[index_1st] = -999999
    index_2nd, breakdown_torque_2nd = max(enumerate(list_torque_copy), key=operator.itemgetter(1))
    breakdown_slipfreq_2nd = list_slipfreq[index_2nd]
    print('2nd max is #%d'%index_2nd, breakdown_torque_2nd, 'Nm')

    print('Max slip freq error=', 0.5*(breakdown_slipfreq_1st - breakdown_slipfreq_2nd), 'Hz', ', 2*EPS=%g'%(VAREPSILON))

    # find the two slip freq close enough then break.5
    if abs(breakdown_slipfreq_1st - breakdown_slipfreq_2nd) < VAREPSILON: # Hz
        the_index = list_solver_id[index_1st]
        print('Found it.', breakdown_slipfreq_1st, 'Hz', breakdown_torque_1st, 'Nm', 'The index is', the_index)
        remove_files(list_solver_id, dir_femm_temp, suffix='.fem', id_solver_femm_found=the_index)
        remove_files(list_solver_id, dir_femm_temp, suffix='.ans', id_solver_femm_found=the_index)

        with open(dir_femm_temp + 'femm_found.csv', 'w') as f:
            f.write('%g\n%g\n'%(breakdown_slipfreq_1st, breakdown_torque_1st)) #, Qs_stator_slot_area, Qr_rotor_slot_area))
        break

    else:
        print('Not yet.')
        count_loop += 1
        if count_loop > 100:
            os.system('pause')

        # not found yet, try new frequencies.
        if breakdown_slipfreq_1st > breakdown_slipfreq_2nd:
            if breakdown_slipfreq_1st == list_slipfreq[-1]:
                freq_begin = breakdown_slipfreq_1st + freq_step
                freq_end   = freq_begin + no_of_freqs - freq_step
            else:
                freq_begin = breakdown_slipfreq_1st
                freq_end   = breakdown_slipfreq_2nd
                freq_step  = (freq_end - freq_begin) / (2 + no_of_freqs - 1) 
                freq_begin += freq_step
                freq_end   -= freq_step

        elif breakdown_slipfreq_1st < breakdown_slipfreq_2nd:
            freq_begin = breakdown_slipfreq_1st
            freq_end   = breakdown_slipfreq_2nd

            # freq_step can be negative!
            freq_step  = (freq_end - freq_begin) / (2 + no_of_freqs - 1)
            freq_begin += freq_step
            freq_end   -= freq_step
        print('try: freq_begin=%g, freq_end=%g.' % (freq_begin, freq_end))

remove_files(list_solver_id, dir_femm_temp, suffix='.txt')
if bool_remove_files:
    os.remove(dir_femm_temp + "femm_temp.fem")

femm.mi_close()
femm.closefemm()

