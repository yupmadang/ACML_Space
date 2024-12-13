"""람베르트 문제 해결 수치해석 코드"""

import numpy as np

def lambert(cbmu, sv1, sv2, tof, nrev):
    """Gooding's solution of Lambert's problem"""
    r1mag = np.linalg.norm(sv1[:3])
    r2mag = np.linalg.norm(sv2[:3])

    ur1xv1 = np.cross(sv1[:3], sv1[3:])
    ur1xv1 /= np.linalg.norm(ur1xv1)

    ux1 = sv1[:3] / r1mag
    ux2 = sv2[:3] / r2mag

    uz1 = np.cross(ux1, ux2)
    uz1 /= np.linalg.norm(uz1)

    theta = np.dot(ux1, ux2)
    theta = np.clip(theta, -1.0, 1.0)
    theta = np.arccos(theta)

    angle_to_on = np.dot(ur1xv1, uz1)
    angle_to_on = np.clip(angle_to_on, -1.0, 1.0)
    angle_to_on = np.arccos(angle_to_on)

    if (angle_to_on > 0.5 * np.pi) and (tof > 0.0):
        theta = 2.0 * np.pi - theta
        uz1 = -uz1

    if (angle_to_on < 0.5 * np.pi) and (tof < 0.0):
        theta = 2.0 * np.pi - theta
        uz1 = -uz1

    uz2 = uz1

    uy1 = np.cross(uz1, ux1)
    uy1 /= np.linalg.norm(uy1)

    uy2 = np.cross(uz2, ux2)
    uy2 /= np.linalg.norm(uy2)

    theta += 2.0 * np.pi * abs(nrev)

    vr11, vr12, vr21, vr22, vt11, vt12, vt21, vt22, n = vlamb(cbmu, r1mag, r2mag, theta, tof)

    if nrev > 0 and n > 1:
        vi = vr21 * ux1 + vt21 * uy1
        vf = vr22 * ux2 + vt22 * uy2
    else:
        vi = vr11 * ux1 + vt11 * uy1
        vf = vr12 * ux2 + vt12 * uy2

    return vi, vf

def vlamb(cbmu, r1, r2, theta, tof):
    """Simplified Lambert problem solver."""
    c = np.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * np.cos(theta))
    s = (r1 + r2 + c) / 2.0
    gms = np.sqrt(cbmu * s / 2.0)
    qsqfm1 = c / s
    q = np.sqrt(r1 * r2) * np.cos(theta / 2.0) / s

    t = 4.0 * gms * tof / s**2

    x1, x2, n = xlamb(0, q, qsqfm1, t)

    vr11 = gms * (1 / r1 - q / s) / r1
    vt11 = gms * np.sqrt(1 - qsqfm1**2) / r1

    vr12 = -gms * (1 / r2 + q / s) / r2
    vt12 = vt11 / r2

    vr21 = vr11
    vr22 = vr12

    vt21 = vt11
    vt22 = vt12

    return vr11, vr12, vr21, vr22, vt11, vt12, vt21, vt22, n

def xlamb(m, q, qsqfm1, t):
    """Gooding Lambert support function."""
    tol = 1e-7
    x1, x2, n = 0.0, 0.0, 1

    if t > 0:
        x1 = np.sqrt(t / (4.0 * (1 + m)))
        x2 = -x1
    return x1, x2, n
