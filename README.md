# Spectral Analysis of the Mesh Laplacian

Exploring the spectral decomposition of the Laplace-Beltrami operator on triangle meshes. This repo implements the core ideas from scratch and demonstrates them on sphere and torus.

## Notebooks

| # | Notebook | What it covers |
|---|----------|----------------|
| 01 | [Laplacian Construction](notebooks/01_laplacian_construction.ipynb) | Building the cotangent and uniform Laplacians, mass matrix, verifying symmetry and null space |
| 02 | [Eigenvector Visualization](notebooks/02_eigenvectors_visualization.ipynb) | Spectral decomposition, eigenvalue spectrum, visualizing eigenfunctions on sphere and torus |
| 03 | [Spectral Embedding](notebooks/03_spectral_embedding.ipynb) | Laplacian eigenmaps, Fiedler vector bisection, 2D/3D spectral coordinates |

## Quick start

```bash
git clone https://github.com/parthchav/spectral-mesh-analysis.git
cd spectral-mesh-analysis
pip install -e .

# Generate sample meshes
python src/generate_meshes.py

# Launch notebooks
jupyter notebook notebooks/
```

## Project structure

```
├── src/
│   ├── laplacian.py         # Laplacian assembly and eigensolvers
│   ├── viz.py               # Visualization helpers (pyvista + matplotlib)
│   └── generate_meshes.py   # Generate sphere, torus, plane meshes
├── notebooks/
│   ├── 01_laplacian_construction.ipynb
│   ├── 02_eigenvectors_visualization.ipynb
│   └── 03_spectral_embedding.ipynb
├── meshes/                  # Generated sample meshes
└── setup.py
```

## Implementation

- The cotangent Laplacian, mass matrix, and OBJ loader are implemented from scratch.
- Eigenvalue problems solved with `scipy.sparse.linalg.eigsh`.
- 3D mesh visualization uses [PyVista](https://docs.pyvista.org/).

## References

- Reuter, Wolter, Peinecke — *Laplace-Beltrami spectra as "Shape-DNA" of surfaces and solids* (2006)
- Levy — *Laplace-Beltrami Eigenfunctions: Towards an Algorithm That "Understands" Geometry* (2006)
- Crane — [*Discrete Differential Geometry: An Applied Introduction*](https://www.cs.cmu.edu/~kmcrane/Projects/DDG/)
- Botsch et al. — *Polygon Mesh Processing*, Ch. 3