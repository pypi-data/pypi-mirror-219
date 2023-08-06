import json
from securedict import DecryptDicts, EncryptDicts

def test_encrypt_and_decrypt():

    secrets = {
        "Key1" : "Value1",
        "Key2" : "Value2",
        "Key3" : "Value3",
    }

    ed = EncryptDicts()
    dd = DecryptDicts()

    ed.new_key("testRefKey.txt")
    ed.encrypt_dict(secrets)
    ed.write_dict("encsecrets.py")
    # print(json.dumps(ed._encdict,indent=2))

    dd.read_key_from_file("testRefKey.txt")
    dec = dd.decrypt_dict(ed._encdict)
    # print(json.dumps(dec,indent=2))

    assert dec == secrets
