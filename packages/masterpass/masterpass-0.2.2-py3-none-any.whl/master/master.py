import os
import sys
import hashlib
import base64
import re

from .logger import Logger


class Master:

    def __init__(self, path: str):
        self.path = path
        self.separator = "-"
        self.length = 6
        self.chunks = 6

        self.services = None
        self.username = None
        self.password = None


    def load(self) -> int:
        if not self.services is None:
            return len(self.services)

        self.services = set()
        if not os.path.isfile(self.path):
            Logger.warn(f"File {self.path} doesn't exit.")
            return 0

        with open(self.path, "r") as f:
            for line in f.readlines():
                self.services.add(line.strip())

        Logger.debug(f"Loaded file {self.path}")
        return len(self.services)


    def add(self, service: str):
        self.load()
        return self.services.add(service)


    def remove(self, service: str):
        self.load()
        return self.services.discard(service)


    def save(self) -> bool:
        dirName = os.path.dirname(self.path)
        os.makedirs(dirName, exist_ok=True)

        with open(self.path, "w") as f:
            f.write("\n".join(self.services))
        Logger.debug(f"Wrote file {self.path}")


    def generate(self, service: str, counter: int = 0) -> str:
        source = f"{self.username}:{self.password}:{service}:{counter}"
        Logger.debug(f"Source:   {source}")
        hashed = hashlib.sha256()
        hashed.update(bytes(source, "utf8"))
        digest = hashed.digest()
        Logger.debug(f"Digest:   {digest} ({type(digest)} {len(digest)})")
        Logger.debug(f"Hex:      {digest.hex()}")
        encoded = base64.b64encode(digest).decode()
        Logger.debug(f"Encoded:  {encoded} ({type(encoded)})")

        cleaned = re.sub(r"[^0-9A-Za-z]", "", encoded)
        parts = []
        for i in range(self.chunks):
            start = i * self.length
            stop = (i + 1) * self.length
            parts.append(cleaned[start:stop])
        Logger.debug(f"Parts: {parts}")
        password = self.separator.join(parts)
        Logger.debug(f"Password: {password}")
        return password
