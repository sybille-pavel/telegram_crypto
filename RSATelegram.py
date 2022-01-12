from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os


class RSAMessages:
    def __init__(self, chatId):
        self.chatId = chatId
        try:
            os.mkdir(chatId)
            self.generateKey()
        except FileExistsError as e:
            pass

    def getPublicKey(self):
        try:
            file = open(self.getPathPublicKey())
        except FileNotFoundError as e:
            return False
        else:
            return file.read()

    def getPrivateKey(self):
        try:
            file = open(self.getPathPrivateKey())
        except FileNotFoundError as e:
            return False
        else:
            return file.read()

    def getCompanionPublicKey(self):
        try:
            file = open(self.getPathCompanionPublicKey())
        except FileNotFoundError as e:
            return False
        else:
            return file.read()

    def getChatInfo(self):
        try:
            file = open(self.getPathChatInfo())
        except FileNotFoundError as e:
            return 0
        else:
            return file.read()

    def getPathPublicKey(self):
        return self.chatId + "/receiver.pem"

    def getPathPrivateKey(self):
        return self.chatId + "/private.pem"

    def getPathCompanionPublicKey(self):
        return self.chatId + "/receiver_companion.pem"

    def getPathMessageFile(self):
        return self.chatId + "/messagebin.bin"

    def getPathChatInfo(self):
        return self.chatId + "/info.bin"


    def setCompanionPublicKey(self, publicKey, reCreate=False):
        filepath = self.getPathCompanionPublicKey()
        if (not self.getCompanionPublicKey() or reCreate):
            file = open(filepath, "wb")
            file.write(RSA.import_key(publicKey).export_key())
            file.close()

    def setChatInfo(self, info):
        filepath = self.getPathChatInfo()
        file = open(filepath, "wb")
        file.write(info)
        file.close()

    def generateKey(self, reCreate=False):
        if ((self.getPrivateKey() and self.getPublicKey()) and not reCreate):
            return

        key = RSA.generate(2048)
        privateKey = key.export_key()
        fileOut = open(self.getPathPrivateKey(), "wb")
        fileOut.write(privateKey)
        fileOut.close()

        publicKey = key.publickey().export_key()
        fileOut = open(self.getPathPublicKey(), "wb")
        fileOut.write(publicKey)
        fileOut.close()

    def encryptData(self, data):
        publicKey = self.getCompanionPublicKey()

        publicKey = RSA.import_key(publicKey)
        session = get_random_bytes(16)

        cipherRsa = PKCS1_OAEP.new(publicKey)
        encSessionKey = cipherRsa.encrypt(session)

        cipherAes = AES.new(session, AES.MODE_EAX)

        data = data.encode("utf-8")
        cipherText, tag = cipherAes.encrypt_and_digest(data)

        FILE_NAME = self.getPathMessageFile()
        file_out = open(FILE_NAME, "wb")
        [file_out.write(x) for x in (encSessionKey, cipherAes.nonce, tag, cipherText)]
        file_out.close()
        return FILE_NAME

    def decryptData(self):
        filename = self.getPathMessageFile()
        fileIn = open(filename, "rb")

        privateKey = RSA.import_key(self.getPrivateKey())

        enc_session_key, nonce, tag, ciphertext = \
            [fileIn.read(x) for x in (privateKey.size_in_bytes(), 16, 16, -1)]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(privateKey)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode("utf-8")
