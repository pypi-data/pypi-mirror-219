import requests
import base64
import hmac
import hashlib
import time
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

ENDPOINT = "https://gw3.io"
EMPTY_DAG_ROOT = "QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn"


class GW3Client:
    """
    A client for interacting with the Gateway3 API. You need to obtain an
    access key and access secret from https://www.gw3.io
    """

    def __init__(self, access_key: str, access_secret: str):
        """
        Initialize the GW3Client.
        """
        self.access_key = access_key
        self.access_secret = base64.urlsafe_b64decode(access_secret)

    def sign(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        """
        Sign a request with the access secret and update its URL and headers.
        """
        url = urlparse(r.url)
        query = dict(parse_qsl(url.query))
        query["ts"] = str(int(time.time()))
        query = urlencode(query, doseq=True)

        data = f"{r.method}\n{url.path}\n{query}".encode("utf-8")
        mac = hmac.new(self.access_secret, data, hashlib.sha256)
        sign = base64.urlsafe_b64encode(mac.digest())

        r.url = urlunparse(url._replace(query=query))
        r.headers["X-Access-Key"] = self.access_key
        r.headers["X-Access-Signature"] = sign.decode("utf-8")
        return r

    def send_request(self, req: requests.Request):
        prepped = self.sign(req.prepare())
        try:
            response = requests.Session().send(prepped)
            response.raise_for_status()
        except:
            return None

        if response.ok:
            return response

    def get_ipfs(self, hash):
        url = f"{ENDPOINT}/ipfs/{hash}"
        req = requests.Request("GET", url)
        response = self.send_request(req)

        if response != None:
            return response.content
        else:
            raise Exception("get_ipfs API call")

    def get_ipns(self, name):
        url = f"{ENDPOINT}/ipns/{name}"
        req = requests.Request("GET", url)
        response = self.send_request(req)

        if response != None:
            return response.content
        else:
            raise Exception("get_ipns API call")

    def auth_upload(self, size):
        url = f"{ENDPOINT}/ipfs/?size={size}"
        req = requests.Request("POST", url)
        response = self.send_request(req)

        if response != None:
            return response.json()["data"]["url"]
        else:
            raise Exception("auth_upload API call")

    def upload(self, data):
        url = self.auth_upload(len(data))
        response = requests.post(url, data=data)
        if response.ok:
            return response.headers["IPFS-Hash"]
        else:
            raise Exception("upload API call")

    def auth_dag_add(self, root, path, size):
        url = f"{ENDPOINT}/ipfs/{root}{path}?size={size}"
        req = requests.Request("PUT", url)
        response = self.send_request(req)

        if response != None:
            return response.json()["data"]["url"]
        else:
            raise Exception("auth_dag_add API call")

    def dag_add(self, root, path, data):
        url = self.auth_dag_add(root, path, len(data))
        response = requests.put(url, data=data)
        if response.ok:
            return response.headers["IPFS-Hash"]
        else:
            raise Exception("dag_add API call")

    def auth_dag_rm(self, root, path):
        url = f"{ENDPOINT}/ipfs/{root}{path}"
        req = requests.Request("DELETE", url)
        response = self.send_request(req)

        if response != None:
            return response.json()["data"]["url"]
        else:
            raise Exception("auth_dag_rm API call")

    def dag_rm(self, root, path):
        url = self.auth_dag_rm(root, path)
        response = requests.delete(url)
        if response.ok:
            return response.headers["IPFS-Hash"]
        else:
            raise Exception("dag_rm API call")

    def pin(self, cid):
        url = f"{ENDPOINT}/api/v0/pin/add?arg={cid}"
        req = requests.Request("POST", url)
        response = self.send_request(req)

        if response == None:
            raise Exception("pin API call")

    def unpin(self, cid):
        url = f"{ENDPOINT}/api/v0/pin/rm?arg={cid}"
        req = requests.Request("POST", url)
        response = self.send_request(req)

        if response == None:
            raise Exception("unpin API call")

    def create_ipns(self, cid):
        url = f"{ENDPOINT}/api/v0/name/create?arg={cid}"
        req = requests.Request("POST", url)
        response = self.send_request(req)

        if response.ok:
            return response.json()["data"]["name"]
        else:
            raise Exception("create_ipns API call")

    def update_ipns(self, name, cid):
        url = f"{ENDPOINT}/api/v0/name/publish?arg={cid}&key={name}"
        req = requests.Request("POST", url)
        response = self.send_request(req)

        if response.ok:
            return response.json()["msg"]
        else:
            raise Exception("update_ipns API call")