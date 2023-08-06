# -*- coding: utf-8 -*-
"""
Utilites for loading / creating datasets
"""

import contextlib
import hashlib
import json
import os
import pickle
import shutil
import sys
import tarfile
import time
import urllib
import warnings
import zipfile

import requests
from pkg_resources import resource_filename

RESTRICTED = ["grh4d"]


def _osfify_urls(data, return_restricted=True):
    """
    Formats `data` object with OSF API URL

    Parameters
    ----------
    data : object
        If dict with a `url` key, will format OSF_API with relevant values
    return_restricted : bool, optional
        Whether to return restricted annotations. These will only be accesible
        with a valid OSF token. Default: True

    Returns
    -------
    data : object
        Input data with all `url` dict keys formatted
    """

    OSF_API = "https://files.osf.io/v1/resources/{}/providers/osfstorage/{}"

    if isinstance(data, str) or data is None:
        return data
    elif 'url' in data:
        # if url is None then we this is a malformed entry and we should ignore
        if data['url'] is None:
            return
        # if the url isn't a string assume we're supposed to format it
        elif not isinstance(data['url'], str):
            if data['url'][0] in RESTRICTED and not return_restricted:
                return
            data['url'] = OSF_API.format(*data['url'])

    try:
        for key, value in data.items():
            data[key] = _osfify_urls(value, return_restricted)
    except AttributeError:
        for n, value in enumerate(data):
            data[n] = _osfify_urls(value, return_restricted)
        # drop the invalid entries
        data = [d for d in data if d is not None]

    return data


def get_dataset_info(name, return_restricted=True):
    """
    Returns information for requested dataset `name`

    Parameters
    ----------
    name : str
        Name of dataset
    return_restricted : bool, optional
        Whether to return restricted annotations. These will only be accesible
        with a valid OSF token. Default: True

    Returns
    -------
    dataset : dict or list-of-dict
        Information on requested data
    """

    fn = resource_filename('lytemaps',
                           os.path.join('datasets', 'data', 'osf.json'))
    with open(fn) as src:
        osf_resources = _osfify_urls(json.load(src), return_restricted)

    try:
        resource = osf_resources[name]
    except KeyError:
        raise KeyError("Provided dataset '{}' is not valid. Must be one of: {}"
                       .format(name, sorted(osf_resources.keys())))

    return resource


def get_data_dir(data_dir=None):
    """
    Gets path to neuromaps data directory

    Parameters
    ----------
    data_dir : str, optional
        Path to use as data directory. If not specified, will check for
        environmental variable 'NEUROMAPS_DATA'; if that is not set, will
        use `~/neuromaps-data` instead. Default: None

    Returns
    -------
    data_dir : str
        Path to use as data directory
    """

    if data_dir is None:
        data_dir = os.environ.get('NEUROMAPS_DATA',
                                  os.path.join('~', 'neuromaps-data'))
    data_dir = os.path.expanduser(data_dir)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return data_dir


def _get_token(token=None):
    """
    Returns `token` if provided or set as environmental variable

    Parameters
    ----------
    token : str, optional
        OSF personal access token for accessing restricted annotations. Will
        also check the environmental variable 'NEUROMAPS_OSF_TOKEN' if not
        provided; if that is not set no token will be provided and restricted
        annotations will be inaccessible. Default: None

    Returns
    -------
    token : str
        OSF token
    """

    if token is None:
        token = os.environ.get('NEUROMAPS_OSF_TOKEN', None)

    return token


def _get_session(token=None):
    """
    Returns requests.Session with `token` auth in header if supplied

    Parameters
    ----------
    token : str, optional
        OSF personal access token for accessing restricted annotations. Will
        also check the environmental variable 'NEUROMAPS_OSF_TOKEN' if not
        provided; if that is not set no token will be provided and restricted
        annotations will be inaccessible. Default: None

    Returns
    -------
    session : requests.Session
        Session instance with authentication in header
    """

    session = requests.Session()
    token = _get_token(token)
    if token is not None:
        session.headers['Authorization'] = 'Bearer {}'.format(token)

    return session


# Below we're also including some functions and constants stolen from
# nilearn.datasets.utils that are used in the neuromaps.datasets module.
# Basically, it's everything you need to call nilearn's _fetch_file
# and _fetch_files function.
# These are included here to avoid a dependency on nilearn.
# _REQUESTS_TIMEOUT
# md5_hash
# _format_time
# _md5_sum_file
# _NaiveFTPAdapter
# _chunk_report_
# _chunk_read_
# _fetch_file
_REQUESTS_TIMEOUT = (15.1, 61)


def md5_hash(string):
    """
    Stolen from nilearn.datasets.utils
    """
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def _format_time(t):
    """
    Stolen from nilearn.datasets.utils
    """
    if t > 60:
        return "%4.1fmin" % (t / 60.)
    else:
        return " %5.1fs" % (t)


def _md5_sum_file(path):
    """ Calculates the MD5 sum of a file.
    """
    with open(path, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


class _NaiveFTPAdapter(requests.adapters.BaseAdapter):
    """
    Stolen from nilearn.datasets.utils
    """
    def send(self, request, timeout=None, **kwargs):
        try:
            timeout, _ = timeout
        except Exception:
            pass
        try:
            data = urllib.request.urlopen(request.url, timeout=timeout)
        except Exception as e:
            raise requests.RequestException(e.reason)
        data.release_conn = data.close
        resp = requests.Response()
        resp.url = data.geturl()
        resp.status_code = data.getcode() or 200
        resp.raw = data
        resp.headers = dict(data.info().items())
        return resp

    def close(self):
        pass



def _chunk_report_(bytes_so_far, total_size, initial_size, t0):
    """
    Stolen from nilearn.datasets.utils
    """
    if not total_size:
        sys.stderr.write("\rDownloaded %d of ? bytes." % (bytes_so_far))

    else:
        # Estimate remaining download time
        total_percent = float(bytes_so_far) / total_size

        current_download_size = bytes_so_far - initial_size
        bytes_remaining = total_size - bytes_so_far
        dt = time.time() - t0
        download_rate = current_download_size / max(1e-8, float(dt))
        # Minimum rate of 0.01 bytes/s, to avoid dividing by zero.
        time_remaining = bytes_remaining / max(0.01, download_rate)

        # Trailing whitespace is to erase extra char when message length
        # varies
        sys.stderr.write(
            "\rDownloaded %d of %d bytes (%.1f%%, %s remaining)"
            % (bytes_so_far, total_size, total_percent * 100,
               _format_time(time_remaining)))


def _chunk_read_(response, local_file, chunk_size=8192, report_hook=None,
                 initial_size=0, total_size=None, verbose=1):
    """
    Stolen from nilearn.datasets.utils
    """
    try:
        if total_size is None:
            total_size = response.headers.get('Content-Length').strip()
        total_size = int(total_size) + initial_size
    except Exception as e:
        if verbose > 2:
            print("Warning: total size could not be determined.")
            if verbose > 3:
                print("Full stack trace: %s" % e)
        total_size = None
    bytes_so_far = initial_size

    t0 = time_last_display = time.time()
    for chunk in response.iter_content(chunk_size):
        bytes_so_far += len(chunk)
        time_last_read = time.time()
        if (report_hook and
                # Refresh report every second or when download is
                # finished.
                (time_last_read > time_last_display + 1. or not chunk)):
            _chunk_report_(bytes_so_far,
                           total_size, initial_size, t0)
            time_last_display = time_last_read
        if chunk:
            local_file.write(chunk)
        else:
            break


def _fetch_file(url, data_dir, resume=True, overwrite=False,
                md5sum=None, username=None, password=None,
                verbose=1, session=None):
    """
    Stolen from nilearn.datasets.utils
    """
    if session is None:
        with requests.Session() as session:
            session.mount("ftp:", _NaiveFTPAdapter())
            return _fetch_file(
                url, data_dir, resume=resume, overwrite=overwrite,
                md5sum=md5sum, username=username, password=password,
                verbose=verbose, session=session)
    # Determine data path
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Determine filename using URL
    parse = urllib.parse.urlparse(url)
    file_name = os.path.basename(parse.path)
    if file_name == '':
        file_name = md5_hash(parse.path)

    temp_file_name = file_name + ".part"
    full_name = os.path.join(data_dir, file_name)
    temp_full_name = os.path.join(data_dir, temp_file_name)
    if os.path.exists(full_name):
        if overwrite:
            os.remove(full_name)
        else:
            return full_name
    if os.path.exists(temp_full_name):
        if overwrite:
            os.remove(temp_full_name)
    t0 = time.time()
    local_file = None
    initial_size = 0

    try:
        # Download data
        headers = {}
        auth = None
        if username is not None and password is not None:
            if not url.startswith('https'):
                raise ValueError(
                    'Authentication was requested on a non  secured URL (%s).'
                    'Request has been blocked for security reasons.' % url)
            auth = (username, password)
        if verbose > 0:
            displayed_url = url.split('?')[0] if verbose == 1 else url
            print('Downloading data from %s ...' % displayed_url)
        if resume and os.path.exists(temp_full_name):
            # Download has been interrupted, we try to resume it.
            local_file_size = os.path.getsize(temp_full_name)
            # If the file exists, then only download the remainder
            headers["Range"] = "bytes={}-".format(local_file_size)
            try:
                req = requests.Request(
                    method="GET", url=url, headers=headers, auth=auth)
                prepped = session.prepare_request(req)
                with session.send(prepped, stream=True,
                                  timeout=_REQUESTS_TIMEOUT) as resp:
                    resp.raise_for_status()
                    content_range = resp.headers.get('Content-Range')
                    if (content_range is None or not content_range.startswith(
                            'bytes {}-'.format(local_file_size))):
                        raise IOError('Server does not support resuming')
                    initial_size = local_file_size
                    with open(local_file, "ab") as fh:
                        _chunk_read_(
                            resp, fh, report_hook=(verbose > 0),
                            initial_size=initial_size, verbose=verbose)
            except Exception:
                if verbose > 0:
                    print('Resuming failed, try to download the whole file.')
                return _fetch_file(
                    url, data_dir, resume=False, overwrite=overwrite,
                    md5sum=md5sum, username=username, password=password,
                    verbose=verbose, session=session)
        else:
            req = requests.Request(
                method="GET", url=url, headers=headers, auth=auth)
            prepped = session.prepare_request(req)
            with session.send(
                    prepped, stream=True, timeout=_REQUESTS_TIMEOUT) as resp:
                resp.raise_for_status()
                with open(temp_full_name, "wb") as fh:
                    _chunk_read_(resp, fh, report_hook=(verbose > 0),
                                 initial_size=initial_size, verbose=verbose)
        shutil.move(temp_full_name, full_name)
        dt = time.time() - t0
        if verbose > 0:
            # Complete the reporting hook
            sys.stderr.write(' ...done. ({0:.0f} seconds, {1:.0f} min)\n'
                             .format(dt, dt // 60))
    except (requests.RequestException):
        sys.stderr.write("Error while fetching file %s; dataset "
                         "fetching aborted." % (file_name))
        raise
    if md5sum is not None:
        if (_md5_sum_file(full_name) != md5sum):
            raise ValueError("File %s checksum verification has failed."
                             " Dataset fetching aborted." % local_file)
    return


def _is_within_directory(directory, target):
    """
    Stolen from nilearn.datasets.utils
    """
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    prefix = os.path.commonprefix([abs_directory, abs_target])

    return prefix == abs_directory


def _safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    """
    Stolen from nilearn.datasets.utils
    """
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not _is_within_directory(path, member_path):
            raise Exception("Attempted Path Traversal in Tar File")

    tar.extractall(path, members, numeric_owner=numeric_owner)


def _uncompress_file(file_, delete_archive=True, verbose=1):
    """Uncompress files contained in a data_set.
    Parameters
    ----------
    file_ : string
        Path of file to be uncompressed.
    delete_archive : bool, optional
        Whether or not to delete archive once it is uncompressed.
        Default=True.
    %(verbose)s
    Notes
    -----
    This handles zip, tar, gzip and bzip files only.
    """
    if verbose > 0:
        sys.stderr.write('Extracting data from %s...' % file_)
    data_dir = os.path.dirname(file_)
    # We first try to see if it is a zip file
    try:
        filename, ext = os.path.splitext(file_)
        with open(file_, "rb") as fd:
            header = fd.read(4)
        processed = False
        if zipfile.is_zipfile(file_):
            z = zipfile.ZipFile(file_)
            z.extractall(path=data_dir)
            z.close()
            if delete_archive:
                os.remove(file_)
            file_ = filename
            processed = True
        elif ext == '.gz' or header.startswith(b'\x1f\x8b'):
            import gzip
            if ext == '.tgz':
                filename = filename + '.tar'
            elif ext == '':
                # We rely on the assumption that gzip files have an extension
                shutil.move(file_, file_ + '.gz')
                file_ = file_ + '.gz'
            with gzip.open(file_) as gz:
                with open(filename, 'wb') as out:
                    shutil.copyfileobj(gz, out, 8192)
            # If file is .tar.gz, this will be handled in the next case
            if delete_archive:
                os.remove(file_)
            file_ = filename
            processed = True
        if os.path.isfile(file_) and tarfile.is_tarfile(file_):
            with contextlib.closing(tarfile.open(file_, "r")) as tar:
                _safe_extract(tar, path=data_dir)
            if delete_archive:
                os.remove(file_)
            processed = True
        if not processed:
            raise IOError(
                    "[Uncompress] unknown archive file format: %s" % file_)

        if verbose > 0:
            sys.stderr.write('.. done.\n')
    except Exception as e:
        if verbose > 0:
            print('Error uncompressing file: %s' % e)
        raise


def movetree(src, dst):
    """
    Stolen from nilearn.datasets.utils
    """
    names = os.listdir(src)

    # Create destination dir if it does not exist
    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []

    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname) and os.path.isdir(dstname):
                movetree(srcname, dstname)
                os.rmdir(srcname)
            else:
                shutil.move(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive movetree so that we can
        # continue with other files
        except Exception as err:
            errors.extend(err.args[0])
    if errors:
        raise Exception(errors)


def _fetch_files(data_dir, files, resume=True, verbose=1, session=None):
    """
    Stolen from nilearn.datasets.utils
    """
    if session is None:
        with requests.Session() as session:
            session.mount("ftp:", _NaiveFTPAdapter())
            return _fetch_files(
                data_dir, files, resume=resume,
                verbose=verbose, session=session)
    # There are two working directories here:
    # - data_dir is the destination directory of the dataset
    # - temp_dir is a temporary directory dedicated to this fetching call. All
    #   files that must be downloaded will be in this directory. If a corrupted
    #   file is found, or a file is missing, this working directory will be
    #   deleted.
    files = list(files)
    files_pickle = pickle.dumps([(file_, url) for file_, url, _ in files])
    files_md5 = hashlib.md5(files_pickle).hexdigest()
    temp_dir = os.path.join(data_dir, files_md5)

    # Create destination dir
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Abortion flag, in case of error
    abort = None

    files_ = []
    for file_, url, opts in files:
        # 3 possibilities:
        # - the file exists in data_dir, nothing to do.
        # - the file does not exists: we download it in temp_dir
        # - the file exists in temp_dir: this can happen if an archive has been
        #   downloaded. There is nothing to do

        # Target file in the data_dir
        target_file = os.path.join(data_dir, file_)
        # Target file in temp dir
        temp_target_file = os.path.join(temp_dir, file_)
        # Whether to keep existing files
        overwrite = opts.get('overwrite', False)
        if (abort is None and
                (overwrite or (not os.path.exists(target_file) and
                not os.path.exists(temp_target_file)))):

            # We may be in a global read-only repository. If so, we cannot
            # download files.
            if not os.access(data_dir, os.W_OK):
                raise ValueError('Dataset files are missing but dataset'
                                 ' repository is read-only. Contact your data'
                                 ' administrator to solve the problem')

            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            md5sum = opts.get('md5sum', None)

            dl_file = _fetch_file(url, temp_dir, resume=resume,
                                  verbose=verbose, md5sum=md5sum,
                                  username=opts.get('username', None),
                                  password=opts.get('password', None),
                                  session=session, overwrite=overwrite)
            if 'move' in opts:
                # XXX: here, move is supposed to be a dir, it can be a name
                move = os.path.join(temp_dir, opts['move'])
                move_dir = os.path.dirname(move)
                if not os.path.exists(move_dir):
                    os.makedirs(move_dir)
                shutil.move(dl_file, move)
                dl_file = move
            if 'uncompress' in opts:
                try:
                    _uncompress_file(dl_file, verbose=verbose)
                except Exception as e:
                    abort = str(e)

        if (abort is None and not os.path.exists(target_file) and not
                os.path.exists(temp_target_file)):
            warnings.warn('An error occurred while fetching %s' % file_)
            abort = ("Dataset has been downloaded but requested file was "
                     "not provided:\nURL: %s\n"
                     "Target file: %s\nDownloaded: %s" %
                     (url, target_file, dl_file))
        if abort is not None:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise IOError('Fetching aborted: ' + abort)
        files_.append(target_file)
    # If needed, move files from temps directory to final directory.
    if os.path.exists(temp_dir):
        # XXX We could only moved the files requested
        # XXX Movetree can go wrong
        movetree(temp_dir, data_dir)
        shutil.rmtree(temp_dir)
    return files_


class Bunch(dict):
    """
    Stolen from sklearn.utils.Bunch
    """

    def __init__(self, **kwargs):
        super().__init__(kwargs)

        # Map from deprecated key to warning message
        self.__dict__["_deprecated_key_to_warnings"] = {}

    def __getitem__(self, key):
        if key in self.__dict__.get("_deprecated_key_to_warnings", {}):
            warnings.warn(
                self._deprecated_key_to_warnings[key],
                FutureWarning,
            )
        return super().__getitem__(key)

    def _set_deprecated(
        self,
        value,
        *,
        new_key,
        deprecated_key,
        warning_message,
    ):
        """Set key in dictionary to be deprecated with its warning message."""
        self.__dict__[
            "_deprecated_key_to_warnings"
        ][deprecated_key] = warning_message
        self[new_key] = self[deprecated_key] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setstate__(self, state):
        # Bunch pickles generated with scikit-learn 0.16.* have an non
        # empty __dict__. This causes a surprising behaviour when
        # loading these pickles scikit-learn 0.17: reading bunch.key
        # uses __dict__ but assigning to bunch.key use __setattr__ and
        # only changes bunch['key']. More details can be found at:
        # https://github.com/scikit-learn/scikit-learn/issues/6196.
        # Overriding __setstate__ to be a noop has the effect of
        # ignoring the pickled __dict__
        pass
