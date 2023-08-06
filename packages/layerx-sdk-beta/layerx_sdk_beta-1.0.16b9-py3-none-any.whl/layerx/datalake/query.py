import datetime
from typing import TYPE_CHECKING
from .logger import get_debug_logger

if TYPE_CHECKING:
    from . import DatalakeClient

annotation_logger = get_debug_logger('Query')


class Query:
    def __init__(self, client: "DatalakeClient"):
        self._client = client


    def get_selection_id(self, collection_id, query, filter, object_type, object_list, is_all_selected):
        if object_list == None:
            object_list = []
        filterData = {
            "contentType": object_type,
            "filterBy": [],
            "date": None
        }

        if filter != None:
            if ("filterBy" in filter and len(filter["filterBy"]) > 0):
                filterData["filterBy"] = filter["filterBy"]
            else:
                filterData["filterBy"] = []

            if ("date" in filter):
                filterData["date"] = filter["date"]
        
        #"metadata.Tags=2.1"
        payload = {
            "isAllSelected": is_all_selected,
            # "projectType": 3,
            "objectIdList": object_list,
            "filterData": filterData,
            "query": query,
            "collectionId": collection_id
        }
        print(payload)
        response = self._client.datalake_interface.get_selection_id(payload)
        return response