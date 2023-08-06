from __future__ import absolute_import
import hashlib

def blended_hash(layout, prefix=None):
    if layout:
        try:
            hash_value = hashlib.md5(repr(layout).encode('utf-8')).hexdigest()
            if prefix:
                prefix = prefix.replace(" ", "_")
                if prefix[0].isalpha() or prefix[0] == '_':
                    hash_value = prefix+hash_value
                else:
                    hash_value = "Prefix must start with 'alphabat' or '_'"
            else:
                hash_value = "layout_" + hash_value
        except Exception as e:
            hash_value = e
        return hash_value
