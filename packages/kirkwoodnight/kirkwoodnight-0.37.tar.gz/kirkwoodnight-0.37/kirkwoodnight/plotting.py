import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.dates as mdates
import os

def get_summary(path):
    ra = None
    dec = None
    type_ = None
    constellation = None
    magnitude = None
    obs_frac = None
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("ID"):
                id = line.split()[-1]
            if line.startswith("RA"):
                ra = line.split()[-1]
            elif line.startswith("Dec"):
                dec = line.split()[-1]
            elif line.startswith("Type"):
                type_ = line.split()[-1]
            elif line.startswith("Subype"):
                subtype_ = line.split()[-1]
            elif line.startswith("Constellation"):
                constellation = line.split()[-1]
            elif line.startswith("V Mag"):
                magnitude = line.split()[-1]
            elif line.startswith("Obs. Frac."):
                obs_frac = line.split()[-1]
    time,Observable,alt,az = np.loadtxt(path,skiprows=12,unpack=True,dtype=str)
    return id,ra,dec,type_,subtype_,constellation,magnitude,obs_frac,time,Observable,alt,az



def plot_it(files_path):

    summaries = [x for x in os.listdir(files_path) if x.endswith("summary.txt")]

    # get time series
    for summ in summaries[:1]:
        path = os.path.join(files_path,summ)
        id,ra,dec,type_,subtype_,constellation,magnitude,obs_frac,time_series,Observable,alt,az = get_summary(path)
        
        
    recording = dict()    
        
    for i,time in enumerate(time_series):
        # print(time)
        recording[time] = dict()
        
        # get data
        id_list = [];ra_list = [];dec_list = [];type_list = [];subtype_list=[];constellation_list = [];magnitude_list = [];obs_frac_list = []
        observable_list = [];alt_list = [];az_list = [];names = []
        for summ in summaries:
            path = os.path.join(files_path,summ)
            id,ra,dec,type_,subtype_,constellation,magnitude,obs_frac,time_series,Observable,alt,az = get_summary(path)
            
            id_list.append(id);ra_list.append(ra);dec_list.append(dec);type_list.append(type_);subtype_list.append(subtype_);constellation_list.append(constellation)
            magnitude_list.append(magnitude);obs_frac_list.append(obs_frac);observable_list.append(Observable[i])
            alt_list.append(alt[i]);az_list.append(az[i])
            names.append(summ.split("_")[0].strip())
            
        recording[time]['id'] = id_list
        recording[time]['ra'] = np.array(ra_list,dtype=float)
        recording[time]['dec'] = np.array(dec_list,dtype=float)
        recording[time]['type'] = type_list
        recording[time]['subtype'] = subtype_list
        recording[time]['constellation'] = constellation_list
        recording[time]['magnitude'] = np.array(magnitude_list,dtype=float)
        recording[time]['obs_frac'] = np.array(obs_frac_list,dtype=float)
        observable_list = np.array(observable_list,dtype=str)
        observable_list[observable_list == 'YES'] = 1
        observable_list[observable_list == 'NO'] = 0

        recording[time]['Observable'] = np.array(observable_list,dtype=int)
        recording[time]['alt'] = np.array(alt_list,dtype=float)
        recording[time]['az'] = np.array(az_list,dtype=float)
        recording[time]['names'] = names


        # load data and plot it
        id = recording[time]['id']
        ra = recording[time]['ra']
        dec = recording[time]['dec']
        type_ = recording[time]['type']
        subtype_ = recording[time]['subtype']
        constellation = recording[time]['constellation']
        mag = recording[time]['magnitude']
        obs_frac = recording[time]['obs_frac']
        observable = recording[time]['Observable']
        alt = recording[time]['alt']
        az = recording[time]['az']
        names = recording[time]['names']
        # Create a polar plot
        fig = plt.figure( figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')

        for i in range(len(ra)):
            id = id[i]
            ra_deg = ra[i]*u.degree
            dec_deg = dec[i]*u.degree

            sky_position = SkyCoord(ra_deg, dec_deg, frame='icrs')

            # Convert to Alt/Az coordinates for the plot
            alt_deg = alt[i]*u.degree
            az_deg = az[i]*u.degree
            horizon_position = SkyCoord(alt=alt_deg, az=az_deg, frame='altaz')

            # Convert azimuth to plot correctly in polar coordinates
            radians = (90 - az_deg.value) * u.degree.to(u.radian)

            ax.plot(radians, alt_deg.value, 'o', color='#041A40', markersize=15, alpha=0.75)
            ax.plot(radians, alt_deg.value, 'o', color='white', markersize=10, alpha=0, label=id+ ": " +names[i])
            ax.text(radians, alt_deg.value, i, color='yellow', ha='center', va='center',zorder=10, rotation=0,fontweight='bold')

        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

        ax.xaxis.grid(color='k', linestyle='solid')
        ax.yaxis.grid(color='k', linestyle='solid')
        ax.xaxis.label.set_color('k')
        ax.tick_params(axis='x', colors='k')
        ax.tick_params(axis='y', colors='k')
        # Add cardinal directions
        ax.text(-0.15, 0.5, 'W', color='k', ha='center', va='center', alpha=1, fontweight='bold', fontsize=20, transform=ax.transAxes)
        ax.text(1.15, 0.5, 'E', color='k', ha='center', va='center', alpha=1, fontweight='bold', fontsize=20, transform=ax.transAxes)
        ax.text(0.5, 1.15, 'N', color='k', ha='center', va='center', alpha=1, fontweight='bold', fontsize=20, transform=ax.transAxes)
        ax.text(0.5, -0.15, 'S', color='k', ha='center', va='center', alpha=1, fontweight='bold', fontsize=20, transform=ax.transAxes)


        # Change the color of the outer circle to white
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
            
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=5, facecolor='white', edgecolor='white', fontsize=12)
        plt.title('Time:'+time,color='k')
        plt.savefig(files_path+time+'.png',dpi=300,bbox_inches='tight',facecolor='black')
 