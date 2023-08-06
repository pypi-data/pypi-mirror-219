""" decrypts the values for a python dictionary (usually a secrets dict) """
import base64
from cryptography.fernet import Fernet
from kubernetes import client, config

class DecryptDicts:
    """ must call one of readInClusterKey, readKeyFromFile, or setKey before decrypting """
    # key = None
    def __init__(self):
        self._key = None

    def set_key(self, key):
        """ provides a key as a string """
        self._key = Fernet(bytes(key, 'utf-8'))

    def read_key_from_file(self, path):
        """ reads the key from a text file """
        with open(path, "r", encoding='utf-8') as fstr:
            refkey = ''.join(fstr.readlines())
            refkeybyt = bytes(refkey, 'utf-8')
        fstr.close()
        self._key = Fernet(refkeybyt)

    def read_key_from_cluster(self):
        """ reads the key from _the outside_ kubernetes cluster; requires a valid kubectl config """
        config.load_kube_config()
        v_one = client.CoreV1Api()
        key = base64.b64decode(v_one.read_namespaced_secret("py-secret-key", \
                                                         "default").data["key"]).decode('utf-8')
        self._key = Fernet(bytes(key, 'utf-8'))

    def read_in_cluster_key(self):
        """ reads the key from _inside of_ the kubernetes cluster """
        config.incluster_config.load_incluster_config()
        v_one = client.CoreV1Api()
        key = base64.b64decode(v_one.read_namespaced_secret("py-secret-key", \
                                                         "default").data["key"]).decode('utf-8')
        self._key = Fernet(bytes(key, 'utf-8'))

    def decrypt_and_decode(self, strval):
        """ decrypts and decodes the value provided """
        byt = bytes(strval,'utf-8')
        enc = self._key.decrypt(byt)
        return enc.decode('utf-8')

    def decrypt_dict(self, encdict):
        """ loops through the keys in a dict and decrypts and decodes the values """
        if self._key is not None:
            decdict = {}
            for k in encdict:
                decval = self.decrypt_and_decode(encdict[k])
                decdict[k] = decval
            # print(json.dumps(decdict,indent=2))
            return decdict
        return False
