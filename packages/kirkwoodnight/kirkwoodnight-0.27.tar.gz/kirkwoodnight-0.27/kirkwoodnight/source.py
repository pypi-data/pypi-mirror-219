# version 0.14

# basic importsl 
import os
import numpy as np
import pandas as pd
import pkg_resources

# date/time functionality
import datetime
from datetime import date

# color and visualization
from tabulate import tabulate
from colorama import Fore

# skyfield (for locations of solar system objects)
import skyfield
from skyfield.api import load
from skyfield.api import position_of_radec, load_constellation_map, load_constellation_names
from skyfield.magnitudelib import planetary_magnitude

# astropy (coordinates, units, date/time functionality)
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.table import Table
from astropy.time import Time
from astropy.time import TimeDelta

# astroplan
import astroplan
from astroplan import FixedTarget
from astropy.table import QTable
from astroplan.utils import time_grid_from_range
from astroplan import Observer
from astroplan import (AltitudeConstraint, AirmassConstraint,
                       AtNightConstraint, MoonIlluminationConstraint, MoonSeparationConstraint)

def make_planet_table(date_str):
    '''Make Planet Table

    Generates AstroPy Table with positions (RA, Dec) of solar system planets on the given date.
    
    Args:
        date_str (str): Desired date (str, formatted as "YYYY-MM-DD")

    Returns:
        df (DataFrame): Table of RA/dec for each object (AstroPy Table)
    '''

    y,m,d = [int(num) for num in date_str.split("-")] # split input date into constituents

    ts = load.timescale()
    t = ts.utc(y, m, d)
    planets = load('de421.bsp') # load ephemerides

    earth = planets["earth"] # establish earth location
    barycentric = earth.at(t)

    # other 7 planets
    pl_l = ["mercury", "venus", "mars", "jupiter barycenter", "saturn barycenter", "uranus barycenter", "neptune barycenter"]
    pl_names = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    type_l = ["Planet"]*len(pl_names)
    subtype_l = ["Terrestrial", "Terrestrial", "Terrestrial", "Gas Giant", "Gas Giant", "Ice Giant", "Ice Giant"]
    mag_l = []
    ra_l = []
    dec_l = []

    # grab position of every other planet
    for pl in pl_l:
        planet = planets[pl]
        astrometric = barycentric.observe(planet) # set coordinate system
        ra, dec, distance = astrometric.radec(t) # grab ra, dec of planet
        mag_l.append(planetary_magnitude(astrometric))  # calculate apparent mag of planet
        ra, dec = float(ra._degrees), float(dec._degrees) # convert RA and dec to degrees
        ra_l.append(ra), dec_l.append(dec)
        
    # find constellation for each planet
    constellation_at = load_constellation_map() 
    pos = position_of_radec(np.array(ra_l)/15, np.array(dec_l))
    const_abbrev = constellation_at(pos)
    const_name_dict = dict(load_constellation_names())
    const_l = [const_name_dict[abbrev] for abbrev in const_abbrev]
        
    # return pandas dataframe with info for planets
    df = pd.DataFrame({"Name": pl_names, "RA": ra_l, "Dec": dec_l, "Type": type_l, "Subtype": subtype_l, "Constellation": const_l, "Magnitude": mag_l})
    return df


def make_constraints(alt_lim = (10, 80), moon_sep = 5, max_airmass = None, night_type = None, moon_illum = None):
    '''Make Constraints

    Creates list of desired observational constraints for use in sim_kirkwood_obs. Intended only as a helper function.
    
    Args: (to be called in sim_kirkwood_obs, if needed)
        alt_lim (tuple): Lower and upper bounds (in deg) on allowable altitude of telescope, default is (20, 80)
        moon_sep (float): Minimum angular separation (in deg) from moon, default is 5
        max_airmass (float, optional): Maximum allowable airmass
        night_type (str, optional): Defines beginning and end of night, options are "civil", "naut", and "astro" respectively for "civilian", "nautical", and "astronomical" definitions of twilight
        moon_illum (str, optional): Allowable moon phase, options are "grey" and "dark"
    
    Returns:
        constraints (list): List of observational constraints (List of Astroplan objects)
    '''
    
    constraints = [AltitudeConstraint(alt_lim[0]*u.deg, alt_lim[1]*u.deg), MoonSeparationConstraint(moon_sep*u.deg)]
    if max_airmass:
        constraints.append(AirmassConstraint(max_airmass))
    if night_type == "civ":
        constraints.append(AtNightConstraint.twilight_civil())
    if night_type == "naut":
        constraints.append(AtNightConstraint.twilight_nautical())
    if night_type == "astro":
        constraints.append(AtNightConstraint.twilight_astronomical())
    if night_type == "grey":
        constraints.append(MoonIlluminationConstraint.grey())
    if night_type == "dark":
        constraints.append(MoonIlluminationConstraint.dark()) 
        
    return constraints

def make_obs_grid(kirkwood, constraints, targets, t1_ust, t2_ust, dt = 0.5):
    '''Make Observation Grid

    Creates grids (NumPy arrays) defining observational efficacy for each object during the desired night.
    Intended only as a helper function for sim_kirkwood_obs.
    
    Args:
        kirkwood (Astroplan Observer object): Object defining location of Kirkwood observatory. Passed automatically from sim_kirkwood_obs, does not require user alteration.
        constraints (list): Output from make_constraints (list of Astroplan Constraint objects). Passed automatically from sim_kirkwood_obs, does not require user alteration.
        targets (list): List of objects definiting positions of target objects (Astroplan Target objects). Passed automatically from sim_kirkwood_obs, does not require user alteration.
        t1_ust, t2_ust (AstroPy.Time objects): Starting and ending time of observations in Universal Standard Time. Passed autmoatically form sim_kirkwood_obs, does not require user alteration.
        dt (float): Time interval of output observing schedule (in hours), default is 0.5 (30 mins). Can be called directly in sim_kirkwood_obs, if needed.)
    
    Returns:
        time_grid (array): time array for observing schedule (in UST) expressed as Julian Date
    
    '''
    
    dt *= u.hour # add astropy units to dt
    grid_list = []
    time_grid = time_grid_from_range([t1_ust, t2_ust], # create time grid
                                 time_resolution=dt)
    for target in targets: # iterate over targets
        # initialize blank grid with size len(constraints)*len(time_grid)
        # each row is one of the requested constraints, each column is an interval of size dt during the observing run
        observability_grid = np.zeros((len(constraints), len(time_grid)))
        for i, constraint in enumerate(constraints):
            # populate observability grid
            # array value is 0 if the constraint is not met, 1 if satisfied
            observability_grid[i, :] = constraint(kirkwood, target, times=time_grid)
        grid_list.append(observability_grid) # make list of grids, one for each object
    big_grid = np.array(grid_list)
    # combine all constraints to make observing schedule
    # total_obs is an array of size num_objects*len(time_grid)
    # array value is 0 if object is not observable during that block, 1 if it is
    total_obs = np.prod(big_grid, axis = 1)
    # for each object calculate percentage of night it will be observable
    obs_percent = np.sum(total_obs, axis = 1)/total_obs.shape[1]
    print()
    return time_grid, total_obs, obs_percent


def sim_kirkwood_obs(date = str(date.today()), start_time = str(datetime.datetime.now().time()), duration = 4,
                        alt_lim = (10, 80), moon_sep = 5, max_airmass = None, night_type = None, moon_illum = None, dt = 0.5):
    '''Simulate Kirkwood Observation

    Given date, time, and duration of an observing run (with optional observational constraints),
    prints table of object positions ranked by duration of observability, as well as rough observing schedule 
    detailing blocks of time when each object will be observable during the run. With user input of desired
    objects, saves text files with general info, sky positions, and observability for each object. 
    
    Args:
        date (str): desired date of observation, formatted as "YYYY-MM-DD", default is present day
        start_time (str): desired start time of observing run (in local time zone), formatted as "HH:MM", defaults to current clock time
        duration (float): approximate duration of observing run (in hours), defaults to 4
        alt_lim (tuple, optional): arg of make_constraints
        moon_sep (float, optional): arg of make_constraints
        max_airmass (float, optional): arg of make_constraints
        night_type (str, optional): arg of make_constraints
        moon_illum (str, optional): arg of make_constraints
        dt (float, optional): time interval for observing grid, argument for make_obs_grid
    
    Returns:
        target_df (DataFrame): pandas DataFrame containing the target info for those selected for observation.
        time_df (DataFrame): pandas DataFrame containing the target observing plans as a function of time.
    
    '''

    t1 = Time(date + " " + start_time) # convert start time to time object
    t2 = t1 + TimeDelta(duration*u.h) # make end time and add units
    
    # define Observer object, input location of Kirkwood
    kirkwood = Observer(longitude=-86.5264*u.deg, latitude=39.1653*u.deg,
                  elevation=235*u.m, name="Kirkwood", timezone="US/East-Indiana")
    
    # convert EST to UST
    t1_ust, t2_ust = t1 + TimeDelta(4*u.h), t2 + TimeDelta(4*u.h)
    time_range = Time([t1_ust, t2_ust])

    # make table of planets
    planet_df = make_planet_table(date)
    
    # make table of deep sky objects
    stream = pkg_resources.resource_stream(__name__, 'data/obj_list.csv')
    deep_sky_df = pd.read_csv(stream, encoding = "latin-1")
    target_df = pd.concat([planet_df, deep_sky_df])

    # make astropy table to feed into astroplan
    target_table_pd = target_df[["Name", "RA", "Dec"]]
    target_table = Table.from_pandas(target_table_pd)
    targets = [FixedTarget(coord=SkyCoord(ra=ra*u.deg, dec=dec*u.deg), name=name) for name, ra, dec in target_table]
    
    # make constraints
    constraints = make_constraints(alt_lim, moon_sep, max_airmass, night_type, moon_illum)
    # make time grid and raw observing tables/schedule
    time_grid, total_obs, obs_percent = make_obs_grid(kirkwood, constraints, targets, t1_ust, t2_ust, dt)
    
    # build dataframe of all targets, add column for observability fraction
    target_df["Obs. Frac."] = obs_percent
    target_df = target_df.set_index("Name")
    target_df["Magnitude"] = target_df["Magnitude"].astype(float)
    target_df = target_df.sort_values(by=['Obs. Frac.', "Magnitude"], ascending = [False, True]) # sort table by observability and brightness
    target_df = target_df.round(2)

    types = list(set(target_df["Type"]))
    types = [" " + item for item in types]
    print("Is/are there a particular type(s) of object you would like to look at? The options are:\n")
    print(",".join([i for i in types]))
    print("\nPlease enter the type(s) of the objects you would like to observe, separated by commas (if multiple). Hit ENTER to observe all listed types.")
    var = input()
    if var == "exit":
            sys.exit()
    if var!= "":
        var = var.split(",")
        target_df = target_df[target_df["Type"].isin(var)]
        subtypes = list(set(target_df["Subtype"]))
        subtypes = [item + " " for item in subtypes]
        print("Is there a specific subtype of object you would like to look at? The options are:\n")
        print(",".join([i for i in subtypes]))
        print("\nPlease enter the subtype(s) of object you would like to observe, separated by commas (if multiple). Hit ENTER to observe all listed subtypes.")
        subvar = input()
        if subvar == "exit":
            sys.exit()
        if subvar != "":
            subvar = subvar.split(",")
            target_df = target_df[target_df["Subtype"].isin(var)]

    display_N = len(target_df.index)

    if display_N >= 20:
        # user input for how many objects to display in printed tables
        display_N = 20
        print("How many objects would you like displayed? (Sorted by most observable, hit ENTER for default of 20. Maximum is %d)"%(len(target_df.index)))
        var = input()
        if var == "exit":
            sys.exit()
        if var != "":
            display_N  = int(var)

    target_df = target_df[:display_N]
    target_names_ordered = list(target_df.index)
    
    # convert time array back to EST
    time_est = [t.datetime - datetime.timedelta(hours=4) for t in time_grid]
    time_labels = [t.strftime("%H:%M") for t in time_est]
    
    # make dataframe for observing schedule
    time_df = pd.DataFrame(total_obs, columns = time_labels)
    time_df.insert(0, "Name", target_names_ordered)
    time_df = time_df.set_index("Name")
    time_df = time_df[time_df.index.isin(target_names_ordered)]
    time_df = time_df.reindex(target_df.index) # sort objects to be in same order as other table
    time_df = time_df.replace([0, 1], [Fore.RED + "no"  + Fore.RESET, Fore.GREEN + 'YES' + Fore.RESET]) # add color
    
    # add ID numbers to objects
    target_df.insert(0, "ID", range(1, len(target_df) + 1))
    time_df.insert(0, "ID", range(1, len(time_df) + 1))

    # display information table
    print(tabulate(target_df[:display_N], headers = 'keys', tablefmt = 'psql'))

    # display schedule
    print(tabulate(time_df[:display_N], headers = 'keys', tablefmt = 'psql'))

    # user input for which object IDs they want to observe
    print("\nWould you like to generate infromation/schedule files for select objects? Type 'yes' or press ENTER to exit the program):")
    var = input()
    if var == "" or var == "exit":
        sys.exit()
    if var == "yes":
        print("Please enter the IDs of the objects you would like to observe, separated by commas. Hit ENTER to observe all listed objects.")

        ids = input()
        if ids == "exit":
            sys.exit()

        print("Generating files...")

        if ids == "":
            ids = list(range(1, display_N + 1))
        else:
            ids = ids.split(","); ids = [int(i) for i in ids]
    
        # limit info and schedule dataframes only to selected objects
        selected_target_df = target_df.loc[target_df['ID'].isin(ids)]
        selected_names = list(selected_target_df.index) # names of selected objects
        selected_time_df = time_df.loc[time_df['ID'].isin(ids)]
        selected_time_df = selected_time_df.replace([Fore.RED + "no"  + Fore.RESET, Fore.GREEN + 'YES' + Fore.RESET], ["no", "YES"])
    
        # remake astroplan targets for selected objects
        selected_target_df_pos = selected_target_df[["RA", "Dec"]]
        selected_target_df_pos.reset_index(inplace=True)
        selected_target_table = Table.from_pandas(selected_target_df_pos)
        selected_targets = [FixedTarget(coord=SkyCoord(ra=ra*u.deg, dec=dec*u.deg), name=name) for name, ra, dec in selected_target_table]

        # create directories for output files
        dir = "output"
        os.makedirs(dir, exist_ok=True)
        subdir = dir + "/" + str(datetime.datetime.now()).split(" ")[0] + "_" + str(datetime.datetime.now()).split(" ")[1][:8].replace(":", ".")
        os.makedirs(subdir, exist_ok = True)

    # loop over targets and calcluate alt and az for each time interval during the night
        for i in range(len(selected_targets)):
           alt, az = [], []
           for t in time_grid:
               t = Time(t.datetime)
                alt.append(kirkwood.altaz(t, selected_targets[i]).alt.value)
                az.append(kirkwood.altaz(t, selected_targets[i]).az.value)
            obj = selected_names[i]
            target_info = selected_target_df.loc[obj]
            target_time = selected_time_df.loc[obj]
            target_info = target_info.drop(labels=["ID"]) # final info for selected object
            target_time = target_time.drop(labels=["ID"])
            target_obs = list(target_time)
            target_time = pd.DataFrame([time_labels, target_obs, alt, az])
            target_time = target_time.T
            target_time.columns = ["Time", "Observable", "Alt", 'Az']
            target_time = target_time.set_index("Time") # final schedule (and alt/az) for selected object

        # write info/schedule files for each object and save
        filename = obj+"_summary.txt"
                    
        with open(subdir + "/" + filename, 'w') as f:
            f.write(target_info.to_string() + "\n" + "\n")
            f.write(target_time.to_string())
            print("Info and schedule for selected objects saved as text files in " + subdir)

    # write and save log file
        print("\nWould you like to save a log file? Type 'yes' or press ENTER to exit the program:")
        var = input()
        if var == "":
            sys.exit()
        if var == "yes":
            with open(subdir + "/" + "log", 'w') as f:
                f.write("Date/Time:" + " " + str(datetime.datetime.now()) + "\n" + "\n")
                f.write("Desired Date: " + str(date) + "\n")
                f.write("Desired Start Time: " + str(start_time) + "\n")
                f.write("Duration (hrs): " + str(duration) + "\n")
                f.write("Altitude Range (deg): " + str(alt_lim[0]) + " to " + str(alt_lim[1]) + "\n")
                f.write("Minimum Moon Separation (deg): " + str(moon_sep) + "\n")
                f.write("Maximum Airmass: " + str(max_airmass) + "\n")
                f.write("Twilight Convention: " + str(night_type) + "\n")
                f.write("Lunar Illumination: " + str(moon_illum) + "\n")
                f.write("Time Partition (hrs): " + str(dt) + "\n" + "\n")
                f.write(str(len(selected_targets)) + " objects selected for observation: \n")
                for obj in selected_names:
                    f.write(obj + "\n")

    print("Log file saved in " + subdir)

    return target_df, time_df