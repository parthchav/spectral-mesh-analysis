"""
Generate simple sample meshes for testing.

Uses trimesh for clean, well-formed primitives.
"""

import os
import trimesh


def generate_meshes(out_dir: str = None):
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(__file__), "..", "meshes")
    os.makedirs(out_dir, exist_ok=True)

    # Sphere
    sphere = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    sphere.export(os.path.join(out_dir, "sphere.obj"))
    print(f"  -> {len(sphere.vertices)} vertices, {len(sphere.faces)} faces")

    # Torus
    torus = trimesh.creation.torus(major_radius=1.0, minor_radius=0.4,
                                    major_sections=60, minor_sections=30)
    torus.export(os.path.join(out_dir, "torus.obj"))
    print(f"  -> {len(torus.vertices)} vertices, {len(torus.faces)} faces")

    # Plane (subdivided thin box)
    plane = trimesh.creation.box(extents=[1, 1, 0.001])
    for _ in range(4):
        plane = plane.subdivide()
    plane.export(os.path.join(out_dir, "plane.obj"))
    print(f"  -> {len(plane.vertices)} vertices, {len(plane.faces)} faces")

    print("Done! Meshes saved to meshes/")


if __name__ == "__main__":
    generate_meshes()