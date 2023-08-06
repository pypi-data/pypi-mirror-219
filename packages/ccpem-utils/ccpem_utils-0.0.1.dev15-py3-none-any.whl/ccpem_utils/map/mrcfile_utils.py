from ccpem_utils.map.parse_mrcmapobj import MapObjHandle
from ccpem_utils.map.mrc_map_utils import (
    crop_map_grid,
    pad_map_grid,
    downsample_apix,
    softedge_map,
    realspace_filter_mapobj,
)
from ccpem_utils.map.array_utils import (
    calculate_contour_by_sigma,
    get_contour_mask,
    add_maskarray_softedge,
)
from ccpem_utils.model.coord_grid import calc_atom_coverage_by_res
import mrcfile
from typing import Sequence, Union, Optional
import os


def get_mapobjhandle(map_input):
    # read
    with mrcfile.open(map_input, mode="r", permissive=True) as mrc:
        wrapped_mapobj = MapObjHandle(mrc)
    return wrapped_mapobj


def write_newmapobj(mapobj, map_output):
    with mrcfile.new(map_output, overwrite=True) as mrc:
        mapobj.update_newmap_data_header(mrc)
    mapobj.close()


def crop_mrc_map(
    map_input: str,
    map_output: str = None,
    new_dim: Sequence[int] = None,
    contour: float = None,
    ext: int = 0,
    cubic: bool = False,
    inplace: bool = True,
    mask_map: MapObjHandle = None,
):
    mapobj = get_mapobjhandle(map_input)
    crop_map_grid(
        mapobj,
        new_dim=new_dim,
        contour=contour,
        ext=ext,
        cubic=cubic,
        inplace=inplace,
        mask_map=mask_map,
    )
    if not map_output:
        map_output = os.path.splitext(map_input)[0] + "_cropped.mrc"
    write_newmapobj(mapobj, map_output)


def pad_mrc_map(
    map_input: str,
    ext_dim: Sequence[int],
    map_output: str = None,
    inplace: bool = True,
):
    mapobj = get_mapobjhandle(map_input)
    pad_map_grid(
        mapobj,
        ext_dim=ext_dim,
        inplace=inplace,
    )
    if not map_output:
        map_output = os.path.splitext(map_input)[0] + "_padded.mrc"
    write_newmapobj(mapobj, map_output)


def bin_mrc_map(
    map_input: str,
    new_dim: Union[int, Sequence[int]] = None,
    new_spacing: Union[float, Sequence[float]] = None,
    map_output: str = None,
    inplace: bool = True,
):
    if not new_spacing and not new_dim:
        raise ValueError("Please provide either new_dim or new_spacing")
    mapobj = get_mapobjhandle(map_input)
    if isinstance(new_dim, int):
        max_dim = new_dim
        new_spacing = (
            max(
                mapobj.x_size() * mapobj.apix[0],
                mapobj.y_size() * mapobj.apix[1],
                mapobj.z_size() * mapobj.apix[2],
            )
            / max_dim
        )

    elif new_dim:
        new_spacing = (
            (mapobj.x_size() / new_dim[0]) * mapobj.apix[0],
            (mapobj.y_size() / new_dim[1]) * mapobj.apix[1],
            (mapobj.z_size() / new_dim[2]) * mapobj.apix[2],
        )
    downsample_apix(
        mapobj,
        new_spacing=new_spacing,
        inplace=inplace,
    )
    if not map_output:
        map_output = os.path.splitext(map_input)[0] + "_binned.mrc"
    write_newmapobj(mapobj, map_output)


def calc_mrc_sigma_contour(
    map_input: str,
    sigma_factor: float = 1.5,
):
    with mrcfile.open(map_input, mode="r", permissive=True) as mrc:
        return calculate_contour_by_sigma(arr=mrc.data, sigma_factor=sigma_factor)


def save_contour_mask(
    map_input: str,
    filter_type: Optional[str] = "cosine",
    contour: float = -100,
    map_output: str = None,
    edge: int = 6,
    sigma_factor: float = 1.5,
):
    mapobj = get_mapobjhandle(map_input)
    if contour != -100:
        contour = calculate_contour_by_sigma(arr=mapobj.data, sigma_factor=sigma_factor)
    contour_mask = get_contour_mask(array=mapobj.data, threshold_level=contour)
    if filter_type:
        softedged_mask = add_maskarray_softedge(
            contour_mask, edge=edge, filter_type=filter_type
        )
    else:
        softedged_mask = contour_mask
    mapobj.data = softedged_mask
    if not map_output:
        map_output = (
            os.path.splitext(os.path.basename(map_input))[0] + "_contour_mask.mrc"
        )
    write_newmapobj(mapobj, map_output)


def calc_atom_gaussian_coverage(
    map_input: str,
    res_map: float = 3.0,
    sim_sigma_coeff: float = 0.225,
    sigma_thr: float = 2.5,
):
    with mrcfile.open(map_input, mode="r", permissive=True) as mrc:
        apix = mrc.voxel_size.item()
        return calc_atom_coverage_by_res(
            res_map=res_map,
            sim_sigma_coeff=sim_sigma_coeff,
            sigma_thr=sigma_thr,
            apix=apix,
        )


def add_softedge(
    map_input: str, edgetype: str = "cosine", edge: int = 6, map_output: str = None
):
    mapobj = get_mapobjhandle(map_input)
    softedge_map(mapobj=mapobj, filter_type=edgetype, edge=edge, inplace=True)
    if not map_output:
        map_output = (
            os.path.basename(os.path.splitext(map_input)[0])
            + "_"
            + edgetype
            + "_softmask.mrc"
        )
    write_newmapobj(mapobj, map_output)


def realspace_filter_map(
    map_input: str,
    filter_type: str = "gaussian",
    map_output: str = None,
    kernel_size: int = 5,
    sigma: float = 1,
    truncate: int = 3,
    iter: int = 1,
    edgeonly: bool = False,
    minzero: bool = False,
    normzero_one: bool = False,  # normalise between 0 and 1
    maxone: bool = False,  # for masks with edgeonly
):
    mapobj = get_mapobjhandle(map_input)
    realspace_filter_mapobj(
        mapobj,
        filter_type=filter_type,
        inplace=True,
        kernel_size=kernel_size,
        sigma=sigma,
        truncate=truncate,
        iter=iter,
        edgeonly=edgeonly,
        minzero=minzero,
        normzero_one=normzero_one,
        maxone=maxone,
    )
    if not map_output:
        map_output = (
            os.path.basename(os.path.splitext(map_input)[0])
            + "_"
            + filter_type
            + "_filtered.mrc"
        )
    write_newmapobj(mapobj, map_output)
