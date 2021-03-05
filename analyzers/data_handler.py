# coding:u8
import os
import datetime
import itertools
import math
import numpy as np
import pygmo as pg
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import ast


def csv_row_reader(handle):
    from csv import reader
    read_iterator = reader(handle, skipinitialspace=True)
    return whole_row_reader(read_iterator)        

def whole_row_reader(reader):
    for row in reader:
        yield row[:]
        
def read_csv_results(study_name, path_prefix, configuration):
    # Torque
    basic_info = []
    time_list = []
    TorCon_list = []
    with open(path_prefix + study_name + '_torque.csv', 'r') as f:
        count = 0
        for row in csv_row_reader(f):
            count +=1
            if count<=8:
                try:
                    float(row[1])
                except:
                    continue
                else:
                    basic_info.append((row[0], float(row[1])))
            else:
                time_list.append(float(row[0]))
                TorCon_list.append(float(row[1]))

    # Force
    basic_info = []
    # time_list = []
    ForConX_list = []
    ForConY_list = []
    with open(path_prefix + study_name + '_force.csv', 'r') as f:
        count = 0
        for row in csv_row_reader(f):
            count +=1
            if count<=8:
                try:
                    float(row[1])
                except:
                    continue
                else:
                    basic_info.append((row[0], float(row[1])))
            else:
                # time_list.append(float(row[0]))
                ForConX_list.append(float(row[1]))
                ForConY_list.append(float(row[2]))
    ForConAbs_list = np.sqrt(np.array(ForConX_list)**2 + np.array(ForConY_list)**2 )

    # Current
    key_list = []
    current_voltage_dict = {}
    with open(path_prefix + study_name + '_circuit_current.csv', 'r') as f:
        count = 0
        for row in csv_row_reader(f):
            count +=1
            if count<=8:
                if 'Time' in row[0]: # Time(s)
                    for key in row:
                        key_list.append(key)
                        current_voltage_dict[key] = []
                else:
                    continue
            else:
                for ind, val in enumerate(row):
                    current_voltage_dict[key_list[ind]].append(float(val))

    # Terminal Voltage 
    new_key_list = []
    if configuration['delete_results_after_calculation'] == False:
        # file name is by individual_name like ID32-2-4_EXPORT_CIRCUIT_VOLTAGE.csv rather than ID32-2-4Tran2TSS_circuit_current.csv
        fname = path_prefix + study_name[:-8] + "_EXPORT_CIRCUIT_VOLTAGE.csv"
        # print 'Terminal Voltage - look into:', fname
        with open(fname, 'r') as f:
            count = 0
            for row in csv_row_reader(f):
                count +=1
                if count==1: # Time | Terminal1 | Terminal2 | ... | Termial6
                    if 'Time' in row[0]: # Time, s
                        for key in row:
                            new_key_list.append(key) # Yes, you have to use a new key list, because the ind below bgeins at 0.
                            current_voltage_dict[key] = []
                    else:
                        raise Exception('Problem with csv file for terminal voltage.')
                else:
                    for ind, val in enumerate(row):
                        current_voltage_dict[new_key_list[ind]].append(float(val))
    key_list += new_key_list

    # Loss
    # Iron Loss
    with open(path_prefix + study_name + '_iron_loss_loss.csv', 'r') as f:
        count = 0
        for row in csv_row_reader(f):
            count +=1
            if count>7:
                print('This should be 0:', float(row[0]))
                rotor_iron_loss = float(row[1]) # Rotor Core
                stator_iron_loss = float(row[3]) # Stator Core
                break                    
    with open(path_prefix + study_name + '_joule_loss_loss.csv', 'r') as f:
        count = 0
        for row in csv_row_reader(f):
            count +=1
            if count>7:
                rotor_eddycurrent_loss  = float(row[1]) # Rotor Core
                stator_eddycurrent_loss = float(row[3]) # Stator Core
                break
    with open(path_prefix + study_name + '_hysteresis_loss_loss.csv', 'r') as f:
        count = 0
        for row in csv_row_reader(f):
            count +=1
            if count>7:
                rotor_hysteresis_loss  = float(row[1]) # Rotor Core
                stator_hysteresis_loss = float(row[3]) # Stator Core
                break

    # Joule Loss (Copper and Magnet)
    magnet_loss_list = []
    with open(path_prefix + study_name + '_joule_loss.csv', 'r') as f:
        count = 0
        for row in csv_row_reader(f):
            count +=1
            if count == 7: # 少一个slip变量，所以不是8，是7。
                headers = row
                for idx_coil, h in enumerate(headers):
                    if 'Magnet' in h:
                        break

            if count>7:
                if 'Magnet' not in headers[idx_coil]:
                    print(headers)
                    raise Exception('Error when load csv data for Magnet.')
                magnet_loss_list.append(float(row[idx_coil])) # Magnet

    magnet_loss_2TS_part = magnet_loss_list[-int(0.5*configuration['number_of_steps_per_rev_2TS']*configuration['number_of_revolution_2TS']):] # number_of_steps_2ndTTS = steps for half peirod

    magnet_loss = sum(magnet_loss_2TS_part) / len(magnet_loss_2TS_part)
    print('Magnet loss:', magnet_loss)

    fea_output_dict = {
                          'time_list'            : time_list,
                          'torque_list'          : TorCon_list,
                          'forceX_list'          : ForConX_list,
                          'forceY_list'          : ForConY_list,
                          'current_voltage_dict' : current_voltage_dict,
                          'magnet_loss'          : magnet_loss,
                          'stator_iron_loss'     : stator_iron_loss,
                          'rotor_iron_loss'      : rotor_iron_loss,                     
                        }                           

    return fea_output_dict

def write_swarm_survivor(output_dir, pop, pop_size):
    print('Saving swarm survivor')
    with open(output_dir + 'swarm_survivor.txt', 'w') as f:
        f.write('\n---------%d\n'%(pop_size) \
                + '\n'.join(','.join('%.16f'%(x) for x in el[0].tolist() + el[1].tolist() ) for el in zip(pop.get_x(), pop.get_f()) )) # convert 2d array to string

def read_swarm_survivor(output_dir):

    if not os.path.exists(output_dir + 'swarm_survivor.txt'):
        print('\tNo file!')
        return None
    print('\tRead in', output_dir + 'swarm_survivor.txt')
    with open(output_dir + 'swarm_survivor.txt', 'r') as f:
        buf = f.readlines()
        length_buf = len(buf)      
        number_of_chromosome = length_buf-6
        if number_of_chromosome == 0:
            return None
        swarm_raw = [buf[i] for i in range(2, len(buf))]
        swarm_archive_x = extract_x_from_survivor(swarm_raw)
        print(len(swarm_archive_x))
        return swarm_archive_x 
    
def extract_x_from_survivor(swarm_raw):

    swarm_archive_xf = []
    for raw in swarm_raw:
        x_extract = ([float(x) for x in raw.split(',')])
        if x_extract[2] < 49:
            swarm_archive_xf.append(x_extract)
    swarm_archive_x =  [xf[:-3] for xf in swarm_archive_xf]

    return swarm_archive_x    

def read_swarm_data(output_dir):

    if not os.path.exists(output_dir + 'swarm_data.txt'):
        print('\tNo file!')
        return None
    print('\tRead in', output_dir + 'swarm_data.txt')
    with open(output_dir + 'swarm_data.txt', 'r') as f:
        buf = f.readlines()
        buf = buf[1:]
        length_buf = len(buf) 
        if length_buf % 21 == 0:
            pass
        else:
            raise Exception('Invalid swarm_data.txt!')
        number_of_chromosome = length_buf / 21
        if number_of_chromosome == 0:
            return None
        swarm_data_raw = [buf[i:i+21] for i in range(0, len(buf), 21)]
        swarm_data_xf = extract_xf_from_swarm_v2(swarm_data_raw)
        return swarm_data_xf 

def extract_xf_from_swarm_v2(swarm_data_raw):

    swarm_data_xf = []
    for raw in swarm_data_raw:
        design_parameters_denorm = [float(x) for x in raw[5].split(',')]
        loc1 = raw[2].find('f1')
        loc2 = raw[2].find('f2')
        loc3 = raw[2].find('f3')
        f1 = float(raw[2][loc1+3:loc2-1])
        f2 = float(raw[2][loc2+3:loc3-1])
        f3 = float(raw[2][loc3+3:])
        x_denorm = get_x_denorm_from_design_parameters(design_parameters_denorm)
        if f3 < 5 and f2 < -0.91 and x_denorm[2] < 49:
            swarm_data_xf.append(x_denorm + [f1, f2, f3])
    return swarm_data_xf

  
def read_swarm_archive(output_dir):

    if not os.path.exists(output_dir + 'swarm_archive.txt'):
        print('\tNo file!')
        return None, None, None, None
    print('\tRead in', output_dir + 'swarm_archive.txt')
    with open(output_dir + 'swarm_archive.txt', 'r') as f:
        buf = f.readlines()
        length_buf = len(buf)      
        if length_buf % 6 == 0:
            pass
        else:
            raise Exception('Invalid swarm_archive.txt!')
        number_of_chromosome = length_buf / 6
        if number_of_chromosome == 0:
            return None
        swarm_archive_raw = [buf[i:i+6] for i in range(0, len(buf), 6)]
        swarm_archive_xf, swarm_proj_name, swarm_design_param, swarm_performance = extract_from_swarm_v3(swarm_archive_raw)
        return swarm_archive_xf, swarm_proj_name, swarm_design_param, swarm_performance
    
    
def extract_from_swarm_v3(swarm_archive_raw):

    swarm_archive_xf = []
    swarm_proj_name = []
    swarm_performance = []
    swarm_design_param = []
    for raw in swarm_archive_raw:
        xf_extract = [float(xf) for xf in raw[3].split(',')]
        design_param_extract = ast.literal_eval(raw[4])
        perform_extract = ast.literal_eval(raw[5])  
        # we can remove this in final, this was added as initial population had alpha_St greater than the bounds set
        if xf_extract[2] < 49:
            swarm_archive_xf.append(xf_extract)
            swarm_design_param.append(design_param_extract)
            swarm_performance.append(perform_extract)
            name_line = raw[2].split(',')
            swarm_proj_name.append(name_line[0])
    return swarm_archive_xf, swarm_proj_name, swarm_design_param, swarm_performance

  
def get_x_denorm_from_design_parameters(design_parameters):

    # # step 1: get free_variables from design_parameters
    # free_variables = [None]*10
    # free_variables[0]  = design_parameters[0] # spmsm_template.deg_alpha_st 
    # free_variables[1]  = design_parameters[3] # spmsm_template.mm_d_so         
    # free_variables[2]  = design_parameters[5] # spmsm_template.mm_d_st
    # free_variables[3]  = design_parameters[6] # spmsm_template.mm_d_sy 
    # free_variables[4]  = design_parameters[7] # spmsm_template.mm_w_st         
    # # free_variables[5]  = design_parameters[12] # spmsm_template.sleeve_length   
    # free_variables[5]  = design_parameters[14] # spmsm_template.mm_d_pm           
    # free_variables[6]  = design_parameters[17] # spmsm_template.mm_d_ri         
    # free_variables[7] =  design_parameters[13] # Airgap  
    # free_variables[8]  = design_parameters[15] # alpha_rm       
    # free_variables[9] = design_parameters[19] # d_rp 

    x = [None]*11
    x[0] = (design_parameters[13]+2)*1e-3
    x[1] = 11.94*1e-3
    x[2] = design_parameters[0]
    x[3] = design_parameters[3]*1e-3
    x[4] = design_parameters[7]*1e-3
    x[5] = design_parameters[5]*1e-3
    x[6] = design_parameters[6]*1e-3
    x[7] = design_parameters[15]
    x[8] = design_parameters[14]*1e-3
    x[9] = design_parameters[19]*1e-3
    x[10] = design_parameters[17]*1e-3

    return x
  

def get_pareto_fronts(swarm_xf, swarm_name=None, swarm_performance=None, run_folder=None, show_plot=False):

    number_of_chromosome = len(swarm_xf)
    print('Archive size:', number_of_chromosome)
    fits = [xf[-3:] for xf in swarm_xf]
    vectors = [xf[:-3] for xf in swarm_xf]
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits)
    fronts_index = ndf[0]
    fits_at_front = [fits[point] for point in fronts_index]
    vectors_at_front = [vectors[point] for point in fronts_index]
    if swarm_name != None and swarm_performance != None:
        projname_at_front = [swarm_name[point] for point in fronts_index]
        peformance_front = [swarm_performance[point] for point in fronts_index]

    if show_plot == True:
        my_2p5d_plot_non_dominated_fronts(fits, run_folder, comp=[2,1], marker='o', up_to_rank_no=1)
        perf_to_plot = []
        for p in peformance_front:
            perf = [p['Ea'],p['FRW'],p['TRV']/1000]
            perf_to_plot.append(perf)
        my_2p5d_plot_perf_fronts(perf_to_plot, run_folder, comp=[2,1], marker='o', up_to_rank_no=1)

    return vectors_at_front, fits_at_front, projname_at_front, peformance_front

def my_2p5d_plot_non_dominated_fronts(points, run_folder, marker='^', comp=[0, 1], up_to_rank_no=1, no_text=True, ax=None, fig=None, no_colorbar=False, z_filter=None, label=None):
    # [from jiahao]this is adapted from pygmo package but there is a bug therein so I write my own function (I also initiated an issue at their Github page and they acknowledge the issue).

    plt.rcParams['mathtext.fontset'] = 'stix' # 'cm'
    plt.rcParams["font.family"] = "Times New Roman"
    
    font = {'family' : 'Times New Roman', #'serif',
            'color' : 'black',
            'weight' : 'normal',
            'size' : 14,}

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    full_comp = [0, 1, 2]
    full_comp.remove(comp[0])
    full_comp.remove(comp[1])
    z_comp = full_comp[0]

    fronts, _, _, _= pg.fast_non_dominated_sorting(points)

    # We define the colors of the fronts (grayscale from black to white)
    cl = list(zip(np.linspace(0.9, 0.1, len(fronts)),
                  np.linspace(0.9, 0.1, len(fronts)),
                  np.linspace(0.9, 0.1, len(fronts))))

    if ax is None:
        fig, ax = plt.subplots(figsize=(3.8, 4),constrained_layout=False)
        plt.subplots_adjust(left=None, bottom=None, right=0.85, top=None, wspace=None, hspace=None)

    count = 0
    for ndr, front in enumerate(fronts):
        count += 1
        
        # Frist compute the points coordinates
        x_scale = 1
        y_scale = 1
        z_scale = 1
        x = [points[idx][comp[0]] for idx in front]
        y = [points[idx][comp[1]] for idx in front]
        z = [points[idx][z_comp]  for idx in front]
        
        # Then sort them by the first objective
        tmp = [(a, b, c) for a, b, c in zip(x, y, z)]
        tmp = sorted(tmp, key=lambda k: k[0])
        
        # Now plot using step
        ax.step([coords[0] for coords in tmp], 
                [coords[1] for coords in tmp], color=cl[ndr], where='post')

        # Now add color according to the value of the z-axis variable usign scatter
        if z_filter is not None:
            z = np.array(z)
            x = np.array(x)[z<z_filter]
            y = np.array(y)[z<z_filter]
            z = z[z<z_filter]
            print('Cost, -Efficency, Ripple Sum')
            for a,b,c in zip(x,y,z):
                print(a,b,c)
            scatter_handle = ax.scatter(x, y, c=z, s=40,  edgecolor=None, alpha=0.5, cmap='viridis', marker=marker, zorder=99, vmin=0, vmax=20, label=label,markersize=20) #'viridis'    Spectral
        else:
            scatter_handle = ax.scatter(x, y, c=z, s=40, edgecolor=None, alpha=0.5, cmap='viridis', marker=marker, zorder=99) #'viridis'

        # ax.set_ylim(-94.2,-92)
        ax.set_xlim(0,8)

        if up_to_rank_no is None:
            pass
        else:
            if count >= up_to_rank_no:
                break
    ax.xaxis.set_major_locator(mtick.MaxNLocator(6))
    axins = inset_axes(ax,
                       width="3%",  # width = 5% of parent_bbox width
                       height="100%",  # height : 50%
                       loc='lower left',
                       bbox_to_anchor=(1, 0., 1, 1),
                       bbox_transform=ax.transAxes,
                       borderpad=0,
                       )
               
    clb = fig.colorbar(scatter_handle, cax=axins)
    
    if z_comp == 0:
        z_label = r'$\rm {Cost}$ [USD]'
        z_text  = '%.1f'
    elif z_comp == 1:
        z_label = r'$-\eta$ [%]'
        z_text  = '%.1f'
    elif z_comp == 2:
        z_label = r'$Weighted Ripple$'
        z_text  = '%.1f'
    if not no_colorbar:
        clb.ax.set_ylabel(z_label, rotation=0, labelpad=20, **font)
        clb.ax.yaxis.set_label_coords(-1,1.085)
        clb.ax.yaxis.set_major_locator(mtick.MaxNLocator(6))
    
    if z_comp == 2: # when OC as z-axis
        print('-----------------------------------------------------')
        print('-----------------------------------------------------')
        print('-----------------------------------------------------')
        # Add index next to the points
        for x_coord, y_coord, z_coord, idx in zip(x, y, z, front):
            if no_text:
                pass
            else:
                ax.annotate( z_text%(z_coord) + ' #%d'%(idx), (x_coord, y_coord) )
    else:
        # text next scatter showing the value of the 3rd objective
        for i, val in enumerate(z):
            if no_text:
                pass
            else:
                ax.annotate( z_text%(val), (x[i], y[i]) )      
    
        # refine the plotting
    if comp[0] == 0:
        ax.set_xlabel(r'$\rm {Cost}$ [USD]', **font)
    elif comp[0] == 1:
        ax.set_xlabel(r'$-\eta$ [%]', **font)
    elif comp[0] == 2:
        ax.set_xlabel(r'Weighted Ripple', **font)

    if comp[1] == 0:
        ax.set_ylabel(r'$\rm {Cost}$ [USD]', **font,rotation=0)
    elif comp[1] == 1:
        ax.set_ylabel(r'$-\eta$ [%]', **font,rotation=0)
    elif comp[1] == 2:
        ax.set_ylabel(r'Weighted Ripple', **font,rotation=0)
    
    ax.yaxis.set_label_coords(-0.1,1.055)
    plt.yticks(rotation=90)
    ax.yaxis.set_major_locator(mtick.MaxNLocator(6))
    
    ax.grid()
    ax.tick_params(axis='both', which='major', labelsize=14)
    clb.ax.tick_params(which='major', labelsize=14, rotation=0)
    # clb.ax.set_yticklabels(clb.ax.get_yticklabels(), rotation='vertical')
    # fig.set_size_inches(8, 4)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig(run_folder + 'paretoPlot.eps', bbox_inches='tight', format='eps')
    fig.savefig(run_folder + 'paretoPlot.png', bbox_inches='tight', dpi=300)
  
    return 

def my_2p5d_plot_perf_fronts(points, run_folder, marker='^', comp=[0, 1], up_to_rank_no=1, no_text=True, ax=None, fig=None, no_colorbar=False, z_filter=None, label=None):
    # [from jiahao]this is adapted from pygmo package but there is a bug therein so I write my own function (I also initiated an issue at their Github page and they acknowledge the issue).

    plt.rcParams['mathtext.fontset'] = 'stix' # 'cm'
    plt.rcParams["font.family"] = "Times New Roman"
    
    font = {'family' : 'Times New Roman', #'serif',
            'color' : 'black',
            'weight' : 'normal',
            'size' : 14,}

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    full_comp = [0, 1, 2]
    full_comp.remove(comp[0])
    full_comp.remove(comp[1])
    z_comp = full_comp[0]

    # We define the colors of the fronts (grayscale from black to white)
    cl = zip(np.linspace(0.9, 0.1, len(points)))

    if ax is None:
        fig, ax = plt.subplots(figsize=(3.8, 4),constrained_layout=False)
        plt.subplots_adjust(left=None, bottom=None, right=0.85, top=None, wspace=None, hspace=None)

    # Frist compute the points coordinates
    x_scale = 1
    y_scale = 1
    z_scale = 1
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    z = [p[2]  for p in points]

    # Then sort them by the first objective
    tmp = [(a, b, c) for a, b, c in zip(x, y, z)]
    tmp = sorted(tmp, key=lambda k: k[0])
    
    # Now plot using step
    # ax.step([coords[0] for coords in tmp], 
    #         [coords[1] for coords in tmp], color=cl, where='post')

    # Now add color according to the value of the z-axis variable usign scatter
    if z_filter is not None:
        z = np.array(z)
        x = np.array(x)[z<z_filter]
        y = np.array(y)[z<z_filter]
        z = z[z<z_filter]
        scatter_handle = ax.scatter(x, y, c=z, s=40,  edgecolor=None, alpha=0.5, cmap='viridis', marker=marker, zorder=99, vmin=0, vmax=20, label=label) #'viridis'    Spectral
    else:
        scatter_handle = ax.scatter(x, y, c=z, s=40,  edgecolor=None, alpha=0.5, cmap='viridis', marker=marker, zorder=99) #'viridis'

    # ax.set_ylim(-94.2,-92)
    ax.set_xlim(0,6)
        
    ax.xaxis.set_major_locator(mtick.MaxNLocator(6))
    axins = inset_axes(ax,
                       width="3%",  # width = 5% of parent_bbox width
                       height="100%",  # height : 50%
                       loc='lower left',
                       bbox_to_anchor=(1, 0., 1, 1),
                       bbox_transform=ax.transAxes,
                       borderpad=0,
                       )
               
    clb = fig.colorbar(scatter_handle, cax=axins)
      
    z_label = r'TRV [kNm/m$^3$]'
    z_text  = '%.1f'
    if not no_colorbar:
        clb.ax.set_ylabel(z_label, rotation=0, labelpad=20, **font)
        clb.ax.yaxis.set_label_coords(-3,1.1)
        clb.ax.yaxis.set_major_locator(mtick.MaxNLocator(6))
    
    if z_comp == 2: # when OC as z-axis
        print('-----------------------------------------------------')
        print('-----------------------------------------------------')
        print('-----------------------------------------------------')
        # Add index next to the points
        for x_coord, y_coord, z_coord, idx in zip(x, y, z, points):
            if no_text:
                pass
            else:
                ax.annotate( z_text%(z_coord) + ' #%d'%(idx), (x_coord, y_coord) )
    else:
        # text next scatter showing the value of the 3rd objective
        for i, val in enumerate(z):
            if no_text:
                pass
            else:
                ax.annotate( z_text%(val), (x[i], y[i]) )
    
    # refine the plotting
    ax.set_xlabel(r'$E_a [deg]$', **font)
    ax.set_ylabel(r'FRW [p.u]', **font, rotation=0)
    ax.yaxis.set_label_coords(0,1.05)
    plt.yticks(rotation=90)
    ax.yaxis.set_major_locator(mtick.MaxNLocator(6))
    ax.grid()
    ax.tick_params(axis='both', which='major', labelsize=14)
    clb.ax.tick_params(which='major', labelsize=14, rotation=0)
    # fig.set_size_inches(8, 4)
    plt.gcf().subplots_adjust(bottom=0.15)
    # plt.gcf().subplots_adjust(right=0.15)
    plt.savefig(run_folder + 'paretoPerf.eps', bbox_inches='tight',format='eps')
    fig.savefig(run_folder + 'paretoPerf.png', bbox_inches='tight',dpi=300)
    
    return 

def plot_x_with_bounds(free_var, bounds, fea_config_dict, alpha=0.5, zorder=1):
        fig, axeses = plt.subplots(3, 4, sharex=True, dpi=300, figsize=(8, 4), facecolor='w', edgecolor='k')
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.35, hspace=None)
        plt.rcParams['mathtext.fontset'] = 'stix' # 'cm'
        plt.rcParams['font.family'] = ['Times New Roman']
        font = {'family' : 'Times New Roman', #'serif',
                'color' : 'darkblue',
                'weight' : 'normal',
                'size' : 8,}
        
        var_label = [
                     '$\delta_e$ [m]', 
                     '$r_{ro}$ [m]', 
                     r'$\alpha_{st} [deg]$', 
                     '$d_{so}$ [m]',
                     '$w_{st}$ [m]',
                     '$d_{st}$ [m]',
                     '$d_{sy}$ [m]',
                     r'$\alpha_m$ [deg]',
                     '$d_m$ [m]',
                     '$d_{mp}$ [m]',
                     '$d_{ri}$ [m]',
                     '$v_{tip}$ [m/s]'
                    ]
        
        var_list = []
        for var in free_var:
            tip_speed = var[1]*fea_config_dict['mech_omega']
            var.append(tip_speed)
            var_list.append(var)
        
        print(bounds[0][1])
        print(bounds[1][1])
        bounds[0].append(bounds[0][1]*fea_config_dict['mech_omega']) 
        bounds[1].append(bounds[1][1]*fea_config_dict['mech_omega'])            

        ax_list = []
        for i in range(3):
            ax_list.extend(axeses[i].tolist())
            
        for i,y_label in enumerate(var_label):
            ax = ax_list[i]; 
            x_i = [x[i] for x in var_list]  # in [m]
            len_x = len(x_i)
            design_number = list(range(len_x))
            ax.scatter(design_number, x_i, alpha=alpha, s = 10)
            ax.plot(np.ones(len_x) * bounds[0][i], 'm-')
            ax.plot(np.ones(len_x) * bounds[1][i], 'm-')
            ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
            ax.tick_params(axis ='y', which ='both', length = 0)
            ax.axes.get_xaxis().set_visible(False)
            ax.tick_params(axis='both', which='major', labelsize=8)
            tx = ax.yaxis.get_offset_text()
            tx.set_fontsize(8)
            ax.set_ylabel(y_label, **font)
            ax.yaxis.set_major_locator(mtick.MaxNLocator(3))
            ax.set_xlim([0,len_x])

        plt.savefig(fea_config_dict['run_folder'] + 'freeVar.eps', format='eps')    
        fig.savefig(fea_config_dict['run_folder'] + 'freeVar.png', dpi=300)
        
        return

# https://dsp.stackexchange.com/questions/11513/estimate-frequency-and-peak-value-of-a-signals-fundamental
#define N_SAMPLE ((long int)(1.0/(0.1*TS))) // Resolution 0.1 Hz = 1 / (N_SAMPLE * TS)
class Goertzel_Data_Struct(object):
    """docstring for Goertzel_Data_Struct"""
    def __init__(self, id=None, ):
        self.id = id    
        self.bool_initialized = False
        self.sine = None
        self.cosine = None
        self.coeff = None
        self.scalingFactor = None
        self.q = None
        self.q2 = None
        self.count = None
        self.k = None #// k is the normalized target frequency 
        self.real = None
        self.imag = None
        self.accumSquaredData = None
        self.ampl = None
        self.phase = None


    # /************************************************
    #  * Real time implementation to avoid the array of input double *data[]
    #  * with Goertzel Struct to store the variables and the output values
    #  *************************************************/
    def goertzel_realtime(gs, targetFreq, numSamples, samplingRate, data):
        # gs is equivalent to self
        try:
            len(data)
        except:
            pass
        else:
            raise Exception('This is for real time implementation of Goertzel, hence data must be a scalar rather than array-like object.')

        if gs.bool_initialized == False:
            gs.bool_initialized = True

            gs.count = 0
            gs.k = (0.5 + ((numSamples * targetFreq) / samplingRate))
            omega = (2.0 * math.pi * gs.k) / numSamples
            gs.sine = sin(omega)
            gs.cosine = cos(omega)
            gs.coeff = 2.0 * gs.cosine
            gs.q1=0
            gs.q2=0
            gs.scalingFactor = 0.5 * numSamples
            gs.accumSquaredData = 0.0

        q0 = gs.coeff * gs.q1 - gs.q2 + data
        gs.q2 = gs.q1
        gs.q1 = q0 # // q1 is the newest output vk[N], while q2 is the last output vk[N-1].

        gs.accumSquaredData += data*data

        gs.count += 1
        if gs.count>=numSamples:
            # // calculate the real and imaginary results with scaling appropriately
            gs.real = (gs.q1 * gs.cosine - gs.q2) / gs.scalingFactor #// inspired by the python script of sebpiq
            gs.imag = (gs.q1 * gs.sine) / gs.scalingFactor

            # // reset
            gs.bool_initialized = False
            return True
        else:
            return False

    def goertzel_offline(gs, targetFreq, samplingRate, data_list):
        # gs is equivalent to self

        numSamples = len(data_list)

        if gs.bool_initialized == False:
            gs.bool_initialized = True

            gs.count = 0
            gs.k = (0.5 + ((numSamples * targetFreq) / samplingRate))
            omega = (2.0 * math.pi * gs.k) / numSamples
            gs.sine = math.sin(omega)
            gs.cosine = math.cos(omega)
            gs.coeff = 2.0 * gs.cosine
            gs.q1=0
            gs.q2=0
            gs.scalingFactor = 0.5 * numSamples
            gs.accumSquaredData = 0.0

        for data in data_list:
            q0 = gs.coeff * gs.q1 - gs.q2 + data
            gs.q2 = gs.q1
            gs.q1 = q0 # // q1 is the newest output vk[N], while q2 is the last output vk[N-1].

            gs.accumSquaredData += data*data

            gs.count += 1
            if gs.count>=numSamples:

                # // calculate the real and imaginary results with scaling appropriately
                gs.real = (gs.q1 * gs.cosine - gs.q2) / gs.scalingFactor #// inspired by the python script of sebpiq
                gs.imag = (gs.q1 * gs.sine) / gs.scalingFactor

                # // reset
                gs.bool_initialized = False
                return True
        print(data_list)
        print(gs.count)
        print(numSamples)
        return None

def compute_power_factor_from_half_period(voltage, current, mytime, targetFreq=1e3, numPeriodicalExtension=1000): # 目标频率默认是1000Hz

    gs_u = Goertzel_Data_Struct("Goertzel Struct for Voltage\n")
    gs_i = Goertzel_Data_Struct("Goertzel Struct for Current\n")

    TS = mytime[-1] - mytime[-2]

    if type(voltage)!=type([]):
        voltage = voltage.tolist() + (-voltage).tolist()
        current = current.tolist() + (-current).tolist()
    else:
        voltage = voltage + [-el for el in voltage]
        current = current + [-el for el in current]

    voltage *= numPeriodicalExtension
    current *= numPeriodicalExtension

    N_SAMPLE = len(voltage)
    gs_u.goertzel_offline(targetFreq, 1./TS, voltage)
    gs_i.goertzel_offline(targetFreq, 1./TS, current)

    gs_u.ampl = math.sqrt(gs_u.real*gs_u.real + gs_u.imag*gs_u.imag) 
    gs_u.phase = math.atan2(gs_u.imag, gs_u.real)

    gs_i.ampl = math.sqrt(gs_i.real*gs_i.real + gs_i.imag*gs_i.imag) 
    gs_i.phase = math.atan2(gs_i.imag, gs_i.real)

    print('gs_u.ampl', gs_u.ampl)
    print('gs_i.ampl', gs_i.ampl)

    phase_difference_in_deg = ((gs_i.phase-gs_u.phase)/math.pi*180)
    power_factor = math.cos(gs_i.phase-gs_u.phase)
    return power_factor
    
def max_indices_2(arr, k):
    '''
    Returns the indices of the k first largest elements of arr
    (in descending order in values)
    '''
    assert k <= arr.size, 'k should be smaller or equal to the array size'
    arr_ = arr.astype(float)  # make a copy of arr
    max_idxs = []
    for _ in range(k):
        max_element = np.max(arr_)
        if np.isinf(max_element):
            break
        else:
            idx = np.where(arr_ == max_element)
        max_idxs.append(idx)
        arr_[idx] = -np.inf
    return max_idxs

def min_indices(arr, k):
    if type(arr) == type([]):
        arr = np.array(arr)
    indices = np.argsort(arr)[:k]
    items   = arr[indices] # arr and indices must be np.array
    return indices, items

def max_indices(arr, k):
    if type(arr) == type([]):
        arr = np.array(arr)
    arr_copy = arr[::]
    indices = np.argsort(-arr)[:k]
    items   = arr_copy[indices]
    return indices, items

def autolabel(ax, rects, xpos='center', bias=0.0, textfont=None):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height+bias,
                '%.2f'%(height), ha=ha[xpos], va='bottom', rotation=90, **textfont)   

def use_weights(which='O1'):
    if which == 'O1':
        return [ 1, 0.1,   1, 0.1, 0.1,   0 ]
    if which == 'O2':
        return [ 1,1,1,1,1,  0 ]
    if which == 'O3':
        return [ 1,0,1,0,0,  1 ]
    if which == 'O1R':
        return [ 1, 0.2,   1, 0.1, 0.1,   0 ]
    if which == 'O4':
        return [ 2,2,1,1,1,  0 ]
    return None

def compute_list_cost(weights, rotor_volume, rotor_weight, torque_average, normalized_torque_ripple, ss_avg_force_magnitude, normalized_force_error_magnitude, force_error_angle, jmag_loss_list, femm_loss_list, power_factor, total_loss):
    # O2
    # weights = [ 1, 1.0,   1, 1.0, 1.0,   0 ]
    # O1
    # weights = [ 1, 0.1,   1, 0.1, 0.1,   0 ]
    list_cost = [   30e3 / ( torque_average/rotor_volume ),
                    normalized_torque_ripple         *  20, 
                    1.0 / ( ss_avg_force_magnitude/rotor_weight ),
                    normalized_force_error_magnitude *  20, 
                    force_error_angle                * 0.2, # [deg] 
                    total_loss                       / 2500. ] 
    cost_function = np.dot(np.array(list_cost), np.array(weights))
    return cost_function, list_cost

    # The weight is [TpRV=30e3, FpRW=1, Trip=50%, FEmag=50%, FEang=50deg, eta=sqrt(10)=3.16]
    # which means the FEang must be up to 50deg so so be the same level as TpRV=30e3 or FpRW=1 or eta=316%
    # list_weighted_cost = [  30e3 / ( torque_average/rotor_volume ),
    #                         1.0 / ( ss_avg_force_magnitude/rotor_weight ),
    #                         normalized_torque_ripple         *   2, #       / 0.05 * 0.1
    #                         normalized_force_error_magnitude *   2, #       / 0.05 * 0.1
    #                         force_error_angle * 0.2          * 0.1, # [deg] /5 deg * 0.1 is reported to be the base line (Yegu Kang) # force_error_angle is not consistent with Yegu Kang 2018-060-case of TFE
    #                         2*total_loss/2500., #10 / efficiency**2,
    #                         im_variant.thermal_penalty ] # thermal penalty is evaluated when drawing the model according to the parameters' constraints (if the rotor current and rotor slot size requirement does not suffice)
    # cost_function = sum(list_weighted_cost)


def fobj_scalar(torque_average, ss_avg_force_magnitude, normalized_torque_ripple, normalized_force_error_magnitude, force_error_angle, total_loss, 
                weights=None, rotor_volume=None, rotor_weight=None):

    list_cost = [   30e3 / ( torque_average/rotor_volume ),
                    normalized_torque_ripple         *  20, #       / 0.05 * 0.1
                    1.0 / ( ss_avg_force_magnitude/rotor_weight ),
                    normalized_force_error_magnitude *  20, #       / 0.05 * 0.1
                    force_error_angle                * 0.2, # [deg] /5 deg * 0.1 is reported to be the base line (Yegu Kang) # force_error_angle is not consistent with Yegu Kang 2018-060-case of TFE
                    total_loss                       / 2500. ] #10 / efficiency**2,
    cost_function = np.dot(np.array(list_cost), np.array(weights))
    return cost_function

def fobj_list(l_torque_average, l_ss_avg_force_magnitude, l_normalized_torque_ripple, l_normalized_force_error_magnitude, l_force_error_angle, l_total_loss,
                weights=None, rotor_volume=None, rotor_weight=None):

    l_cost_function = []
    for torque_average, ss_avg_force_magnitude, normalized_torque_ripple, normalized_force_error_magnitude, force_error_angle, total_loss in zip(l_torque_average, l_ss_avg_force_magnitude, l_normalized_torque_ripple, l_normalized_force_error_magnitude, l_force_error_angle, l_total_loss):
        list_cost = [   30e3 / ( torque_average/rotor_volume ),
                        normalized_torque_ripple         *  20,
                        1.0 / ( ss_avg_force_magnitude/rotor_weight ),
                        normalized_force_error_magnitude *  20,
                        force_error_angle                * 0.2,
                        total_loss                       / 2500. ]
        cost_function = np.dot(np.array(list_cost), np.array(weights))
        l_cost_function.append(cost_function)
    return np.array(l_cost_function)


class ExceptionReTry(Exception):
    """Exception for requiring a second attemp."""
    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload # you could add more args
    def __str__(self):
        return str(self.message)    




