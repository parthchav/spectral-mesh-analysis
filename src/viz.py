"""
pip install pyvista[jupyter]
"""

import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt


def mesh_to_pv(V, F):
    """Convert (V, F) arrays to a pyvista PolyData mesh."""
    faces = np.column_stack([np.full(len(F), 3), F]).ravel()
    return pv.PolyData(V, faces)


def plot_eigenvectors(V, F, eigenvectors, eigenvalues, num=6, cmap="RdBu"):
    """Plot eigenvectors as scalar fields on the mesh."""
    num = min(num, eigenvectors.shape[1])
    cols = 3
    rows = (num + cols - 1) // cols

    pl = pv.Plotter(shape=(rows, cols), window_size=(400 * cols, 400 * rows),
                    off_screen=False)

    for idx in range(num):
        pl.subplot(idx // cols, idx % cols)
        mesh = mesh_to_pv(V, F)
        mesh[f"eigvec"] = eigenvectors[:, idx]
        pl.add_mesh(mesh, scalars="eigvec", cmap=cmap,
                    show_scalar_bar=False, smooth_shading=True)
        pl.add_title(f"e{idx+1}  (l = {eigenvalues[idx]:.2f})", font_size=8)

    pl.link_views()
    pl.show()


def plot_eigenvalue_spectrum(eigenvalues, title="Eigenvalue Spectrum"):
    """Simple bar + line chart of eigenvalues."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    k = len(eigenvalues)

    ax1.bar(range(k), eigenvalues, color="steelblue", alpha=0.8)
    ax1.set(xlabel="index k", ylabel="l_k", title=title)

    ax2.plot(range(k), eigenvalues, "o-", markersize=3)
    ax2.set(xlabel="k", ylabel="l_k", title="Eigenvalue Growth")

    plt.tight_layout()
    plt.show()


def plot_spectral_embedding(eigenvectors, eigenvalues, dims=(0, 1),
                            title="Spectral Embedding", color=None):
    """2D scatter of spectral embedding coordinates."""
    fig, ax = plt.subplots(figsize=(7, 6))
    x, y = eigenvectors[:, dims[0]], eigenvectors[:, dims[1]]
    if color is None:
        color = np.arange(len(x))

    sc = ax.scatter(x, y, c=color, cmap="viridis", s=2, alpha=0.8)
    ax.set(xlabel=f"e{dims[0]+1} (l={eigenvalues[dims[0]]:.2f})",
           ylabel=f"e{dims[1]+1} (l={eigenvalues[dims[1]]:.2f})",
           title=title)
    ax.set_aspect("equal")
    fig.colorbar(sc, ax=ax, shrink=0.7, label="vertex index")
    plt.tight_layout()
    plt.show()