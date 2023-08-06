import logging
import os
import shutil
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import nibabel as nib
import numpy as np
import pyvista as pv
from rich.progress import Progress
from rich.progress import track
import vtk
from vtk.util import numpy_support as nps

from .. import geo
from ..utils import listify


log = logging.getLogger(__name__)


def isosurface(
    data: np.ndarray,
    value: float = 0.5,
    label: Optional[int] = None,
    node_centered: bool = True,
    smooth: bool = True,
    decimation: float = 0.01,
    smooth_iter: int = 30,
    relaxation_factor: float = 0.25,
) -> pv.PolyData:
    """Create an isosurface model using marching cubes.

    Args:
        data (np.ndarray): A 3-D array with scalar or integer data.
        value (float, optional): The value of the surface in `data`. Defaults to 0.5.
        label (Optional[int], optional): Get the isosurface of the `data == label` segmentation. Defaults to None.
        node_centered (bool, optional): Whether the values in the data are sampled in the node-centered style. Defaults to true.
        smooth (bool, optional): whether to apply smoothing. Defaults to True.
        decimation (float, optional): How much to decimate the surface. Defaults to 0.01.
        smooth_iter (int, optional): number of smoothing iterations to run.
        relaxation_factor (float): passed to surface.smooth.

    Returns:
        pv.PolyData: a Pyvista mesh.
    """
    log.debug("making isosurface")
    vol = vtk.vtkStructuredPoints()
    log.debug("set dimensions")
    vol.SetDimensions(*data.shape[:3])
    if node_centered:
        log.debug("node centered origin")
        vol.SetOrigin(0, 0, 0)
    else:
        log.debug("cell-centered origin")
        vol.SetOrigin(0.5, 0.5, 0.5)
    log.debug("spacing")
    vol.SetSpacing(1, 1, 1)

    if label is not None:
        data = (data == label).astype(np.uint8)
    else:
        data = (data > value).astype(np.uint8)

    if np.sum(data) == 0:
        log.warning("No voxels in isosurface")
        return pv.PolyData()

    log.debug("transfer scalars")
    scalars = nps.numpy_to_vtk(data.ravel(order="F"), deep=True)
    vol.GetPointData().SetScalars(scalars)

    log.debug("marching cubes...")
    dmc = vtk.vtkDiscreteMarchingCubes()
    dmc.SetInputData(vol)
    dmc.GenerateValues(1, 1, 1)
    dmc.ComputeGradientsOff()
    dmc.ComputeNormalsOff()
    dmc.Update()

    surface: pv.PolyData = pv.wrap(dmc.GetOutput())

    if not surface.is_all_triangles():
        log.debug("triangulate...")
        surface.triangulate(inplace=True)

    log.debug("decimate")
    surface.decimate_pro(
        decimation,
        feature_angle=60,
        splitting=False,
        preserve_topology=True,
        inplace=True,
    )

    if smooth:
        log.debug("smooth")
        surface.smooth(
            n_iter=smooth_iter,
            relaxation_factor=relaxation_factor,
            feature_angle=70,
            boundary_smoothing=False,
            inplace=True,
        )

    log.debug("normals")
    surface.compute_normals(inplace=True)
    if surface.n_open_edges > 0:
        log.warning(f"surface is not closed, with {surface.n_open_edges} open edges")

    return surface


def voxelize(
    surface: pv.PolyData,
    density: float = 0.2,
    bounds: Optional[List[float]] = None,
) -> Tuple[np.ndarray, geo.FrameTransform]:
    """Voxelize the surface mesh with the given density.

    Args:
        surface (pv.PolyData): The surface.
        density (Union[float, Tuple[float, float, float]]): Either a single float or a
            list of floats giving the size of a voxel in x, y, z.
            (This is really a spacing, but it's misnamed in pyvista.)

    Returns:
        Tuple[np.ndarray, geo.FrameTransform]: The voxelized segmentation of the surface as np.uint8 and the associated world_from_ijk transform.
    """
    density = listify(density, 3)
    voxels = pv.voxelize(surface, density=density, check_surface=False)

    spacing = np.array(density)
    if bounds is None:
        bounds = surface.bounds

    x_min, x_max, y_min, y_max, z_min, z_max = bounds
    size = np.array([(x_max - x_min), (y_max - y_min), (z_max - z_min)])
    if np.any(size) < 0:
        raise ValueError(f"invalid bounds: {bounds}")
    x, y, z = np.ceil(size / spacing).astype(int) + 1
    origin = np.array([x_min, y_min, z_min])
    world_from_ijk = geo.FrameTransform.from_rt(np.diag(spacing), origin)
    ijk_from_world = world_from_ijk.inv

    data = np.zeros((x, y, z), dtype=np.uint8)
    vectors = np.array(voxels.points)
    A_h = np.hstack((vectors, np.ones((vectors.shape[0], 1))))
    transform = np.array(ijk_from_world)
    B = (transform @ A_h.T).T[:, :3]
    B = np.round(B).astype(int)
    data[B[:, 0], B[:, 1], B[:, 2]] = 1

    return data, world_from_ijk


def voxelize_file(path: str, output_path: str, **kwargs):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    surface = pv.read(path)
    try:
        data, world_from_ijk = voxelize(surface, **kwargs)
    except ValueError:
        log.warning(f"skipped {path} due to size error")
        return

    img = nib.Nifti1Image(data, geo.get_data(geo.RAS_from_LPS @ world_from_ijk))
    nib.save(img, output_path)


def voxelize_dir(input_dir: str, output_dir: str, use_cached: bool = True, **kwargs):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    input_len = len(input_dir.parts)
    paths: List[Path] = list(input_dir.glob("*/*.stl"))
    output_path: Path
    with Progress() as progress:
        surfaces_voxelized = progress.add_task("Voxelizing surfaces", total=len(paths))
        for path in paths:
            log.info(f"voxelizing {path}")
            output_path = output_dir / os.path.join(*path.parts[input_len:])
            output_path = output_path.with_suffix(".nii.gz")
            if output_path.exists() and use_cached:
                progress.advance(surfaces_voxelized)
                continue

            voxelize_file(path, output_path, **kwargs)
            progress.advance(surfaces_voxelized)
