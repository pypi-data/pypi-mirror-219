import numpy as np
import os 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection
import matplotlib.ticker as mticker

from matplotlib_dhi import *
from matplotlib_dhi import subplots

import cmocean
def import_multiple_pd0(paths,labels):
    '''
    reads multiple Workhorse ADCP files from a list of filepaths


    Parameters
    ----------
    paths : list
        list containing paths to each .pd0 file
    labels : TYPE
        DESCRIPTION.

    Returns
    -------
    adcp_file : dict
        Dictionary with keys specified by labels.

    '''
    adcp_file = {}
    for p,path in enumerate(paths):
        label = labels[p]
        #path = row['Relative Data Location'].strip('\n').strip() # path to the ADCP data, strip formatting characters and spaces
        
        try:
            adcp_file[label] = WorkhorseADCP.WorkhorseADCP(path)
        except: 
            print(f'Cound not read {path}')        
    return adcp_file
#%%

def metadata_table(adcp_file,**kwargs):
## Add a table with metadata 

    fig,ax = subplots(for_production = True, figheight = 5, figwidth = 5)
    
    row_labels = ['File',
                  'Instrument S/N',
                  'Beam Facing',
                  'Instrument Depth (m)',
                  'Instrument HAB (m)',
                  'Frequency',
                  '# Bins',
                  'First Date',
                  'Last Date',
                  'Elapsed Time (hr)',
                  'First Good Bin',
                  'Last Good Bin',]
    
    try:
        beam_dir = adcp_file.beam_facing
        sysfreq  = adcp_file.ensemble_data[0]['SYSTEM CONFIGURATION']['FREQUENCY']
    except:
        beam_dir = 'unknown'
        sysfreq  = 'unknown'
    
    cell_text = [adcp_file.filepath.split(os.sep)[-1],
                 str(adcp_file.ensemble_data[0]['FIXED LEADER']['INSTRUMENT SERIAL NUMBER']),
                 str(beam_dir),
                 str(adcp_file.instrument_depth),
                 str(adcp_file.instrument_HAB),
                 str(sysfreq),
                 str(adcp_file.n_bins),
                 adcp_file.ensemble_times[0].strftime('%d-%b-%y %H:%M:%S'),
                 adcp_file.ensemble_times[-1].strftime('%d-%b-%y %H:%M:%S'),
                 str(round((adcp_file.ensemble_times[-1]- adcp_file.ensemble_times[0]).total_seconds()/60/60,2)),
                 'nan',
                 'nan',]
    
    


    def left_justify_list(x):
        # left jsutify a list of strings so that they all have the same length
        x = cell_text 
        max_len = max([len(i) for i in x])
        
        for i in range(len(x)):
            x[i] = x[i].ljust(max_len)
        return x
        
    
    cell_text = [[i] for i in left_justify_list(cell_text)]    
    # pad each string on the right to have length 
    
    
    table = ax.table(cellText = cell_text,
                        rowLabels = row_labels,
                        rowLoc = 'left',
                        cellLoc = 'left',
                        bbox = [0.6,00,.4,1],alpha = 0.4)
    
    table.set_fontsize(9)
            
    ax.axis('off')
    ax.grid(False)
    ax.set_title("File Metadata",pad = 15)
    
    return fig,ax
#%%

def error_velocity_plot(adcp_file,**kwargs):#plot_by = 'bin',start_bin = None,end_bin = None,start_ensemble = None,end_ensemble = None,title = None):
    """
    Generate a fencegate plot of error velocity

    Parameters
    ----------
    adcp_file : object
        WorkhorseADCP object.
    plot_by : str
        y-axes plot method ('bin','depth').
    start_bin : int
        First bin to plot. (use zero based index)
    end_bin : int
        Last bin to plot.(use zero based index)
    start_ensemble : int
        First ensemble to plot.(use zero based index)
    end_ensemble : int
        Last ensemble to plot.(use zero based index)
    title : str
        plot axes title.

    Returns
    -------
    fig,ax
        matplotlib figure and axes objects

    """


    if kwargs.get('plot_by'):plot_by = kwargs.get('plot_by')
    else: plot_by = 'bin'
    
    if kwargs.get('start_bin'): start_bin = kwargs.get('start_bin')
    else: start_bin = 0
    
    if kwargs.get('end_bin'): end_bin = kwargs.get('end_bin')
    else: end_bin = adcp_file.n_bins
    

    if kwargs.get('start_ensemble'): start_ensemble = kwargs.get('start_ensemble')
    else: start_ensemble = 0
    
    if kwargs.get('end_ensemble'): end_ensemble = kwargs.get('end_ensemble')
    else: end_ensemble = adcp_file.n_ensembles   
    
    if kwargs.get('title'): title = kwargs.get('title')
    else: title = adcp_file.filepath.split(os.sep)[-1]
    
    
    nbins = (end_bin - start_bin)
    u,v,z,du,dv,dz,errv = adcp_file.get_velocity()
    errv = errv.T[start_bin:end_bin,start_ensemble:end_ensemble]
    #echo_intensity = adcp_file.get_ensemble_array(beam_number = 0, field_name = 'CORRELATION MAGNITUDE')[start_bin:end_bin,start_ensemble:end_ensemble]
    ensemble_times = adcp_file.get_ensemble_datetimes()[start_ensemble:end_ensemble]
    

    subplot_titles = []
    fig,ax = subplots( figheight = 2.5, figwidth = 10.5, width_ratios = [1])
    

    ## format the ADCP data axes (left)
    topax = ax.twiny()
    ax.set_title(title)
    
    
    # set plot params based on instrument configuration 

    
    
    # set plotting extents in vertical direction
    if plot_by == 'bin':
        ylims = [start_bin,end_bin]
        ax.set_ylabel('Bin')
    elif plot_by == 'depth':
        bin_depths = adcp_file.get_bin_midpoints_depth()
        ylims = [bin_depths[start_bin],bin_depths[end_bin]]
        ax.set_ylabel('Depth')
    elif plot_by == 'HAB':
        bin_heights = adcp_file.get_bin_midpoints_HAB()
        ylims = [bin_heights[start_bin],bin_heights[end_bin]]
        ax.set_ylabel('Height Above Bed')
    else: 
        print('Invalid plot_by parameter')
    
    
    # set plotting extents in horizontal direction
    xlims = mdates.date2num(ensemble_times) # list of elegible xlimits 
    if adcp_file.beam_facing == 'UP':
        extent = [xlims[0],xlims[-1],ylims[0],ylims[1]]
    else:
        errv = np.flipud(errv)
        extent = [xlims[0],xlims[-1],ylims[1],ylims[0]]
        
        
    cmap = plt.cm.magma
    im = ax.imshow(errv, origin = 'lower', extent = extent, cmap = cmap, aspect = 'auto',norm=mpl.colors.LogNorm())#vmin=-1, vmax=2))# vmin = 0, vmax = np.nanmax(errv))
    cbar = fig.colorbar(im, ax=ax,orientation="vertical",location = 'right',fraction=0.046)
    cbar.set_label('Error Velocity (m/s)', rotation=90,fontsize= 12)
    
    
    ax.xaxis.set_major_locator(mticker.FixedLocator(ax.get_xticks()))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M %d%b%y '))
    topax.set_xlim(start_ensemble,end_ensemble)
    ax.set_xlabel('Ensemble')
    ax.grid(alpha = 0.1)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = -10, ha = 'left')
    
    
    

    
    return fig,ax

#%%
def four_beam_flood_plot(adcp_file,**kwargs):#plot_by = 'bin',start_bin = None,end_bin = None,start_ensemble = None,end_ensemble = None,title = None):
    """
    Generate a flooded color plots of correlation magnitude

    Parameters
    ----------
    adcp_file : object
        WorkhorseADCP object.
    plot_by : str
        y-axes plot method ('bin','depth').
    start_bin : int
        First bin to plot. (use zero based index)
    end_bin : int
        Last bin to plot.(use zero based index)
    start_ensemble : int
        First ensemble to plot.(use zero based index)
    end_ensemble : int
        Last ensemble to plot.(use zero based index)
    title : str
        plot axes title.

    Returns
    -------
    fig,ax
        matplotlib figure and axes objects

    """
    
    # if adcp_file.ensemble_data[0]['COORDINATE SYSTEM'] != 'BEAM COORDINATES':
    #     print('Plot feature only implemented for BEAM coordinates')


    if kwargs.get('plot_by'):plot_by = kwargs.get('plot_by')
    else: plot_by = 'bin'
    
    if kwargs.get('start_bin'): start_bin = kwargs.get('start_bin')
    else: start_bin = 0
    
    if kwargs.get('end_bin'): end_bin = kwargs.get('end_bin')
    else: end_bin = adcp_file.n_bins
    

    if kwargs.get('start_ensemble'): start_ensemble = kwargs.get('start_ensemble')
    else: start_ensemble = 0
    
    if kwargs.get('end_ensemble'): end_ensemble = kwargs.get('end_ensemble')
    else: end_ensemble = adcp_file.n_ensembles   
    
    if kwargs.get('title'): title = kwargs.get('title')
    else: title = adcp_file.filepath.split(os.sep)[-1]
    
    
    nbins = (end_bin - start_bin)

    if kwargs.get('field'): field = kwargs.get('field')
    else: field = 'ECHO INTENSITY'
    

    x1 = adcp_file.get_ensemble_array(field_name = field, beam_number = 0)[start_bin:end_bin,start_ensemble:end_ensemble]
    x2 = adcp_file.get_ensemble_array(field_name = field, beam_number = 1)[start_bin:end_bin,start_ensemble:end_ensemble]
    x3 = adcp_file.get_ensemble_array(field_name = field, beam_number = 2)[start_bin:end_bin,start_ensemble:end_ensemble]
    x4 = adcp_file.get_ensemble_array(field_name = field, beam_number = 3)[start_bin:end_bin,start_ensemble:end_ensemble]
    
    
    #echo_intensity = adcp_file.get_ensemble_array(beam_number = 0, field_name = 'CORRELATION MAGNITUDE')[start_bin:end_bin,start_ensemble:end_ensemble]
    ensemble_times = adcp_file.get_ensemble_datetimes()[start_ensemble:end_ensemble]
    

    subplot_titles = []
    fig,ax = subplots(nrow = 4, ncol = 1, figheight = 8, figwidth = 10.5, width_ratios = [1])
    

    ## format the ADCP data axes (left)
    topax = ax[0].twiny()
    topax.set_xlim(start_ensemble,end_ensemble)
    ax[0].set_title(field)
    
    fig.suptitle(title, fontsize = 16)
    

    # set plot params based on instrument configuration 

    def set_axes_labels(axs,ylabel):
        # function to set the ylabel on a list of axes objects 
        for ax in axs:
            ax.set_ylabel(ylabel)
            
        return axs
            
    
    
    # set plotting extents in vertical direction
    if plot_by == 'bin':
        ylims = [start_bin,end_bin]
        set_axes_labels(ax,'Bin')
    elif plot_by == 'depth':
        bin_depths = adcp_file.get_bin_midpoints_depth()
        ylims = [bin_depths[start_bin],bin_depths[end_bin]]
        set_axes_labels(ax,'Depth')
    elif plot_by == 'HAB':
        bin_heights = adcp_file.get_bin_midpoints_HAB()
        ylims = [bin_heights[start_bin],bin_heights[end_bin]]
        set_axes_labels(ax,'Height Above Bed')

    else: 
        print('Invalid plot_by parameter')
        
        
        
    
    
    def get_plot_extent(X):
        """
        

        Parameters
        ----------
        X : numpy array
            Input array (ensemble data).

        Returns
        -------
        X : numpy array
            Possibly rotated input array (ensemble data) - to match the sensor orientation.
            
        extent : list
            bounding box for the plotted image.

        """
   
    
        # set plotting extents in horizontal direction
        xlims = mdates.date2num(ensemble_times) # list of elegible xlimits 
        if adcp_file.beam_facing == 'UP':
            extent = [xlims[0],xlims[-1],ylims[0],ylims[1]]
        else:
            X = np.flipud(X)
            extent = [xlims[0],xlims[-1],ylims[1],ylims[0]]
        return X,extent
        
    
    cmaps = {'PERCENT GOOD': plt.cm.bone,
             'ECHO INTENSITY': plt.cm.turbo,
             'CORRELATION MAGNITUDE': plt.cm.nipy_spectral,
             'ABSOLUTE BACKSCATTER':cmocean.cm.thermal,
             'SIGNAL TO NOISE RATIO':plt.cm.bone_r}
    cmap = cmaps[field]
    
    
    for x in [x1,x2,x3,x4]:
        x[x == 32768] = np.nan
    
    
    vmin = np.nanmin([x1,x2,x3,x4])
    vmax = np.nanmax([x1,x2,x3,x4])
    print(vmin)
    print(vmax)
    
    x1,extent = get_plot_extent(x1)
    im = ax[0].imshow(x1, origin = 'lower', extent = extent, cmap = cmap, aspect = 'auto')
    
    x2,extent = get_plot_extent(x2)
    im = ax[1].imshow(x2, origin = 'lower', extent = extent, cmap = cmap, aspect = 'auto')
    
    x3,extent = get_plot_extent(x3)
    im = ax[2].imshow(x3, origin = 'lower', extent = extent, cmap = cmap, aspect = 'auto')
    
    x4,extent = get_plot_extent(x4)
    im = ax[3].imshow(x4, origin = 'lower', extent = extent, cmap = cmap, aspect = 'auto')
    

    
    for i,axes in enumerate(ax):# modify subplot apperance 
        # set colorbar 
        cbar = fig.colorbar(im, ax=axes,orientation="vertical",location = 'right',fraction=0.046)
        cbar.set_label(f'Beam {i+1}', rotation=90,fontsize= 8)
        
        axes.xaxis.set_major_locator(mticker.FixedLocator(axes.get_xticks()))
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M %d%b%y '))
        axes.grid(alpha = 0.1)
        axes.set_xticklabels(axes.get_xticklabels(), rotation = 0, ha = 'center')
        
        #axes.text(.5,.5,f'PG{i+1}',transform = ax. transAxes)
        #axes.text(0.5, 0.5, 'matplotlib')#, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
        #path_effects=[mpl_path_effects.Stroke(linewidth=.25, foreground="black",alpha = .75)] 
        #axes.text(.025,.8,f'Percent Good {i}',transform = axes.transAxes, fontsize = 8, color = 'white',path_effects = path_effects)
    ax[-1].set_xlabel('Ensemble')
    
    

    
    return fig,ax



#%%
def single_beam_flood_plot(adcp_file,**kwargs):#plot_by = 'bin',start_bin = None,end_bin = None,start_ensemble = None,end_ensemble = None,title = None):
    """
    Generate a fencegate plot of ensemble data

    Parameters
    ----------
    adcp_file : object
        WorkhorseADCP object.
    plot_by : str
        y-axes plot method ('bin','depth').
    start_bin : int
        First bin to plot. (use zero based index)
    end_bin : int
        Last bin to plot.(use zero based index)
    start_ensemble : int
        First ensemble to plot.(use zero based index)
    end_ensemble : int
        Last ensemble to plot.(use zero based index)
    title : str
        plot axes title.

    Returns
    -------
    fig,ax
        matplotlib figure and axes objects

    """


    if kwargs.get('plot_by'):plot_by = kwargs.get('plot_by')
    else: plot_by = 'bin'
    
    if kwargs.get('start_bin'): start_bin = kwargs.get('start_bin')
    else: start_bin = 0
    
    if kwargs.get('end_bin'): end_bin = kwargs.get('end_bin')
    else: end_bin = adcp_file.n_bins

    if kwargs.get('start_ensemble'): start_ensemble = kwargs.get('start_ensemble')
    else: start_ensemble = 0
    
    if kwargs.get('end_ensemble'): end_ensemble = kwargs.get('end_ensemble')
    else: end_ensemble = adcp_file.n_ensembles   
    
    if kwargs.get('title'): title = kwargs.get('title')
    else: title = adcp_file.filepath.split(os.sep)[-1]
    
    if kwargs.get('field'): field = kwargs.get('field')
    else: field = 'ECHO INTENSITY'
    
    if kwargs.get('beam'): beam = kwargs.get('beam')
    else: beam = 0
    
    if beam == 'average': beam = 0 
    
    
    nbins = (end_bin - start_bin)
    x = adcp_file.get_ensemble_array(beam_number = 0, field_name = field)[start_bin:end_bin,start_ensemble:end_ensemble]
    #echo_intensity = adcp_file.get_ensemble_array(beam_number = 0, field_name = 'CORRELATION MAGNITUDE')[start_bin:end_bin,start_ensemble:end_ensemble]
    ensemble_times = adcp_file.get_ensemble_datetimes()[start_ensemble:end_ensemble]
    

    subplot_titles = []
    fig,ax = subplots( figheight = 2.5, figwidth = 10.5, width_ratios = [1])
    

    ## format the ADCP data axes (left)
    topax = ax.twiny()
    ax.set_title(title)
    
    
    # set plot params based on instrument configuration 

    
    
    # set plotting extents in vertical direction
    if plot_by == 'bin':
        ylims = [start_bin,end_bin]
        ax.set_ylabel('Bin')
    elif plot_by == 'depth':
        bin_depths = adcp_file.get_bin_midpoints_depth()
        ylims = [bin_depths[start_bin],bin_depths[end_bin]]
        ax.set_ylabel('Depth')
    elif plot_by == 'HAB':
        bin_heights = adcp_file.get_bin_midpoints_HAB()
        ylims = [bin_heights[start_bin],bin_heights[end_bin]]
        ax.set_ylabel('Height Above Bed')
    else: 
        print('Invalid plot_by parameter')
    
    
    # set plotting extents in horizontal direction
    xlims = mdates.date2num(ensemble_times) # list of elegible xlimits 
    if adcp_file.beam_facing == 'UP':
        extent = [xlims[0],xlims[-1],ylims[0],ylims[1]]
    else:
        x = np.flipud(x)
        extent = [xlims[0],xlims[-1],ylims[1],ylims[0]]
        
        
    cmaps = {'PERCENT GOOD': plt.cm.bone,
             'ECHO INTENSITY': plt.cm.turbo,
             'CORRELATION MAGNITUDE': plt.cm.nipy_spectral,
             'ABSOLUTE BACKSCATTER':cmocean.cm.thermal,
             'SIGNAL TO NOISE RATIO':plt.cm.Reds}
    cmap = cmaps[field]
    
    
    im = ax.imshow(x, origin = 'lower', extent = extent, cmap = cmap, aspect = 'auto')
    cbar = fig.colorbar(im, ax=ax,orientation="vertical",location = 'right',fraction=0.046)
    
    if beam == 0:
        cbar_label = f'{field}\n BEAM AVERAGE' 
    else:
        cbar_label = f'{field}\n BEAM {beam}' 
    cbar.set_label(cbar_label, rotation=90,fontsize= 9)
    
    
    ax.xaxis.set_major_locator(mticker.FixedLocator(ax.get_xticks()))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M %d%b%y '))
    topax.set_xlim(start_ensemble,end_ensemble)
    ax.set_xlabel('Ensemble')
    ax.grid(alpha = 0.1)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha = 'left')
    

    
    return fig,ax


#%%
def progressive_vector_plot(adcp_file,**kwargs):
    """
    

    Generate a progressive vector plot from the WorkhorseADCP class object 

    Parameters
    ----------
    adcp_file : object
        WorkhorseADCP object.
    color_by : str
        Coloring method ('bin','velocity','month').
    start_bin : int
        First bin to plot. (use zero based index)
    end_bin : int
        Last bin to plot.(use zero based index)
    start_ensemble : int
        First ensemble to plot.(use zero based index)
    end_ensemble : int
        Last ensemble to plot.(use zero based index)
    title : str
        plot axes title.

    Returns
    -------
    fig,ax
        matplotlib figure and axes objects

    """
    


    if kwargs.get('color_by'):color_by = kwargs.get('color_by')
    else: color_by = 'bin'
    
    if kwargs.get('start_bin'): start_bin = kwargs.get('start_bin')
    else: start_bin = 0
    
    if kwargs.get('end_bin'): end_bin = kwargs.get('end_bin')
    else: end_bin = adcp_file.n_bins-1
    
    if kwargs.get('start_ensemble'): start_ensemble = kwargs.get('start_ensemble')
    else: start_ensemble = 0
    
    if kwargs.get('end_ensemble'): end_ensemble= kwargs.get('end_ensemble')
    else: end_ensemble = adcp_file.n_ensembles   
    
    if kwargs.get('title'): title = kwargs.get('title')
    else: title = adcp_file.filepath.split(os.sep)[-1]     
    


    
    #adcp_file = adcp_file[ID]
    # start_ensemble = 0
    # end_ensemble = adcp_file.n_ensembles
    # start_bin = 0
    # end_bin = adcp_file.n_bins-1
    #color_by = 'bin' #velocity'  #bin'#'velocity'#'bin'
    
    
    plot = True
    nbins = (end_bin - start_bin)+1

    
    
    
    
    u,v,z,du,dv,dz,err = adcp_file.get_velocity()
    ensemble_times = adcp_file.get_ensemble_datetimes()[start_ensemble:end_ensemble]
    
    
    u = u[start_ensemble:end_ensemble,start_bin:end_bin+1]
    v = v[start_ensemble:end_ensemble,start_bin:end_bin+1]
    z = z[start_ensemble:end_ensemble,start_bin:end_bin+1]
    du = du[start_ensemble:end_ensemble,start_bin:end_bin+1]
    dv = dv[start_ensemble:end_ensemble,start_bin:end_bin+1]
    dz = dz[start_ensemble:end_ensemble,start_bin:end_bin+1]
    
    xy_speed = np.sqrt(u**2 + v**2)
    
    pu = np.nancumsum(du,axis = 0) #,-np.outer(du[0,:],np.ones(self.n_ensembles)).T])
    pv = np.nancumsum(dv,axis = 0) # ,-np.outer(dv[0,:],np.ones(self.n_ensembles)).T])
    pz = np.nancumsum(dz,axis = 0) # ,-np.outer(dz[0,:],np.ones(self.n_ensembles)).T])
    
    
    if plot:
        # fig = plt.figure()
        # ax = plt.gca()
        #fig, ax = plt.subplots(1, 2,gridspec_kw={'width_ratios': [3, 1]})
        
        fig,ax = subplots( figheight = 5, figwidth =5.5, width_ratios = [1])
 
        #ax.set_aspect('equal')
        ax.grid(alpha = 0.3)
        ax.set_xlabel('East Distance (m)')
        ax.set_ylabel('North Distance (m)')
        ax.set_title(title)
        #ax.set_aspect('equal',adjustable = 'datalim')
        

        cbar_shrink = .046#.75
        global points,segments
        
        if color_by == 'bin':

            cmap = plt.cm.Spectral  # define the colormap
            # extract all colors from the .jet map
            cmaplist = [cmap(i) for i in range(cmap.N)]
            # force the first color entry to be grey
            cmaplist[0] = (.5, .5, .5, 1.0)
            
            # create the new map
            cmap = mpl.colors.LinearSegmentedColormap.from_list(
                'Custom cmap', cmaplist, cmap.N)
            
            # define the bins and normalize
            bounds = np.linspace(0, nbins, nbins+1)
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
            for b in range(nbins):
                #ax.plot(pu[:,b],pv[:,b], label = f'Bin {start_bin+b}')#, c = cmap(b), norm = norm)#,color = colors[s],alpha = 0.6)
    
                points = np.array((pu[:-1,b], pv[:-1,b])).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                #norm = plt.Normalize(0, adcp_file.n_bins,1)
                lines = LineCollection(segments, cmap=cmap, norm=norm)
                lines.set_array(len(points)*[b])
                lines.set_linewidth(1)
                line = ax.add_collection(lines)           
            cbar = fig.colorbar(line, ax=ax,orientation="vertical")
            cbar.set_label('Bin Number', rotation=270, labelpad = 10, fontsize = 12)
    
    
        elif color_by == 'velocity':
            cmap = plt.cm.jet
            for b in range(nbins):
                points = np.array((pu[:-1,b], pv[1:,b])).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                norm = plt.Normalize(0, np.quantile(xy_speed[~np.isnan(xy_speed)],0.99))
                lines = LineCollection(segments, cmap=cmap, norm=norm)
                lines.set_array(xy_speed[:,b])
                lines.set_linewidth(1)
                line = ax.add_collection(lines)
                #break
            cbar = fig.colorbar(line, ax=ax,orientation="vertical")
            cbar.set_label('Velocity (m/s) ', rotation=270, labelpad = 10, fontsize = 12)
            
        elif color_by == 'month':
            cmap = plt.cm.get_cmap('tab20b', 12)
            def gen_interval(x):
                x = x.isoweekday()
                return x
            vgen_interval = np.vectorize(gen_interval)
            months = [i.month for i in ensemble_times]
            for b in range(nbins):
                points = np.array((pu[:-1,b], pv[1:,b])).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                norm = plt.Normalize(1,12)
                lines = LineCollection(segments, cmap=cmap, norm=norm)
                lines.set_array(months)
                lines.set_linewidth(1)
                line = ax.add_collection(lines)
                #break
            cbar = fig.colorbar(line, ax=ax,orientation="vertical")
            cbar.set_label('Month of Year', rotation=270, labelpad = 10, fontsize = 12)        
            
            
        else:
            print(r'Invalid plot mode {color_by}')
    
        #set axes limits 
        xrange = 1.1*(np.nanmax(abs(pu)))
        yrange = 1.1*(np.nanmax(abs(pv)))
        
        rng = max(xrange,yrange)
        #print([np.nanmax(pu),xrange])
        # ax.set_xbound([-xrange,xrange])
        # ax.set_ybound([-yrange,yrange])
        
        ax.set_xlim(-rng,rng)
        ax.set_ylim(-rng,rng)
    
        ax.set_aspect('equal')

    return fig,ax
#%%






