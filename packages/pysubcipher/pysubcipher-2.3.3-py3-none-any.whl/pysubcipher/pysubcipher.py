import base64
import string
import random
import pickle
import io
import os

from .__init__ import HEXDIGITS, PRINTABLE

from typing import Any
from types import TracebackType

class InvalidCharacterError(ValueError):
    def __init__(self, character: str, /) -> None:
        """Raised if an invalid token is present within a string of text while encrypting or decrypting a value.

        Args:
            character (str): The invalid character.
        """
        super().__init__(f"\"{character}\" is not recognised.")

class EncryptedStringInvalidError(ValueError):
    def __init__(self, token: str) -> None:
        """Raised if an encrypted string is invalid while attempting to decrypt it.

        Args:
            token (str): Unmatched token.
        """
        if len(token) > 18:
            token = f"{token[:18]}..."
        super().__init__(f"Encrypted string is not valid: decryption keys did not match token \"{token}\"")

class InvalidKeysError(ValueError):
    def __init__(self) -> None:
        """Raised if invalid keys are loaded into a SubstitutionCipher instance."""
        super().__init__(f"Cipher keys failed validation")

class _EncryptionKeys():
    def __init__(self, __min_length: int, __max_length: int, /, *, seed: int | float | str | bytes | bytearray | None, charset: str) -> None:
        """Generates a pair of encryption and decryption keys.

        Args:
            __min_length (int): The minimum length of a key.
            __max_length (int): The maximum length of a key.
            seed (int | float | str | bytes | bytearray | None): The random seed that keys will be generated with.
            charset (str): The character set to generate keys with.
        """
        self.__min_length: int = __min_length
        self.__max_length: int = __max_length
        self.__seed: int | float | str | bytes | bytearray | None = seed
        self.__charset: str = charset
        self._encryption_keys: dict[bytes, str] | None = None
        self._decryption_keys: dict[str, bytes] | None = None
        self.__generate_keys(seed = self.__seed)

    def __generate_keys(self, *, seed: bytes) -> None:
        """
        Generates a list of keys bound to a list of characters.

        Args:
            seed (bytes): The random seed to generate keys with.
        """
        random.seed(seed)
        encryption_keys: dict[bytes, str] = {}
        decryption_keys: dict[str, bytes] = {}
        characters = self.__charset

        for character in PRINTABLE:
            key = ''.join([random.choice(characters) for _ in range(random.randint(self.__min_length, self.__max_length))])
            __char = base64.b64encode(character.encode().hex().encode())
            encryption_keys[__char] = key
            decryption_keys[key] = __char

        self._encryption_keys = encryption_keys
        self._decryption_keys = decryption_keys
        random.seed(None)

class SubstitutionCipher(_EncryptionKeys):
    def __init__(self, min_key_length: int = 10, max_key_length: int = 20, *, seed: int | float | str | bytes | bytearray | None | None = os.urandom(1024), charset: str = HEXDIGITS) -> None:
        """A simple substitution cipher encryption tool to encrypt strings of text.

        Args:
            min_key_length (int): The minimum length of a cipher key.
            max_key_length (int): The maximum length of a cipher key.
            seed (int | float | str | bytes | bytearray | None, optional): The seed that cipher keys will be generated with. Defaults to os.urandom(1024).
            charset (str, optional): The character set that cipher keys will be generated with. Defaults to HEXDIGITS.
        """
        self.__min_key_length: int = min_key_length
        self.__max_key_length: int = max_key_length
        self.__charset: str = charset
        self.__current_seed: int | float | str | bytes | bytearray | None = seed
        if not isinstance(charset, str):
            raise TypeError(f"Parameter charset cannot be of type {type(charset)}")
        super().__init__(min_key_length, max_key_length, seed = seed, charset = self.__charset)

    def encrypt(self, s: str, /) -> bytes:
        """Encrypts a string of text using pre-defined cipher keys.

        Args:
            s (str): The string to encrypt.

        Raises:
            InvalidCharacterError: Raised if a non-printable character is present within the string.

        Returns:
            bytes: An encrypted byte string of the original string.
        """
        __encrypted_string: io.StringIO = io.StringIO()
        for character in s:
            character = base64.b64encode(character.encode().hex().encode())
            if character not in self._encryption_keys:
                raise InvalidCharacterError(bytearray.fromhex(base64.b64decode(character).decode()).decode()) 
            __encrypted_string.write(self._encryption_keys.get(character))
        return __encrypted_string.getvalue().encode()
    
    def decrypt(self, s: bytes, /) -> bytes:
        """Decrypts a string of text using pre-defined cipher keys.

        Args:
            s (bytes): The string to decrypt.

        Raises:
            TypeError: Raised if s is not an instance of <class 'bytes'>.
            EncryptedStringInvalidError: Raised if the encrypted string is invalid.

        Returns:
            bytes: An unencrypted byte string of the original encrypted string.
        """
        if not isinstance(s, bytes):
            raise TypeError(f"s must be of type bytes, not {type(s)}")
        __decrypted_string: io.StringIO = io.StringIO()
        while s:
            __match = False
            for k in self._decryption_keys:
                if s.startswith(k.encode()):
                    __decrypted_string.write(bytearray.fromhex(base64.b64decode(self._decryption_keys[k].decode()).decode()).decode())
                    s = s[len(k):]
                    __match = True
                    break
            if not __match:
                raise EncryptedStringInvalidError(s.decode())
        return __decrypted_string.getvalue().encode()
    
    def set_seed(self, seed: int | float | str | bytes | bytearray | None, /) -> None:
        """Sets the random seed for cipher keys to be generated with.

        Args:
            seed (int | float | str | bytes | bytearray | None): The seed to override.
        """
        self.__current_seed = seed
        super().__init__(self.__min_key_length, self.__max_key_length, seed = seed, charset = self.__charset)

    def regenerate_keys(self, seed: int | float | str | bytes | bytearray | None = os.urandom(1024), /) -> None:
        """Regenerates encryption and decryption keys.

        Args:
            seed (int | float | str | bytes | bytearray | None, optional): The seed to generate cipher keys with. Defaults to os.urandom(1024).
        """
        self.set_seed(seed)

    def __test_keys(self, encryption_keys: Any, decryption_keys: Any) -> bool:
        """Tests and validates cipher keys.

        Args:
            encryption_keys (Any): The encryption keys to validate.
            decryption_keys (Any): The decryption keys to validate.

        Returns:
            bool: Returns True if cipher keys are valid, and False if not.
        """
        cipher = SubstitutionCipher()
        cipher._encryption_keys = encryption_keys
        cipher._decryption_keys = decryption_keys
        encrypted_text = cipher.encrypt(PRINTABLE)
        decrypted_text = cipher.decrypt(encrypted_text)
        if decrypted_text.decode() != PRINTABLE:
            return False
        return True
    
    def save_keys(self, file: str, /, *, truncate: bool = False) -> None:
        """Saves the current cipher keys to a file.

        Args:
            file (str): The filepath.
            truncate (bool, optional): If True, file will be truncated prematurely before storing the keys. Defaults to False.
        """
        self.__current_seed = None
        with open(file, "wb") as f:
            if truncate:
                f.truncate(0)
            f.write(pickle.dumps([self._encryption_keys, self._decryption_keys]))

    def load_keys(self, file: str, /) -> None:
        """Loads cipher keys into the current instance.

        Args:
            file (str): The path to the file where the keys are stored.

        Raises:
            InvalidKeysError: Raised if the cipher keys are not valid.
        """
        self.__current_seed = None
        with open(file, "rb") as f:
            contents = f.read()
            try:
                keys = pickle.loads(contents)
            except pickle.UnpicklingError:
                raise InvalidKeysError()
            encryption_keys = keys[0]
            decryption_keys = keys[1]
            result: bool = self.__test_keys(encryption_keys, decryption_keys)
            if result:
                self._encryption_keys = encryption_keys
                self._decryption_keys = decryption_keys
            else:
                raise InvalidKeysError()
            
    def __enter__(self):
        return self
    
    def __exit__(self, exit_type: Exception | None, exit_value: Exception | None, traceback: TracebackType | None) -> None:
        if exit_type:
            raise exit_type(exit_value)

    def __str__(self) -> str:
        return f"SubstitutionCipher(minimum_key_length={self.__min_key_length}, maximum_key_length={self.__max_key_length})"

    def __repr__(self) -> str:
        __quote: str = "'"
        return f"SubstitutionCipher(minimum_key_length={self.__min_key_length}, maximum_key_length={self.__max_key_length}, seed={__quote if isinstance(self.__current_seed, str) else ''}{self.__current_seed}{__quote if isinstance(self.__current_seed, str) else ''}, charset='{self.__charset.strip()}')"

class FileSubstitutionCipher(SubstitutionCipher):
    def __init__(self, min_key_length: int = 10, max_key_length: int = 20, *, seed: int | float | str | bytes | bytearray | None = os.urandom(1024), charset: str = HEXDIGITS) -> None:
        """A simple substitution cipher encryption tool to encrypt file's and their contents.

        Args:
            min_key_length (int): The minimum length of a cipher key.
            max_key_length (int): The maximum length of a cipher key.
            seed (int | float | str | bytes | bytearray | None, optional): The seed that cipher keys will be generated with. Defaults to os.urandom(1024).
            charset (str, optional): The character set that cipher keys will be generated with. Defaults to HEXDIGITS.
        """
        self.__min_key_length: int = min_key_length
        self.__max_key_length: int = max_key_length
        self.__seed: int | float | str | bytes | bytearray | None = seed
        self.__charset: str = charset
        super().__init__(self.__min_key_length, self.__max_key_length, seed = self.__seed, charset = self.__charset)

    def encrypt(self, filepath: str, /, *, write: bool = False) -> bytes | None:
        """Encrypts the contents of a file and returns the encrypted contents.

        Args:
            filepath (str): The path to the file that will be encrypted.
            write (bool, optional): Override the file's contents. Defaults to False.

        Returns:
            bytes | None: Returns the encrypted contents if write is False, otherwise returns None.
        """
        encrypted_contents: bytes = super().encrypt(open(filepath).read())
        if write:
            with open(filepath, "wb") as file:
                file.truncate(0)
                file.write(encrypted_contents)
        else:
            return encrypted_contents
        
    def decrypt(self, filepath: str, /, *, write: bool = False) -> bytes | None:
        """Decrypts the contents of a file and returns the decrypted contents.

        Args:
            filepath (str): The path to the file that will be decrypted.
            write (bool, optional): Override the file's contents. Defaults to False.

        Returns:
            bytes | None: Returns the decrypted contents if write is False, otherwise returns None.
        """
        decrypted_contents: bytes = super().decrypt(open(filepath).read().encode())
        if write:
            with open(filepath, "wb") as file:
                file.truncate(0)
                file.write(decrypted_contents)
        else:
            return decrypted_contents