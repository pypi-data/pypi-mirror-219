from typing import Optional
from silx.io.url import DataUrl
from silx.io.spech5 import SpecFile


def build_spec_data_url(
    file_path: str,
    col_name: str,
    scan_title: Optional[str] = None,
    data_slice: Optional[slice] = None,
):
    if scan_title is None:
        scan_title = SpecFile(file_path)[0].scan_header_dict["S"]
    if "/" in scan_title:
        raise ValueError("scan_title cannot contain '/'")
    return DataUrl(
        file_path=file_path,
        data_path=f"{scan_title}/{col_name}",
        data_slice=data_slice,
        scheme="spec",
    )


def split_spec_url_elmts(url: DataUrl) -> tuple:
    """
    convert an url to (file_path, scan_title, col_name, data_slice)
    """
    if not isinstance(url, DataUrl):
        raise TypeError
    if url.data_path() is None:
        scan_title = None
        col_name = None
    elif "/" in url.data_path():
        scan_title = url.data_path().split("/")[0]
        col_name = "/".join(url.data_path().split("/")[1:])
    else:
        raise ValueError("unrecognized data_path")
    return {
        "file_path": url.file_path(),
        "scan_title": scan_title,
        "col_name": col_name,
        "data_slice": url.data_slice(),
    }
