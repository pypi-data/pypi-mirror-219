from numpy.compat import os_fspath
from numpy.lib.npyio import zipfile_factory
from numpy.lib.format import write_array


def savez_compressed(
    file, data_dict, compress_level=6, allow_pickle=True, pickle_kwargs=None
):
    """like np.savez_compressed but allows for variable compression level"""

    # Import is postponed to here since zipfile depends on gzip, an optional
    # component of the so-called standard library.
    import zipfile

    if not hasattr(file, "write"):
        file = os_fspath(file)
        if not file.endswith(".npz"):
            file = file + ".npz"

    if compress_level is not None:
        compression = zipfile.ZIP_DEFLATED
    else:
        compression = zipfile.ZIP_STORED

    assert (
        isinstance(compress_level, int) and compress_level >= 1 and compress_level <= 9
    )
    zipf = zipfile_factory(
        file, mode="w", compression=compression, compresslevel=compress_level
    )

    for key, val in data_dict.items():
        fname = key + ".npy"
        val = np.asanyarray(val)
        # always force zip64, gh-10776
        with zipf.open(fname, "w", force_zip64=True) as fid:
            write_array(
                fid, val, allow_pickle=allow_pickle, pickle_kwargs=pickle_kwargs
            )

    zipf.close()
