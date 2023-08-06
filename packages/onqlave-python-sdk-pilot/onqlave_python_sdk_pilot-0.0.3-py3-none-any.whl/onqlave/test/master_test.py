import sys
import base64
import io
import time

from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass

from encryption import options
from encryption.encryption import Encryption
from credentials.credentials import Credential
from connection.client import RetrySettings

credentials = [
    {# aes-128
        "access_key": "onq.393NirHhBSVgGc6lhImDTrom1MNGT4GZ",
        "arx_url": "https://dp0.onqlave.com/cluster--zat85DR9975e7uZlUqot-",
        "server_signing_key": "onq.fXc8uj89tNzyIp3JqghedQu4wFvUK4yi",
        "server_secret_key": "onq.HBDzwA3AXsHCxxysA2CAlYOVuBHcFIpqcTiCd97h833WgWldKzdVFhiioS4pufJktdsuNxFmuFghMTer2MFuB851wQuTwUnW6K8H5sbynX8DCN4mKYu0NjMC4cOPjyIB",
        "client_key": ""
    },

    {# aes-256
        "access_key": "onq.8aASPTpXaFKnTCmfNNH1msqedGUoAf63",
        "arx_url": "https://dp0.onqlave.com/cluster--3JCMwPJ0fzRvKuQdUCV-n",
        "server_signing_key": "onq.JHqDxHl8WNAcKwMa0xtETJyhrdRo7EVE",
        "server_secret_key": "onq.tEAr55xspZkhZ5O0wbtrbEuLbMzV8HxZbZtNikltGG4XGK8a5K4LJCGSuN2W9ocWODRXF2ab33YUXqX5D6iXubg2fTpeH9NKkloZzSAIM8SmbXjol15gyZ0sB5xM7C7a",
        "client_key": ""
    },

    {# xchacha-20
        "access_key": "onq.YkDMx4ljEkssZtE58BcwYmHHElUGxi7x",
        "arx_url": "https://dp0.onqlave.com/cluster--6KPvfhDykP7_JeR1gA40K",
        "server_signing_key": "onq.YIhmDTp2VaW17LH6HPIvOKj8JEBOcuyA",
        "server_secret_key": "onq.8uRgl7BmZQJcXNSdRKzhJub4gBiyc1mBnbKLsLJWIpUogMbSSK6ZAyv2ukMJI13tQpIArEvgmTUOFUNLyRMi1KpHXg9lHkTflGLuQC8xw8a0hRU3B7NSGeP7XtwvCYJ8",
        "client_key": ""
    }
]

def run_test():
    debug_option = options.DebugOption(enable_debug=True)
    for each_cred in credentials:
        arx_option = options.ArxOption(arx_url=each_cred['arx_url'])
        credential_option = Credential(
            access_key=each_cred['access_key'],
            signing_key=each_cred['server_signing_key'],
            secret_key=each_cred['server_secret_key'])
        retry_option = RetrySettings(count=1,wait_time=1,max_wait_time=2)

        encryption_engine = Encryption(
            debug_option=debug_option,
            arx_option=arx_option,
            credential_option=credential_option,
            retry_setting=retry_option
        )

        plaintext = "hello world"
        associated_data = "auth"

        cipher_text = encryption_engine.encrypt(plaintext.encode(), associated_data.encode())

        decrypted_cipher = encryption_engine.derypt(cipher_text,associated_data.encode())
        

        plain_file_stream = open("/home/extreme45nm/main-projects/onqlave/onqlave-python/onqlave/test/plain-stream.txt","rb")
        plain_stream = io.BytesIO(plain_file_stream.read())

        cipher_stream = io.BytesIO()
        
        encryption_engine.encrypt_stream(plain_stream,cipher_stream,associated_data.encode())
        cipher_stream.seek(0)

        decrypted_stream = io.BytesIO()
        encryption_engine.derypt_stream(
            cipher_stream=cipher_stream,
            plain_stream=decrypted_stream,
            associated_data=associated_data.encode()
        )
        decrypted_stream.seek(0)

        with open(
            "/home/extreme45nm/main-projects/onqlave/onqlave-python/onqlave/test/decrypted-stream.txt", # replace your output file here
            "wb"
        ) as result:
            result.write(decrypted_stream.read())

run_test()