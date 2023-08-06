import json
import requests
from . import sharepoint_file


class SharepointSite:
    """
    SharePointSite(sharepoint_site_url, sharepoint_base_url, header)

    A class used to represent a SharePoint site using the SharePoint REST API v1.
    ...

    Parameters
    ----------
    sharepoint_site_url : str
        The URL of the Sharepoint site
    sharepoint_base_url : str
        The URL of the Sharepoint instance
    header : dict
        The header for requests made to the API containing the Bearer token

    Attributes
    ----------
    name : str
        The user-facing name of the Sharepoint site
    description : str
        The description of the Sharepoint site
    subsites : list
        A list of dicts of Sharepoint subsites
    libraries : list
        A list of strings of Sharepoint document library names

    Methods
    -------
    listdir(path)
        Returns a list of directories in a document library
    mkdir(path)
        Creates a new directory in a document library
    open(path, checkout = False)
        Downloads a file from a document library and returns a SharepointFile object
    get_subsite(site_name)
        Returns a SharepointSite object for a subsite
    """

    def __init__(
        self,
        sharepoint_site_url: str,
        sharepoint_base_url: str,
        header,
    ) -> None:
        self._site_url = sharepoint_site_url
        self._base_url = sharepoint_base_url
        self._header = header

    @property
    def libraries(self):
        api_url = f"{self._site_url}/_api/web/lists?$select=Title,ServerRelativeUrl&$filter=BaseTemplate eq 101 and hidden eq false&$expand=RootFolder"
        request = requests.get(api_url, headers=self._header)
        request = json.loads(request.content)

        request = request["d"]["results"]
        libraries = [library["RootFolder"]["Name"] for library in request]

        return libraries

    def listdir(self, path: str):
        """List all files in a directory on a SharePoint document library.

        Parameters
        ----------
        path : str
            The path of the directory to search, relative to the site as a whole. File paths are UNIX-like.

        Raises
        ------
        FileNotFoundError
            If the document library does not exist or if a nonexistent folder is searched.
        Exception
            If an API error has occured that is not otherwise caught.

        Returns
        -------
        list
            List of files and directories
        """

        path_list = path.split("/")
        path_list = list(filter(None, path_list))

        if path_list[0] not in self.libraries:
            raise FileNotFoundError(f"Document Library {path_list[0]} Not Found.")

        api_url = f"{self._site_url}/_api/web/GetFolderByServerRelativeUrl('{'/'.join(path_list)}')?$expand=Folders,Files"
        request = requests.get(api_url, headers=self._header)
        request = json.loads(request.content)

        if "error" in request:
            error_code = request["error"]["code"]
            if error_code == "-2147024894, System.IO.FileNotFoundException":
                raise FileNotFoundError(request["error"]["message"]["value"])
            else:
                raise Exception(request["error"]["message"]["value"])

        request = request["d"]
        files = request["Files"]["results"]
        folders = request["Folders"]["results"]
        directory_list = []

        for file in files:
            directory_list.append(file["Name"])
        for folder in folders:
            directory_list.append(folder["Name"])

        return directory_list

    def mkdir(self, path: str):
        """Create a new directory on a SharePoint document library.

        Parameters
        ----------
        path : str
            The path of the directory to create, relative to the site as a whole. File paths are UNIX-like.

        Raises
        ------
        FileExistsError
            If the folder already exists.
        FileNotFoundError
            If the document library does not exist or if a subfolder is attempted to be made in a nonexistent folder.
        Exception
            If an API error has occured that is not otherwise caught.
        """

        path_list = path.split("/")
        path_list = list(filter(None, path_list))

        if path_list[0] not in self.libraries:
            raise FileNotFoundError(f"Document Library {path_list[0]} not found.")

        if path_list[-1] in self.listdir("/".join(path_list[:-1])):
            raise FileExistsError(f"Folder {path_list[-1]} exists.")

        api_url = f"{self._site_url}/_api/web/folders"
        payload = json.dumps(
            {
                "__metadata": {"type": "SP.Folder"},
                "ServerRelativeUrl": "/".join(path_list),
            }
        )

        request = requests.post(url=api_url, data=payload, headers=self._header)
        request = json.loads(request.content)

        if "error" in request:
            error_code = request["error"]["code"]
            if error_code == "-2130247139, Microsoft.SharePoint.SPException":
                raise FileNotFoundError(request["error"]["message"]["value"])
            else:
                raise Exception(request["error"]["message"]["value"])

    def open(self, filepath: str, checkout: bool = False, mode: str = "r+b"):
        """Open a file from a SharePoint document library and return a file-like object.

        Parameters
        ----------
        filepath : str
            The path of the file to return, relative to the site as a whole. File paths are UNIX-like.
        checkout : bool
            If True, the file will be checked out of Sharepoint and locked.
        mode : str
            File mode, append mode is not supported. Default is "r+b".

        Returns
        ------
        SharepointFile
            File-like object.
        """
        mode = mode.replace("t", "")
        if mode not in ("w", "w+", "wb", "w+b", "r", "r+", "rb", "r+b"):
            raise ValueError(f"Invalid mode. Supported modes are 'r', 'r+', 'w', 'w+', 'rb', 'wb', 'r+b', 'w+b'.")
        if "a" in mode:
            raise NotImplementedError()
        elif "b" in mode:
            return sharepoint_file.SharepointBytesFile(
                header=self._header,
                sharepoint_site=self._site_url,
                filepath=filepath,
                checkout=checkout,
                mode=mode,
            )
        else:
            return sharepoint_file.SharepointTextFile(
                header=self._header,
                sharepoint_site=self._site_url,
                filepath=filepath,
                checkout=checkout,
                mode=mode,
            )

    @property
    def name(self):
        api_url = f"{self._site_url}/_api/web/title"
        request = json.loads(requests.get(api_url, headers=self._header).content)
        return request["d"]["Title"]

    @property
    def description(self):
        api_url = f"{self._site_url}/_api/web/description"
        request = json.loads(requests.get(api_url, headers=self._header).content)
        return request["d"]["Description"]

    @property
    def subsites(self):
        api_url = f"{self._site_url}/_api/web/webs/?$select=title,Url"
        request = requests.get(api_url, headers=self._header).text
        request = json.loads(request)
        request = request["d"]["results"]
        sites = []
        for x in request:
            site_dict = {
                "Site Name": x["Title"],
                "Site Path": x["Url"],
            }
            sites.append(site_dict)
        return sites

    def get_subsite(self, site_name: str):
        """Grab a subsite.

        Parameters
        ----------
        site_name : str
            The user-facing name of a SharePoint subsite

        Raises
        ------
        KeyError
            If the subsite does not exist.

        Returns
        ------
        SharepointSite
        """

        site_url = next(
            (item for item in self.subsites if item["Site Name"] == site_name), None
        )
        if site_url is None:
            raise KeyError("Site not found.")
        else:
            site_url = site_url["Site Path"]
        return SharepointSite(site_url, self._base_url, self._header)
