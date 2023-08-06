import json
from urllib.parse import quote_plus
from typing import cast
import sensenova
from sensenova import api_requestor, util

from sensenova.api_resources.abstract import DeletableAPIResource, ListableAPIResource, CreatableAPIResource, FileableAPIResource, DownloadableAPIResource, UploadableAPIResource


class KnowledgeBase(ListableAPIResource, DeletableAPIResource, CreatableAPIResource, DownloadableAPIResource, UploadableAPIResource, FileableAPIResource):
    OBJECT_NAME = "llm.knowledge-bases"
