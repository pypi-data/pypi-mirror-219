import kirkwoodnight
from kirkwoodnight import source
import datetime
from datetime import date

def_l = [str(date.today()), str(datetime.datetime.now().time()), 4, 20, 85, 5, None, None, None, 0.5]

message_list = ["\nWelcome! Until the 'Generating Files...' message, type 'finish' at any point to accept defaults for all remaining settings and constraints, or type 'restart' at any point to begin from scatch. (hit ENTER to begin)",
                "Which date would you like to observe on? (Enter as YYYY-MM-DD, default is today):",
                "What time would you like to start your run? (Enter in military time as HH:MM, default is current local time):",
                "How many hours would you like to observe for? (default is 4)",
                "Would you like to change Kirkwood's minimum altitude limit (in degrees)? (Type value if desired, otherwise hit ENTER. Default is 20.)",
                "Would you like to change Kirkwood's maximum altitude limit (in degrees)? (Type value if desired, otherwise hit ENTER. Default is 85.)",
                "Would you like to change the minimum mandated distance (in degrees) from the Moon? (Type value if desired, otherwise hit ENTER. Default is 5.)",
                "Would you like to specify a maximum allowed airmass? (Type value if desired, otherwise hit ENTER. Default is None.)",
                "Would you like to specify a desired level of darkness for the night? (If desired, type 'civ' or 'naut' or 'astro' to respectively signify civil, nautical, or astronomical twilight. Otherwise hit ENTER. Default is None.)",
                "Would you like to specify a maximum brightness level for the moon? (If desired, type 'grey' or 'dark', otherwise hit ENTER. Default is None.)",
                "How often do you want to re-check for observability (in hours)? (type value if desired, otherwise hit ENTER. Default is 0.5, which creates a schedule in 30 minute intervals.)"]

def input_loop(def_l):
    '''Input Loop

    This function takes in user input and assigns program settings according to user input.
    '''
    for i in range(len(def_l)+1): # add one since intro prompt
        print(message_list[i])
        var = input()
        finished = False
        if var == "exit":
            sys.exit()
        if var == "finish":
            print('Defaults selected for remaining settings.')
            finished = True
            return finished
        elif var == "restart":
            finished = input_loop(def_l)
            if finished:
                return finished
        elif i != 0 and var != "" and ((var != "restart") and (var != "finish")):
            if int(i-1) in [2, 3, 4, 5, 6, 9]: # i-1 to account for intro prompt
                var = float(var)
            def_l[i-1] = var # account for intro prompt
    return finished

def main():   
# print interactive prompts in terminal
    print()
    print("------------------------------------------------------------------------")
    print("KIRKWOOD OBSERVING PLANNER")
    print("CREATED BY: ARMAAN GOYAL, BRANDON RADZOM, JESSICA RANSHAW, XIAN-YU WANG")
    print("LAST UPDATED ON 2023-07-14")
    print("ACCESSED ON %s"%str(datetime.datetime.now()))
    print("------------------------------------------------------------------------")

    print("\n For best results, maximize terminal to fullscreen. \n")
    input_loop(def_l)
    # for i in range(len(def_l)):
    #     print(message_list[i])
    #     var = input()
    #     if var != "":
    #         if i in [2, 3, 4, 5, 6, 9]:
    #             var = float(var)
    #         def_l[i] = var
    #     elif var == "finish":
    #         print('Defaults selected for remaining settings.')
    #         break
    #     elif var =='restart':



    print("Generating Info and Schedules...")

    source.sim_kirkwood_obs(date = def_l[0], start_time = def_l[1], duration = def_l[2],
                        alt_lim = (def_l[3], def_l[4]), moon_sep = def_l[5], max_airmass = def_l[6], night_type = def_l[7], moon_illum = def_l[8], dt = def_l[9])