#######
# This encrpyts a dictionary called 'secrets' from a python file called 'mysecrets.py'
#  1. Generates an encryption key and writes it to a file 'refKey.txt'
#  2. Loops through the plaintext dict encrypting each value and appending the plaintext key and encrypted value to the 'secretsecrets' dict
#  3. Writes out the encrpyted dict as 'encsecrets' in a python file called 'secretsecrets.py'
#
#  4. Create a secret in your cluster with "kubectl create secret generic py-secret-key --from-file=key=refKey.txt"
#  5. Mount your secret as a volume in your deployment.yaml, e.g, as '/etc/secret-volume/key'
#  6. Add secretsecrets.py to your source tree and move 'mysecrets.py' and 'refKey.txt' out of your source tree
#
#  7. in your python source which requires access to your secrets add:
#     from decrypt import DecryptDicts
#     dd = DecryptDicts('/etc/secret-volume/key')
#     from secretsecrets import encsecrets
#     secrets = dd.decryptDict(encsecrets)
#######

# pip install cryptography -- gets you cffi and pycparser too
# provides key-generation and encrypt/decrypt functions
from cryptography.fernet import Fernet
# python dict with secrets to encrypt
# from mysecrets import secrets
# required to output new 'secretsecrets.py'
import json

class EncryptDicts:
    def __init__(self):
        self._key = None
        self._encdict = {}

    def new_key(self, keypath):
        # # generate a new key
        key = Fernet.generate_key()
        # # write the key out to a text file
        f = open(keypath, "wb")
        f.write(key)
        f.close()
        # instantiates a Fernet object with our new key
        self._key = Fernet(key)

    def read_key(self, keypath):
        # or, read/use an existing key
        with open(keypath, "r", encoding='utf-8') as fstr:
            refkey = ''.join(fstr.readlines())
            refkeybyt = bytes(refkey, 'utf-8')
        fstr.close()
        self._key = Fernet(refkeybyt)

    # function to encrypt the dict value
    def encode_and_encrypt(self, str, key):
        byt = bytes(str,'utf-8')
        enc = key.encrypt(byt).decode('utf-8')
        return enc
    
    def encrypt_dict(self, rawsecrets):
        """ loops through the keys in a dict and decrypts and decodes the values """
        if self._key is not None:
            for k in rawsecrets:
                print(f'{k}:{rawsecrets[k]}')
                encval = self.encode_and_encrypt(rawsecrets[k], self._key)
                self._encdict[k] = encval
            # print(json.dumps(self._encdict,indent=2))
        return False
    
    def write_dict(self,path):
        # write out the new python file with the plaintext keys and encypted values
        f = open(path, "w")
        f.write('encsecrets = ')
        f.writelines(json.dumps(self._encdict,indent=2))
        f.close()





# # new dict replicating the plaintext keys from secrets, but with encrypted values
# secretsecrets = {}

# refKey = read_key()

# # loop through the keys, encrypting the values and appending the encrypted values
# for k in secrets:
#     encval = eAndE(secrets[k],refKey)
#     secretsecrets[k] = encval

# # write out the new python file with the plaintext keys and encypted values
# f = open("secretsecrets.py", "w")
# f.write('encsecrets = ')
# f.writelines(json.dumps(secretsecrets,indent=2))
# f.close()