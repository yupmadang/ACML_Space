'''태양을 중심 천체로 주변을 윈주운동하는 행성의 위치와 속도 벡터를 도출하여 J2000좌표계로 반환하는 함수
2개의 배열을 pcfunc의 인자로 들어가는 함수로 딱히 건드릴 필요는 없는데... 나머지는 몰루'''

import spiceypy as spice
import numpy as np

def p2000(ncent, ntarg, jdate):
    # Convert Julian date to ephemeris time (TDB)
    et = spice.unitim(jdate, "JDTDB", "ET")

    # Get the state vector (position and velocity) using SPICE function
    state, _ = spice.spkgeo(targ=ntarg, et=et, ref="J2000", obs=ncent)

    # Extract position and velocity vectors
    r = np.array(state[:3])  # Position vector (x, y, z)
    v = np.array(state[3:])  # Velocity vector (vx, vy, vz)

    return r, v