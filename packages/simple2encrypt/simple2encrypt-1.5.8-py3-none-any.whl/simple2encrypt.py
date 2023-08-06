"""
encryption_utils.py
Utility functions for encryption and file operations.
"""

import argparse
import os
import sys

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

__version__ = '1.5.8'


class Encryption:
    """
    A class for performing encryption and decryption using the AES algorithm.
    """

    def __init__(self, key: bytes, data: bytes):
        """
        Initialize the Encryption object with the key and data.
        :param key: Encryption key
        :param data: Data to be encrypted or decrypted
        """
        self.key = key
        self.data = data

    def encrypt(self) -> bytes:
        """
        Encrypt the data using the AES algorithm.
        :return: Encrypted data
        """
        cipher = AES.new(self.key, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(self.data, cipher.block_size))
        return cipher.iv + encrypted_data

    def decrypt(self) -> bytes:
        """
        Decrypt the data using the AES algorithm.
        :return: Decrypted data
        """
        initialization_vector = self.data[:AES.block_size]  # Extract the IV from the data
        cipher = AES.new(self.key, AES.MODE_CBC, iv=initialization_vector)
        decrypted_data = cipher.decrypt(self.data[AES.block_size:])
        return unpad(decrypted_data, cipher.block_size)


def folder_encrypt(folder_path: str, key: bytes, add_extension='.enc') -> None:
    """
    Encrypts all files within a given folder.

    :param add_extension: Add the extension to the end of the file
    :param folder_path: Path to the folder containing the files to be encrypted.
    :param key: The key for encryption.
    :raises ValueError: If the provided folder path is not a directory.
    """
    if not os.path.isdir(folder_path):
        raise ValueError("Expected a folder path, but received a different type of path.")
    os.chdir(folder_path)
    for file in os.listdir(folder_path):

        if os.path.isfile(folder_path):
            data = read_binary(file)
            encryption = Encryption(key, data)
            encrypted_data = encryption.encrypt()
            new_file_path = file + add_extension
            write_binary(new_file_path, encrypted_data)
            os.remove(file)


def folder_dencrypt(folder_path: str, key: bytes) -> None:
    """
    Decrypts all files within a given folder.

    :param folder_path: Path to the folder containing the files to be decrypted.
    :param key: The key for decryption.
    :raises ValueError: If the provided folder path is not a directory.
    """
    if not os.path.isdir(folder_path):
        raise ValueError("Expected a folder path, but received a different type of path.")
    os.chdir(folder_path)
    for file in os.listdir(folder_path):

        if os.path.isfile(file):
            data = read_binary(file)
            decryption = Encryption(key, data)
            decrypted_data = decryption.decrypt()
            new_file_path = delete_extension(file)
            write_binary(new_file_path, decrypted_data)
            os.remove(file)


def delete_extension(path: str) -> str:
    """
    Remove the last file extension from a path.

    :param path: The file path
    :return: The path without the last extension
    """
    dir_name, basename = os.path.split(path)
    while '.' in basename:
        basename, extension = os.path.splitext(basename)
        if extension:
            return os.path.join(dir_name, basename)
    return path


def generate_key(password: str, length: int) -> bytes:
    """
    Create a new key based on the password and save it to a file.
    :param password: Password for a key generation
    :param length: Length key
    :return: the new key
    """
    valid_lengths = [16, 24, 32]
    if length not in valid_lengths:
        raise ValueError('Invalid key length. Choose length from this list: [16, 24, 32]')
    salt = os.urandom(length)
    key = PBKDF2(password, salt, dkLen=32)
    return key


def read_binary(file_path: str) -> bytes:
    """
    Read binary data from a file.
    :param file_path: Path of the file
    :return: Binary data from the file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")
    if os.path.isdir(file_path):
        raise ValueError("Path is a directory. File path is expected.")
    with open(file_path, 'rb') as f:
        return f.read()


def write_binary(file_path, data) -> bool:
    """
    Write binary data to a file.
    :param file_path: Path of the file to write the data to
    :param data:  write
    :return: True if the file was saved successfully
    """
    if os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' already exists.")
    if os.path.isdir(file_path):
        raise ValueError("Path is a directory. File path is expected.")
    with open(file_path, 'wb') as f:
        f.write(data)
        return True


def encrypt_walk_dirs(folder_path: str, key: bytes, extension: str = '.enc') -> None:
    """
    Walks through the specified folder path and encrypts all files using the provided AES key.

    :param folder_path: The absolute folder path to walk on and encrypt files within.
    :param key: The AES key used for encryption.
    :param extension: Optional. The extension to add to the new encrypted file. Defaults to '.enc'.

    :return: None

    :raises PermissionError: If there is a permission error while accessing or modifying files.
    :raises FileExistsError: If a file with the new name already exists in the destination.
    :raises FileNotFoundError: If the specified file is not found.
    :raises ValueError: If there is an error in the provided data or key.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Read the binary data from the file
                data = read_binary(file_path)

                # Encrypt the data using the provided AES key
                encrypt = Encryption(key, data)
                encrypted_data = encrypt.encrypt()

                # Remove the original file
                os.remove(file_path)

                # Create the new filename with the specified extension
                new_file = f'{file_path}{extension}'

                # Write the encrypted data to the new file
                write_binary(new_file, encrypted_data)

            except (PermissionError, FileExistsError, FileNotFoundError, ValueError) as err:
                # Raise the error to be handled by the calling code
                raise err


def decrypt_walk_dirs(folder_path: str, key: bytes) -> None:
    """
    Walks through the specified folder path and decrypts all files using the provided AES key.

    :param folder_path: The absolute folder path to walk on and decrypt files within.
    :param key: The AES key used for decryption.
    :return: None

    :raises PermissionError: If there is a permission error while accessing or modifying files.
    :raises FileExistsError: If a file with the new name already exists in the destination.
    :raises FileNotFoundError: If the specified file is not found.
    :raises ValueError: If there is an error in the provided data or key.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Read the binary data from the file
                data = read_binary(file_path)

                # Decrypt the data using the provided AES key
                encrypt = Encryption(key, data)
                encrypted_data = encrypt.decrypt()

                # Remove the original file
                os.remove(file_path)

                # Create the new filename with the specified extension
                new_file = delete_extension(file_path)

                # Write the decrypted data to the new file
                write_binary(new_file, encrypted_data)

            except (PermissionError, FileExistsError, FileNotFoundError, ValueError) as err:
                # Raise the error to be handled by the calling code
                raise err


def custom_input(question: str) -> str:
    """
    Take a question as input from the user and return their response.
    :param question: Question to ask the user
    :return: Users response
    """
    try:
        message = input(question)
        return message
    except (KeyboardInterrupt, EOFError):
        print('\n[x] Script closed.')
        sys.exit()


def main():
    """
    the main function calls it to create the secret key
    :return:
    """
    parser = argparse.ArgumentParser(prog='encrypt data', description='create new encryption key')
    parser.add_argument('filename', type=str, help='name of the secret file to save example my-key.key')
    parser.add_argument('password', type=str, help='Password for key generation')
    args = parser.parse_args()
    password = args.password
    file_name = args.filename
    try:
        key = generate_key(password, length=32)
        write_binary(file_name, key)
        print(f"A new file was created based on your password. The file name is: {file_name}")
    except (ValueError, FileExistsError, FileNotFoundError) as write_error:
        print(write_error)
        sys.exit()


if __name__ == '__main__':
    main()
