import pickle
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

class ConfigAPI():
    def __init__(self, path, key):
        self.path = path
        self.key = key

    def calculateHash(self, data_bytes):
        """Calculates the SHA256 hash of the given data"""
        hash_object = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_object.update(data_bytes)
        digest = hash_object.finalize()
        return digest.hex()
    
    def decryptData(self, ciphertext, key):
        """Decrypts, deobfuscates, decodes, and deserializes the given data using the given key."""
        fernet = Fernet(key)
        encoded_data = fernet.decrypt(ciphertext)
        serialized_data = base64.b64decode(encoded_data)
        return pickle.loads(serialized_data)

    def DecHMAC(self, pair, key):
        """Decrypts the given data and verifies the HMAC using the given key. Returns the decrypted data if the HMAC is valid, otherwise raise an error."""
        hmac = pair[0]
        ciphertext = pair[1]
        hmac_calculated = self.calculateHash(ciphertext)
        if hmac == hmac_calculated:
            return self.decryptData(ciphertext, key)
        else:
            raise ValueError("HMAC verification failed. The data has been tampered with!")

    def getFile(self):
        with open(self.path, 'rb') as f:
            pair = pickle.load(f)
            return pair

    def get(self) -> dict:
        try:
            encrypted_pair = self.getFile()
            return self.DecHMAC(encrypted_pair, self.key)
        except Exception as e:
            raise e
    
    def getSimpleDict(self) -> dict:
        d = self.get()
        return {k: v["value"] for k, v in d.items()}
    
    def getSQL(self, name) -> str:
        d = self.get()
        assert name in d
        assert d[name]["type"] == "Stored Procedure"
        # Go read the SQL File.
        file_path = d[name]["value"]
        with open(file_path, 'r') as f:
            sql = f.read()
            return sql

        