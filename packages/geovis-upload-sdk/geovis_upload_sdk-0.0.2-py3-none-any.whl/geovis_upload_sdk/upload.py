import json
import urllib.parse
import urllib.request
import uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import math
from geovis_upload_sdk.sign import hmacSHA256, computeBufferHash


class Uploader:
    def __init__(
            self,
            host: str = "https://cloud.geovisearth.com/",
            appKey: str = "",
            secretKey: str = "",
    ):
        self.host = host
        self.appKey = appKey
        self.secretKey = secretKey

    def upload(self, categoryId, file):
        fileBuffer = file.read()
        file.seek(0, 2)
        file_size = file.tell()
        chunk_size = 1024 * 1024
        if file_size > chunk_size:
            result = self.chunkUpload(categoryId, file, fileBuffer)
            return result
        else:
            result = self.normalUpload(categoryId, file, fileBuffer)
            return result

    def normalUpload(self, categoryId, file, buffer):
        url = self.host
        fileBuffer = buffer
        hashStr = computeBufferHash(fileBuffer)
        encodeFileName = file.filename.encode("utf-8").decode()
        param = "appKey={}&categoryID={}&fileName={}&hash={}".format(self.appKey, categoryId, encodeFileName, hashStr)
        sign = hmacSHA256(param, self.secretKey)
        postUrl = "{}api/filecore/upload?{}&sign={}".format(url, param, urllib.parse.quote(sign))
        file.seek(0, 2)
        file_size = file.tell()
        print('file_size___' + str(file_size))
        headers = {
            'Content-Length': str(file_size)
        }
        request_lib = urllib.request.Request(postUrl, data=fileBuffer, method="POST", headers=headers)
        request_lib.add_header("Content-Type", "application/octet-stream")
        response = urllib.request.urlopen(request_lib)
        if response.getcode() == 200:
            result = response.read()
            decoded_data = json.loads(result)
            return decoded_data
        else:
            print("Request failed with status code:", response.getcode())

    def chunkUpload(self, categoryId, file, fileBuffer):
        uuid4Str = uuid.uuid4()
        uuidStr = str(uuid4Str)
        checkResult = self.checkChunkExist(categoryId, file, fileBuffer, uuidStr)
        if checkResult['Success']:
            uploadChunkItemResult = self.uploadChunkItem(categoryId, file, fileBuffer, checkResult['Data'], uuidStr)
            if uploadChunkItemResult == "success":
                mergeResult = self.mergeChunk(categoryId, file, fileBuffer, uuidStr)
                return mergeResult
        else:
            return checkResult

    def checkChunkExist(self, categoryId, file, fileBuffer, idStr):
        checkChunkExistUrl = self.host + 'api/filecore/checkChunkExist'
        chunk_size = 1024 * 1024  # 1MB
        file.seek(0, 2)
        file_size = file.tell()
        totalChunks = math.ceil(file_size / chunk_size)
        header = {
            "Content-Type": "application/json",
        }
        encodeFileName = file.filename.encode("utf-8").decode()
        hashStr = computeBufferHash(fileBuffer)
        param = "appKey={}&hash={}".format(self.appKey, hashStr)
        sign = hmacSHA256(param, self.secretKey)
        data = {
            'appKey': self.appKey,
            'categoryID': categoryId,
            'fileName': encodeFileName,
            'id': idStr,
            'totalChunks': totalChunks,
        }
        data_json = json.dumps(data)
        postUrl = "{}?{}&sign={}".format(checkChunkExistUrl, param, urllib.parse.quote(sign))
        datas = data_json.encode('utf-8')
        request_lib = urllib.request.Request(postUrl, data=datas, method="POST", headers=header)
        request_lib.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request_lib)
        if response.getcode() == 200:
            result = response.read()
            decoded_data = json.loads(result)
            return decoded_data
        else:
            print("Request failed with status code:", response.getcode())

    def uploadChunkItem(self, categoryId, file, buffer, checkResultData, idStr):
        uploadChunkUrl = self.host + 'api/filecore/uploadChunk'
        chunk_size = 1024 * 1024  # 1MB
        file_size = file.seek(0, 2)
        totalChunks = math.ceil(file_size / chunk_size)
        file.seek(0)
        start = 0
        currentIndex = 1
        end = min(chunk_size, file_size)

        while start < file_size:
            uploadData = file.read(end - start)
            encodeFileName = file.filename.encode("utf-8").decode()
            hashStr = computeBufferHash(buffer)
            param = "appKey={}&hash={}".format(self.appKey, hashStr)
            sign = hmacSHA256(param, self.secretKey)
            postUrl = "{}?{}&sign={}".format(uploadChunkUrl, param, urllib.parse.quote(sign))
            request_body = MultipartEncoder(
                {
                    'totalSize': str(file_size),
                    'fileName': encodeFileName,
                    'id': idStr,
                    'totalChunks': str(totalChunks),
                    'file': (encodeFileName, uploadData),
                    'chunkNumber': str(currentIndex),
                }
            )
            request_header = {
                "Content-Type": request_body.content_type
            }

            response = requests.post(postUrl, data=request_body, headers=request_header, allow_redirects=False)
            response_body_content = response.content
            print(str(currentIndex) + "___"+str(start) + "___" + str(end) + "___" + str(response_body_content))
            start = end
            end = min(start + chunk_size, file_size)
            currentIndex = currentIndex + 1

        return 'success'

    def mergeChunk(self, categoryId, file, buffer, idStr):
        print('categoryId' + categoryId)
        mergeChunkUrl = self.host + 'api/filecore/merge'
        chunk_size = 1024 * 1024  # 1MB
        file.seek(0, 2)
        file_size = file.tell()
        totalChunks = math.ceil(file_size / chunk_size)
        header = {
            "Content-Type": "application/json",
        }
        encodeFileName = file.filename.encode("utf-8").decode()

        hashStr = computeBufferHash(buffer)
        param = "appKey={}&hash={}".format(self.appKey, hashStr)
        sign = hmacSHA256(param, self.secretKey)
        data = {
            'appKey': self.appKey,
            'categoryID': categoryId,
            'fileName': encodeFileName,
            'id': idStr,
            'totalChunks': totalChunks,
        }
        data_json = json.dumps(data)
        postUrl = "{}?{}&sign={}".format(mergeChunkUrl, param, urllib.parse.quote(sign))
        datas = data_json.encode('utf-8')

        request_lib = urllib.request.Request(postUrl, data=datas, method="POST", headers=header)
        request_lib.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request_lib)
        if response.getcode() == 200:
            result = response.read()
            decoded_data = json.loads(result)
            print('mergeChunk' + str(decoded_data))
            return str(decoded_data)
        else:
            print("Request failed with status code:", response.getcode())
            return ''
