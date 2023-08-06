"""
Basic module to calculate the size of grid cells. If a more robust method exists, I'd be happy to implement it here.
"""
import numba
import numpy as np
from optim_esm_tools.analyze.clustering import _distance_bf_coord
import xarray as xr
import typing as ty


def get_area(ds, lat_label):
    # bin_edges = np.unique(ds['lat'].values)
    # bin_edges = np.concatenate([[-90], bin_edges, [90]])
    bin_edges = np.linspace(-90, 90, 800)

    counts_per_bin, _ = np.histogram(ds[lat_label].values, bin_edges)

    bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2

    def _distance(*a):
        import geopy.distance

        return geopy.distance.geodesic(*a).km

    distance_y = np.array(
        [
            _distance([bin_edges[i], 0], [bin_edges[i + 1], 0])
            for i in range(len(bin_edges) - 1)
        ]
    )

    distance_x = np.array(
        [2 * _distance([lat, 0], [lat, 180]) for lat in bin_centers]
    ) / np.maximum(np.array(counts_per_bin), 1)
    area = distance_y * distance_x
    area[counts_per_bin == 0] = 0

    bin_edges[-1] = 91
    idx = np.digitize(ds[lat_label].values, bin_edges)
    overflow = (idx >= len(area)) | (idx < 0)
    idx[overflow] = 0
    # Magical factor that accounts for non-square grid cells
    correction_factor = 0.785238039464103

    area_matrix = area[idx - 1] / correction_factor
    area_matrix[overflow] = 0
    return area_matrix


def calucluate_grid(
    data_set: ty.Union[xr.Dataset, xr.DataArray],
    lat_label: str = 'lat',
    _area_off_percent_threshold: float = 5,
) -> np.ndarray:
    """Calculate the area of each x,y coordinate in the dataset

    Args:
        data_set (ty.Union[xr.Dataset, xr.DataArray]): dataset to calculate grid metric of
        _do_numba (bool, optional): use fast numba calculation. Defaults to True.
        x_label (str, optional): label of x coord. Defaults to 'x'.
        y_label (str, optional): label of y coord. Defaults to 'y'.

    Raises:
        ValueError: If the total area differs siginificantly from the true area of the globe, raise an error

    Returns:
        np.ndarray: _description_
    """
    area = get_area(data_set, lat_label=lat_label)
    if (
        off_by := np.abs(1 - area.sum() / 509600000)
    ) > _area_off_percent_threshold / 100:
        message = f'This estimation leads to an area of {area.sum()} km^2 which is off by {off_by:.1%} (at least {_area_off_percent_threshold}\% of the true value'
        from optim_esm_tools.config import get_logger

        get_logger().error(message)
        # raise ValueError(message)
    to_m2 = 1000**2
    return area * to_m2


@numba.njit
def clip(val, low, high):
    """Simple np.clip like numba function"""
    if high < low:
        raise ValueError
    return min(max(val, low), high)


def _calulate_mesh(lon: np.ndarray, lat: np.ndarray, area: np.ndarray) -> np.ndarray:
    """Calculate the area of each cell based on distance to adjacent cells.
    Averages the distance to left, right up and down:
    If we want to approximate the size of cell "x", we approximate


    . . U . . . .         . . - . . . .
    . L x R . . .  =>     . |-x-| . . .
    . . D . . . .         . . - . . . .
    area_x = (R-L) / 2 * (U-D) / 2

    For any boundary conditions we replace R, L, U or D with x and change
    the normalization appropriately

    Args:
        lon (np.ndarray): mesh of lon values
        lat (np.ndarray): mesh of lat values
        area (np.ndarray): area buffer to fill with values [in km2]!
    """
    len_y, len_x = lon.shape

    for i in range(len_y):
        for j in range(len_x):
            h_multiply = 1 if (i == 0 or i == len_y - 1) else 2
            w_multiply = 1 if (j == 0 or j == len_x - 1) else 2

            coord_up = (
                lon[i][clip(j + 1, 0, len_x - 1)],
                lat[i][clip(j + 1, 0, len_x - 1)],
            )
            coord_down = (
                lon[i][clip(j - 1, 0, len_x - 1)],
                lat[i][clip(j - 1, 0, len_x - 1)],
            )
            coord_left = (
                lon[clip(i + 1, 0, len_y - 1)][j],
                lat[clip(i + 1, 0, len_y - 1)][j],
            )
            coord_right = (
                lon[clip(i - 1, 0, len_y - 1)][j],
                lat[clip(i - 1, 0, len_y - 1)][j],
            )

            h_km = _distance_bf_coord(*coord_up, *coord_down)
            w_km = _distance_bf_coord(*coord_left, *coord_right)

            area[i][j] = h_km * w_km / (h_multiply * w_multiply)


_n_calulate_mesh = numba.njit(_calulate_mesh)
