import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skfuzzy.control import ControlSystemSimulation


def plot_mf(universe, mf_dict, title):
    fig, ax = plt.subplots()
    for label, mf in mf_dict.items():
        ax.plot(universe, mf, label=label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    return fig


def plot_fuzzy_surface(system, md_range, ps_range, pc_fixed=100):
    X, Y = np.meshgrid(md_range, ps_range)
    Z = np.zeros_like(X, dtype=float)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            sim = ControlSystemSimulation(system)

            sim.input['market_demand'] = X[i, j]
            sim.input['product_stock'] = Y[i, j]
            sim.input['production_capacity'] = pc_fixed

            sim.compute()
            Z[i, j] = sim.output['product_import']

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(
        X, Y, Z,
        cmap='viridis',
        edgecolor='none',
        alpha=0.9
    )

    ax.set_xlabel("Market Demand")
    ax.set_ylabel("Product Stock")
    ax.set_zlabel("Product Import")
    ax.set_title("Fuzzy Inference Surface")

    fig.colorbar(surf, shrink=0.5, aspect=10)

    return fig
