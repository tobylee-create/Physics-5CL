import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

angle = np.array([85, 70, 51, 30, 15])
angle_error = np.full(5, 5)

intensity = np.array([1479.45, 666.80, 263.45, 186.75, 134.35])
intensity_error = np.array([3.0, 2.5, 0.6, 1.3, 1.1])

I_0 = 1592.0
background = 22.0

reflectance = (intensity - background) / (I_0 - background)
reflectance_error = intensity_error / (I_0 - background)

fig, ax = plt.subplots(figsize=(7, 4.5))

ax.errorbar(
    angle, reflectance,
    xerr=angle_error,
    yerr=reflectance_error,
    fmt="o",
    capsize=4,
    linestyle="none",
    label="Measured reflectance"
)

# Draw the x- and y-axis lines at zero.
ax.axhline(0, color="black", linewidth=1)
ax.axvline(0, color="black", linewidth=1)

n_block = 1.94294 


def f(x, n_block):
    A = np.deg2rad(x)
    root = np.sqrt(1 - (np.sin(A) / n_block) ** 2)

    numerator = np.cos(A) - n_block * root
    denominator = np.cos(A) + n_block * root

    return (numerator / denominator) ** 2

parameters, covariance = curve_fit(
    f,
    angle,
    reflectance,
    sigma=reflectance_error,
    absolute_sigma=True,
    p0=[1.5],
    bounds=(1.0, np.inf)
)

n_block = parameters[0]
n_error = np.sqrt(covariance[0, 0])

chi_squared = np.sum(
    ((reflectance - f(angle, n_block)) / reflectance_error) ** 2
)
reduced_chi_squared = chi_squared / (len(angle) - 1)

ax.set_xlim(0, 90)
ax.set_ylim(0, 1.00)
ax.set_xlabel("Angle of incidence (degrees)")
ax.set_ylabel("Reflectance $R_s$")
ax.set_title("Reflectance vs. angle of incidence")

x = np.linspace(0, 90, 500)
ax.plot(
    x, f(x, n_block),
    color="red",
    linewidth=2,
    label=fr"Weighted fit: $n_{{\mathrm{{block}}}}={n_block:.3f}$"
)
print(n_block)
print(f"n_block = {n_block:.5f} ± {n_error:.5f}")
print(f"Reduced chi-squared = {reduced_chi_squared:.1f}")

fig.tight_layout()
plt.show()