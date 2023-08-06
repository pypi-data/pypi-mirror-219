import logging
from typing import Any, Optional

from modelbit.api import MbApi, ObjectApi
from modelbit.internal.secure_storage import getSecureData, putSecureData
from modelbit.internal.retry import retry
from modelbit.internal.describe import calcHash, describeFile, describeObject
from modelbit.internal.file_stubs import toYaml

logger = logging.getLogger(__name__)


@retry(8, logger)
def uploadRuntimeObject(api: MbApi, objData: bytes, contentHash: str, uxDesc: str) -> None:
  resp = ObjectApi(api).runtimeObjectUploadInfo(contentHash)
  putSecureData(resp, objData, uxDesc)
  return None


@retry(8, logger)
def downloadRuntimeObject(api: MbApi, contentHash: str, desc: str) -> bytes:
  resp = ObjectApi(api).runtimeObjectDownloadUrl(contentHash)
  if not resp or not resp.objectExists:
    raise Exception("Failed to get file URL")
  data = getSecureData(resp, desc)
  if not data:
    raise Exception(f"Failed to download and decrypt")
  return data


def describeAndUploadRuntimeObject(api: MbApi, obj: Optional[Any], objData: bytes, uxDesc: str) -> str:
  contentHash = calcHash(objData)
  if obj is None:
    description = describeFile(objData, 1)
  else:
    description = describeObject(obj, 1)
  yamlObj = toYaml(contentHash, len(objData), description)
  uploadRuntimeObject(api, objData, contentHash, uxDesc)
  return yamlObj
