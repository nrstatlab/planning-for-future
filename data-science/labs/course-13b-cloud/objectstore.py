"""An object store with the semantics that actually matter.

S3, Azure Blob and GCS are all the same thing: a flat KEY -> BYTES map with
per-object metadata. Everything students find surprising follows from "flat":

  * there are NO DIRECTORIES. 'raw/2026/sales.csv' is one key containing two
    slashes, and the console's folder tree is a rendering of common prefixes.
  * you cannot rename. A rename is a copy plus a delete, and it costs a full
    read and a full write.
  * listing is by PREFIX, and it is the only query the store supports.
"""


class ObjectStore:
    def __init__(self, bucket):
        self.bucket = bucket
        self.objects = {}          # key -> {"body": bytes, "class": str, ...}
        self.versioning = False
        self.versions = {}         # key -> [older bodies]

    def put(self, key, body, storage_class="Standard"):
        if self.versioning and key in self.objects:
            self.versions.setdefault(key, []).append(self.objects[key])
        self.objects[key] = {"body": body, "class": storage_class,
                             "size": len(body)}
        return key

    def get(self, key):
        if key not in self.objects:
            raise KeyError(f"NoSuchKey: {key}")
        return self.objects[key]["body"]

    def delete(self, key):
        """With versioning on, a delete writes a DELETE MARKER."""
        if key not in self.objects:
            return False
        if self.versioning:
            self.versions.setdefault(key, []).append(self.objects[key])
            self.objects[key] = {"body": None, "class": "DeleteMarker",
                                 "size": 0}
        else:
            del self.objects[key]
        return True

    def list(self, prefix="", delimiter=None):
        """List by prefix. With a delimiter, return common prefixes too.

        THIS is what draws the folder tree in the console. There is no
        directory anywhere in this class.
        """
        keys = sorted(k for k in self.objects if k.startswith(prefix))
        if delimiter is None:
            return keys, []
        plain, prefixes = [], set()
        for k in keys:
            rest = k[len(prefix):]
            if delimiter in rest:
                prefixes.add(prefix + rest.split(delimiter, 1)[0] + delimiter)
            else:
                plain.append(k)
        return plain, sorted(prefixes)

    def copy(self, src, dst):
        obj = self.objects[src]
        self.objects[dst] = dict(obj)
        return dst

    def rename(self, src, dst):
        """There is no rename. This is what one actually costs."""
        self.copy(src, dst)
        self.delete(src)
        return {"bytes_read": self.objects[dst]["size"],
                "bytes_written": self.objects[dst]["size"],
                "requests": 2}

    def total_bytes(self):
        return sum(o["size"] for o in self.objects.values())
