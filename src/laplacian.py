import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh


def load_mesh(path):
    """Load a triangle mesh from an OBJ file. Returns (vertices, faces)."""
    vertices, faces = [], []
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == "v":
                vertices.append([float(x) for x in parts[1:4]])
            elif parts[0] == "f":
                idx = [int(p.split("/")[0]) - 1 for p in parts[1:4]]
                faces.append(idx)
                
    return np.array(vertices, dtype=np.float64), np.array(faces, dtype=np.int64)


def cotangent_weights(V, F):
    """Build the cotangent Laplacian"""
    n = V.shape[0]
    I, J, W = [], [], []

    for face in F:
        for local in range(3):
            i = face[local]
            j = face[(local + 1) % 3]
            k = face[(local + 2) % 3]

            ei = V[i] - V[k]
            ej = V[j] - V[k]

            cos_a = np.dot(ei, ej)
            sin_a = np.linalg.norm(np.cross(ei, ej))
            cot_a = cos_a / max(sin_a, 1e-12)
            w = 0.5 * cot_a

            I.extend([i, j])
            J.extend([j, i])
            W.extend([w, w])

    L = sp.coo_matrix((W, (I, J)), shape=(n, n)).tocsc()
    L = L - sp.diags(L @ np.ones(n))  # diagonal = negative row sum
    return L


def mass_matrix(V, F):
    """Lumped mass matrix (barycentric areas — 1/3 of incident triangle areas)."""
    n = V.shape[0]
    areas = np.zeros(n)

    for face in F:
        i, j, k = face
        tri_area = 0.5 * np.linalg.norm(np.cross(V[j] - V[i], V[k] - V[i]))
        for v in face:
            areas[v] += tri_area / 3.0

    return sp.diags(areas)


def uniform_laplacian(V, F):
    """Graph Laplacian L = D - A."""
    n = V.shape[0]
    I, J = [], []

    for face in F:
        for a in range(3):
            i, j = face[a], face[(a + 1) % 3]
            I.extend([i, j])
            J.extend([j, i])

    A = sp.coo_matrix((np.ones(len(I)), (I, J)), shape=(n, n)).tocsc()
    A = (A > 0).astype(float)
    D = sp.diags(np.array(A.sum(axis=1)).flatten())
    
    return D - A


def spectral_decomposition(L, M, k=20, skip_zero=True):
    """Solve the generalized eigenvalue problem L φ = λ M φ. Returns the k smallest non-trivial eigenvalues and eigenvectors. 
     Uses -L so that eigenvalues come out non-negative.
    """
    num = k + 1 if skip_zero else k

    eigenvalues, eigenvectors = eigsh(-L, k=num, M=M, sigma=0, which="LM")

    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    if skip_zero:
        eigenvalues = eigenvalues[1:]
        eigenvectors = eigenvectors[:, 1:]

    return eigenvalues, eigenvectors