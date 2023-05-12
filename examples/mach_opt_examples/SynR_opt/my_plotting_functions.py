import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pygmo as pg
import numpy as np

class DataAnalyzer:
    def __init__(self, save_path):
        self.save_path = save_path
        
    def plot_pareto_front(self, points, marker='o', xy=[0, 1], no_text=True, up_to_rank_no=1, ax=None, fig=None, no_colorbar=False, z_filter=None, label=None):
        plt.rcParams['mathtext.fontset'] = 'stix' # 'cm'
        plt.rcParams["font.family"] = "Times New Roman"
        
        font = {'family' : 'Times New Roman', #'serif',
                'color' : 'black',
                'weight' : 'normal',
                'size' : 14,}
    
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    
        full_comp = [0, 1, 2]
        full_comp.remove(xy[0])
        full_comp.remove(xy[1])
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
            
            # First compute the points coordinates
            x_scale = 1
            y_scale = 1
            z_scale = 1
            x = [points[idx][xy[0]] for idx in front]
            y = [points[idx][xy[1]] for idx in front]
            z = [points[idx][z_comp]  for idx in front]
            
            # Then sort them by the first objective
            tmp = [(a, b, c) for a, b, c in zip(x, y, z)]
            tmp = sorted(tmp, key=lambda k: k[0])
            
            # Now plot using step
            ax.step([coords[0] for coords in tmp], 
                    [coords[1] for coords in tmp], color=cl[ndr], where='post')
    
            # Now add color according to the value of the z-axis variable using scatter
            if z_filter is not None:
                z = np.array(z)
                x = np.array(x)[z<z_filter]
                y = np.array(y)[z<z_filter]
                z = z[z<z_filter]
                print('-Power Density, -Efficency, Torque Ripple')
                for a,b,c in zip(x,y,z):
                    print(a,b,c)
                scatter_handle = ax.scatter(x, y, c=z, s=40,  edgecolor=None, alpha=0.5, cmap='viridis', marker=marker, zorder=99, vmin=0, vmax=20, label=label,markersize=20) #'viridis'    Spectral
            else:
                scatter_handle = ax.scatter(x, y, c=z, s=40, edgecolor=None, alpha=0.5, cmap='viridis', marker=marker, zorder=99) #'viridis'
            
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
        z_text  = '%.1f'

        if not no_colorbar:
            clb.ax.set_ylabel(label[z_comp], rotation=0, labelpad=20, **font)
            clb.ax.yaxis.set_label_coords(-1,1.085)
            clb.ax.yaxis.set_major_locator(mtick.MaxNLocator(6))
          
        
        # refine the plotting
        ax.set_xlabel(label[xy[0]], **font)        
        ax.set_ylabel(label[xy[1]], **font,rotation=0)
        
        ax.yaxis.set_label_coords(-0.1,1.055)
        plt.yticks(rotation=90)
        ax.yaxis.set_major_locator(mtick.MaxNLocator(6))
        
        ax.grid()
        ax.tick_params(axis='both', which='major', labelsize=14)
        clb.ax.tick_params(which='major', labelsize=14, rotation=0)
        # clb.ax.set_yticklabels(clb.ax.get_yticklabels(), rotation='vertical')
        # fig.set_size_inches(8, 4)
        plt.gcf().subplots_adjust(bottom=0.15)
        # plt.savefig(self.save_path + 'paretoPlot.eps', bbox_inches='tight', format='eps')
        fig.savefig(self.save_path + '/paretoPlot.svg', bbox_inches='tight', dpi=300)
        
      
    def plot_x_with_bounds(self, free_var, var_label, bounds, alpha=0.5):
        fig, axes = plt.subplots(3, 4, sharex=True, dpi=300, figsize=(8, 4), facecolor='w', edgecolor='k')
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.35, hspace=None)
        plt.rcParams['mathtext.fontset'] = 'stix' # 'cm'
        plt.rcParams['font.family'] = ['Times New Roman']
        font = {'family' : 'Times New Roman', #'serif',
                'color' : 'darkblue',
                'weight' : 'normal',
                'size' : 8,}
        var_list = []
        for var in free_var:
            var_list.append(var)

        ax_list = []
        for i in range(3):
            ax_list.extend(axes[i].tolist())
            
        for i,y_label in enumerate(var_label):
            ax = ax_list[i]; 
            x_i = [x[i] for x in var_list]  # in [m]
            len_x = len(x_i)
            design_number = list(range(len_x))
            ax.scatter(design_number, x_i, alpha=alpha, s = 10)
            ax.plot(np.ones(len_x) * bounds[i][0], 'm-')
            ax.plot(np.ones(len_x) * bounds[i][1], 'm-')
            ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
            ax.tick_params(axis ='y', which ='both', length = 0)
            ax.axes.get_xaxis().set_visible(False)
            ax.tick_params(axis='both', which='major', labelsize=8)
            tx = ax.yaxis.get_offset_text()
            tx.set_fontsize(8)
            ax.set_ylabel(y_label, **font)
            ax.yaxis.set_major_locator(mtick.MaxNLocator(3))
            ax.set_xlim([0,len_x])
            
        plt.savefig(self.save_path + '/freeVar.svg')    
        
        return