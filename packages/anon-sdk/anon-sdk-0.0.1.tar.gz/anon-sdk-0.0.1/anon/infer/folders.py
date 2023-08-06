from typing import Any, Dict, List, Optional
from enum import Enum
from anon.exceptions import InvalidIdError
from anon.basemodel import AnonBase
import anon.infer.videos
import anon.infer.images
import anon.infer.folders
import anon.client
import anon
from pydantic import conint, Field

class FolderType(Enum):
    VIDEO = "VIDEO"
    GALLERY = "IMAGE"


class RootFolder(AnonBase):
    type: Optional[FolderType]
    folder_id: Optional[str]
    owner_id: str
    # project_id: str

    @property
    def folders(self):
        search_params = {"ownerId": self.owner_id}
        if self.folder_id is not None:
            search_params["parentFolderId"] = self.folder_id
        if self.type is not None:
            search_params["type"] = self.type.value
        return anon.infer.videos.Video.from_search_params(
            search_params, client=self.client
        )

    @property
    def videos(self) -> List["anon.videos.Video"]:
        search_params = {
            "ownerId": self.owner_id,
            "limit": "-1",
        }
        if self.folder_id is not None:
            search_params["parentFolderId"] = self.folder_id
        return anon.infer.videos.Video.from_search_params(
            search_params, client=self.client
        )

    @property
    def images(self) -> List["anon.infer.images.Image"]:
        search_params = {
            "ownerId": self.owner_id,
            "limit": "-1",
        }
        if self.folder_id is not None:
            search_params["parentFolderId"] = self.folder_id
        return anon.infer.images.Image.from_search_params(
            search_params, self.client
        )


class Folder(RootFolder):
    description: Optional[str]
    name: str
    parent_folder_id: Optional[str]
    ancestor_folder_ids: List[str]

    @classmethod
    def create(
        cls,
        name: str,
        # project_id: str,
        owner_id:str,
        client: "anon.client.BaseClient",
        type: FolderType = FolderType.VIDEO,
        description: str = "",
        parent_folder_id: str = "user",
    ):
        request_data = {
            # "projectId": project_id,
            "owner_id":owner_id,
            "name": name,
            "type": type.value,
            "parentFolderId": parent_folder_id,
            "description": description,
            "restriction": "false"
        }
        resp = client.post("/folders", request_data)
        return cls(**resp.json()["data"])

    @classmethod
    def from_search_params(
        cls, params: Dict[str, Any], client: "anon.client.BaseClient"
    ) -> List["Folder"]:
        resp = client.get("/folders", params)
        folders = resp.json()["data"]["folders"]
        folders = [cls(**folder, client=client) for folder in folders]
        return folders  # type: ignore

    @classmethod
    def from_owner_id(
        cls, owner_id: str, client: "anon.client.BaseClient"
    ) -> List["Folder"]:
        folders = cls.from_search_params({"ownerId": owner_id}, client)
        return folders

    @classmethod
    def from_folder_id(
        cls, folder_id: str, client: "anon.client.BaseClient"
    ) -> "Folder":
        folders = cls.from_search_params({"folderId": folder_id}, client)
        if not folders:
            raise InvalidIdError(f"No Folder found with folderId: {folder_id}")
        return folders[0]
    
   

