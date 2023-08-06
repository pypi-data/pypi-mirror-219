import requests
import os

from typing import Optional, get_args
from hashlib import md5
from tqdm import tqdm

from .data_models import Endpoints, JarCat, JarType, JarDetails, FullJarDetails, allowed
from .errors import ServerJarsAPIError, MD5HashMismatch


class ServerJarsAPI:
    """Underlying request interface for interacting with the api."""

    _base_url = f'https://serverjars.com/api'
    _check_hashes = True

    @staticmethod
    def _match(category: JarCat) -> JarType:
        match = next((x for x in allowed if category in allowed[x]), None)
        if not match:
            raise TypeError(f'Invalid jar category"{category}"! Choose from {get_args(JarCat)}')

        return match

    def _get(self,
             url: Endpoints,
             jar_type: Optional[JarType] = None,
             jar_category: Optional[JarCat] = None,
             limit: Optional[int] = None,
             version: Optional[str] = None,
             backfill=False
             ):
        """Request url builder and response parser for all endpoints except jar downloading."""

        aux = ''

        # full path provided
        if jar_type and jar_category:
            aux = f'{jar_type}/{jar_category}'

        # autocomplete path
        elif jar_category and not jar_type:
            jar_type = self._match(jar_category)
            aux = f'{jar_type}/{jar_category}'

        # just type
        elif jar_type:
            aux = f'{jar_type}'

        if aux:
            # based on the current api layout, should only ever be either or.
            if limit:
                aux += f'/{limit}'
            elif version:
                aux += f'/{version}'
        full_url = f'{self._base_url}/{url}/{aux}'
        resp = requests.get(full_url)

        # request error handling
        if resp.status_code != 200:
            raise ServerJarsAPIError({'status_code': resp.status_code, 'endpoint': full_url})
        data = resp.json()

        # api provides a double-wrapped response
        data = data.get('response', data)

        # assemble additional information for saturation
        if backfill:
            # if version wasn't given, response will be latest by default
            ff_version = data.get('version')
            latest = not version
            # version must be checked otherwise
            if not latest:
                latest_version = self._get(url, jar_type, jar_category).get('version')
                latest = latest_version == ff_version

            # update with extended data
            data.update({
                'jar_type': jar_type,
                'jar_category': jar_category,
                'latest': latest,
                'href': f'{self._base_url}/fetchJar/{jar_type}/{jar_category}/{ff_version}'
            })
        return data

    def _download(self, file_info: FullJarDetails) -> bytes:
        """Request builder, response parser, and hash checker for jar download endpoint."""
        # prepare request
        resp = requests.get(file_info.href, stream=True)
        # set progress params
        total = int(resp.headers.get('content-length', 0))
        chunk_size = (32 * 1024)
        progress = tqdm(total=total, unit='B', unit_scale=True, unit_divisor=1024)
        file_stream = bytes()

        # iter through chunks as they arrive and output progress
        for fragment in resp.iter_content(chunk_size):
            progress.update(len(fragment))
            file_stream += fragment
        if resp.status_code != 200:
            raise Exception(f'Download failed with status code {resp.status_code} for url {resp.url}.')

        # check download against expected hash.
        if self._check_hashes:
            calculated = md5(file_stream).hexdigest()
            if calculated != file_info.md5:
                raise MD5HashMismatch(f'Expected: {file_info.md5} Calculated: {calculated}')

        return file_stream


class ServerJars(ServerJarsAPI):
    """Wrapper class with included methods for all ServerJarsAPI endpoints (the redundant fetchLatest
    endpoint is folded into fetchDetails with version path left blank), with additional inbuilt
    convenience methods and custom return dataclasses"""
    def __init__(self, *voided_args, force_unsafe_ignore_hash=False):
        if voided_args:
            raise TypeError(f'Unexpected positional argument: {voided_args}')

        # I'll advised override possible, but only accepted as a keyword argument to safeguard.
        self._check_hashes = not force_unsafe_ignore_hash

    def jar_types(self,
                  single_type: Optional[JarType] = None,
                  flatten=False
                  ) -> dict[JarType, list[JarCat]] | list[JarCat]:
        """
        Method for interfacing with the /fetchTypes/{type} endpoint.

        Parameters
        ----------
        single_type : str
            specify a specific jar type to get categories for.
            Example: single_type = 'servers' -> ['paper', 'purpur', 'sponge']
        flatten : bool
            parse the nested type/categories response into a flat list of categories (default = False)
        Returns
        -------
        dict | list
            Available jars categories for each type, unless specified, then only one type.
        """

        data = self._get('fetchTypes', jar_type=single_type)
        if flatten:
            return [v for x in data for v in data.get(x, [])]
        return data

    def jar_details(self,
                    jar_category: JarCat,
                    version: Optional[str] = None,
                    raw=False,
                    backfill=False
                    ) -> JarDetails | FullJarDetails | dict:
        """
        Get the details of a single jar. Method for /fetchDetails and /fetchLatest endpoints (leave version blank for
        latest).
        Parameters
        ----------
        jar_category : str
            jar subtype to get info for.
        version : str
            search for details on a specific version, None retrieves latest. (default = None)
        raw : bool
            Prevent parsing of API response into a dataclass. (default = False)
        backfill : bool
            Append fields related to the underlying request, including the jar category, jar type, jar version, and href
            of the jar for subsequent requests. Compatible with raw response parameter. (default = False)
        Returns
        -------
        JarDetails | FullJarDetails | dict
            Information for the requested jar file.
        """

        data = self._get('fetchDetails', jar_category=jar_category, version=version, backfill=backfill)
        if raw:
            return data
        elif backfill:
            return FullJarDetails(**data)
        else:
            return JarDetails(**data)

    def multi_jar_details(self, jar_category: JarCat, limit: Optional[int | None] = 5, raw=False
                          ) -> list[JarDetails | dict]:
        """
        Request details on all jars for a specified category.
        Method for the /api/fetchAll/{type}/{category}/{max} endpoint. Endpoint's jar type is autofilled for the
        specified category.

        Parameters
        ----------
        jar_category : JarCat
            Specify jar category to fetch details for. ie 'paper'
        limit : int
            Max length for response, set to None for all results. (default = 5)
        raw : bool
            Disables the conversion of results to their dataclass and returns them as standard dicts.
        Returns
        -------
        list :
            Collection of details for available jars
        """
        data = self._get('fetchAll', jar_category=jar_category, limit=limit)

        return [JarDetails(**v) for v in data] if not raw else data

    def versions(self, jar_category: JarCat) -> list[str]:
        """Get a list of available jar versions for a specified category. (Parses a multi_jar_details call
        under the hood)"""
        data = self.multi_jar_details(jar_category, limit=None)
        return [x.version for x in data]

    def stream_jar(self, jar_category: JarCat, version: str | None = None) -> bytes:
        """Download a specified jar and ensure md5 hash is correct, but return the file as a byte object instead of
        writing to a file."""
        jar_info = self.jar_details(jar_category, version, backfill=True)
        return self._download(jar_info)

    def download_jar(self,
                     jar_category: JarCat,
                     location: Optional[str] = '.',
                     version: Optional[str] = None,
                     save_as: Optional[str] = None
                     ) -> FullJarDetails:
        """
        Download a specified jar, check the hash, and save it to the given location.

        Parameters
        ----------
        jar_category : JarCat
            Specify jar category to download. ie 'paper'
        location : str
            Path of the directory you wish the file to be downloaded to.
        version : str
            None for latest, otherwise the desired version of specified category to download.
        save_as : str
            If provided, the downloaded jar file will be named this. ie location/{save_as}.jar
        Returns
        -------

        """

        jar_info = self.jar_details(jar_category, version, backfill=True)

        # if save_as filename provided, ".jar" is appended if needed
        save_as = save_as if not save_as or '.jar' in save_as else save_as + '.jar'

        filename = jar_info.file if not save_as else save_as
        file_path = f"{location}/{filename}"

        # save time by raising before download
        if os.path.isfile(file_path):
            raise FileExistsError(f'Jar file "{jar_info.file}" already exists at location "{location}"!')

        data = self._download(jar_info)
        with open(file_path, mode='wb') as f:
            f.write(data)

        jar_info.file = os.path.abspath(file_path)

        return jar_info
