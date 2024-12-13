import numpy as np
import matplotlib.pyplot as plt
import spiceypy as spice
import sys, os

sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\julian.py'))
sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\pcfunc.py'))
sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\getdate.py'))
sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\lambert.py'))
sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\mme2000.py'))
sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\p2000.py'))
sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\jd2str.py'))
sys.path.append(os.path.dirname('D:\Yongjin\Code\ACML_Space\ACML_Space\Solver\atan.py'))

from getdate import getdate  # External function
from julian import juli # External function
from pcfunc import pcfunc  # External function
from p2000 import p2000

def spice_import():
     spice.furnsh('D:\Yongjin\Code\ACML_Space\ACML_Space\data\de440.bsp')

def spice_terminate():
    spice.unload('D:\Yongjin\Code\ACML_Space\ACML_Space\data\de440.bsp')

def porkchop_plot():
    """
    Python script for creating ballistic interplanetary pork chop plots using SPICE routines.
    """
    # Constants
    spice_import()
    mu = 132712441933.0  # Gravitational constant of the sun (km^3/sec^2)
    rtd = 180.0 / np.pi
    revmax = 0

    # Get launch and arrival planets
    print("Select departure planet (Earth=3, Mars=4, Venus=2, etc.):")
    ip1 = int(input("Departure planet ID: "))
    print("Select arrival planet (Earth=3, Mars=4, Venus=2, etc.):")
    ip2 = int(input("Arrival planet ID: "))

     # Get nominal departure and arrival dates
    print("Enter nominal departure date:")
    dep_month, dep_day, dep_year = getdate()
    JD_dep = juli(dep_month, dep_day, dep_year)

    print("Enter nominal arrival date:")
    arr_month, arr_day, arr_year = getdate()
    JD_arr = juli(arr_month, arr_day, arr_year)


    print(JD_dep)
    print(JD_arr)

    # Get date spans and step size
    spanx = int(input("Enter launch date span in days: "))
    spany = int(input("Enter arrival date span in days: "))
    step = int(input("Enter step size in days: "))

# Get contour levels with defaults
    print("Enter launch C3 contour levels (comma-separated) or press Enter for defaults:")
    c3_input = input()
    c3_levels = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50] if not c3_input else list(map(float, c3_input.split(',')))

    print("Enter arrival v-infinity contour levels (comma-separated) or press Enter for defaults:")
    vinf_input = input()
    vinf_levels = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0] if not vinf_input else list(map(float, vinf_input.split(',')))

    print("Enter launch declination levels (comma-separated) or press Enter for defaults:")
    dla_input = input()
    dla_levels = [-30, -20, -10, 0, 10, 20, 30] if not dla_input else list(map(float, dla_input.split(',')))

    print("Enter launch RA levels (comma-separated) or press Enter for defaults:")
    rla_input = input()
    rla_levels = [0, 45, 90, 135, 180, 225, 270, 315] if not rla_input else list(map(float, rla_input.split(',')))

    print("Enter time-of-flight levels (comma-separated) or press Enter for defaults:")
    tof_input = input()
    tof_levels = [100, 150, 200, 250, 300, 350, 400] if not tof_input else list(map(float, tof_input.split(',')))

    print("Enter total delta-v levels (comma-separated) or press Enter for defaults:")
    dvt_input = input()
    dvt_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] if not dvt_input else list(map(float, dvt_input.split(',')))

    # Prepare arrays for contour plots
    con_x, con_y = [], []
    c3_dep, vinf_arr = [], []
    decl_dep, decl_arr = [], []
    rasc_dep, rasc_arr = [], []
    tof, dvtotal = [], []

    for i in range(int(JD_dep - spanx), int(JD_dep + spanx + 1), step):
        row_c3, row_vinf, row_decl_dep, row_decl_arr = [], [], [], []
        row_rasc_dep, row_rasc_arr, row_tof, row_dvt = [], [], [], []
        con_x.append(i - JD_dep)

        for j in range(int(JD_arr - spany), int(JD_arr + spany + 1), step):
            con_y.append(j - JD_arr)

            # Compute departure and arrival delta-v
            dv1, dv2 = pcfunc(i, j, mu, ip1, ip2, revmax)

            c3l = np.linalg.norm(dv1)**2
            vinf = np.linalg.norm(dv2)

            row_c3.append(c3l)
            row_vinf.append(vinf)

            # Compute declination and RA for departure
            if c3l <= 50:  # Arbitrary threshold for valid C3
                decl_dep_val = 90.0 - rtd * np.arccos(dv1[2] / np.linalg.norm(dv1))
                rasc_dep_val = rtd * np.arctan2(dv1[1], dv1[0])
            else:
                decl_dep_val, rasc_dep_val = np.nan, np.nan

            row_decl_dep.append(decl_dep_val)
            row_rasc_dep.append(rasc_dep_val)

            # Compute arrival declination and RA
            decl_arr_val = 90.0 - rtd * np.arccos(dv2[2] / np.linalg.norm(dv2))
            rasc_arr_val = rtd * np.arctan2(dv2[1], dv2[0])
            row_decl_arr.append(decl_arr_val)
            row_rasc_arr.append(rasc_arr_val)

            # Compute flight time in days and total delta-v
            row_tof.append(j - i)
            row_dvt.append(np.linalg.norm(dv1) + np.linalg.norm(dv2))

        c3_dep.append(row_c3)
        vinf_arr.append(row_vinf)
        decl_dep.append(row_decl_dep)
        decl_arr.append(row_decl_arr)
        rasc_dep.append(row_rasc_dep)
        rasc_arr.append(row_rasc_arr)
        tof.append(row_tof)
        dvtotal.append(row_dvt)

    # Convert lists to arrays for plotting
    con_x, con_y = np.meshgrid(con_x, con_y)
    c3_dep, vinf_arr = np.array(c3_dep), np.array(vinf_arr)
    decl_dep, decl_arr = np.array(decl_dep), np.array(decl_arr)
    rasc_dep, rasc_arr = np.array(rasc_dep), np.array(rasc_arr)
    tof, dvtotal = np.array(tof), np.array(dvtotal)

    # Plot definitions
    plots = [
        ("Launch C3 and v-infinity", c3_dep, c3_levels, vinf_arr, vinf_levels, "C3L (km^2/s^2)", "v-infinity (km/s)"),
        ("Launch C3 and Declination", c3_dep, c3_levels, decl_dep, dla_levels, "C3L (km^2/s^2)", "DLA (deg)"),
        ("Launch C3 and Right Ascension", c3_dep, c3_levels, rasc_dep, rla_levels, "C3L (km^2/s^2)", "RLA (deg)"),
        ("Flight Time and Total Delta-V", tof, tof_levels, dvtotal, dvt_levels, "TOF (days)", "Delta-V (km/s)"),
        ("Arrival v-infinity and Declination", vinf_arr, vinf_levels, decl_arr, dla_levels, "v-infinity (km/s)", "DLA (deg)"),
        ("Arrival v-infinity and Right Ascension", vinf_arr, vinf_levels, rasc_arr, rla_levels, "v-infinity (km/s)", "RLA (deg)")
    ]

    for idx, (title, data1, levels1, data2, levels2, label1, label2) in enumerate(plots):
        plt.figure(figsize=(10, 8))
        c1 = plt.contour(con_x, con_y, data1, levels=levels1, colors='r')
        plt.clabel(c1, inline=True, fontsize=8)
        c2 = plt.contour(con_x, con_y, data2, levels=levels2, colors='b')
        plt.clabel(c2, inline=True, fontsize=8)
        plt.title(title, fontsize=16)
        plt.xlabel("Days relative to Earth departure")
        plt.ylabel("Days relative to arrival")
        plt.legend([label1, label2], loc='upper right')
        plt.grid(True)
        plt.savefig(f"plot_{idx + 1}.png", dpi=300)
        plt.show()

    spice_terminate()

porkchop_plot()