from random import randint
from time import strftime


class GlyphNameList:
    """
    Ordered collection of glyph names. AKA FontLab encoding
    """

    commentChars = ("#", "%")

    def __init__(self, initial_data=None):
        if isinstance(initial_data, GlyphNameList):
            self.__dict__["_data"] = dict(initial_data._data)
            self.__dict__["_metaData"] = dict(initial_data._metaData)
        else:
            self.__dict__["_data"] = {}
            self.__dict__["_metaData"] = dict(
                name="", ID=None, created=strftime("%Y.%m.%d-%H:%M:%S")
            )
        if isinstance(initial_data, str):
            self.read(initial_data)
        elif isinstance(initial_data, (list, tuple)):
            for i, name in enumerate(initial_data):
                self[i] = name

    def __repr__(self):
        return f"<GlyphNameList: slots={len(self)}, glyphNames={len(self._data)}>"

    def __len__(self):
        if self._data:
            return max(self._data.keys()) + 1
        return 0

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._data.get(key)
        elif isinstance(key, slice):
            # for i in self.keys()[key]:
            #     yield self[i]
            return [self[i] for i in self.keys()[key]]
        else:
            raise IndexError(f"key must be of type int, got '{key}', {type(key)}")

    def __setitem__(self, key, value):
        assert isinstance(key, int)
        assert isinstance(value, (str, type(None)))
        if value:
            self._data[key] = value
        else:
            del self._data[key]

    def __delitem__(self, key):
        assert isinstance(key, int)
        if key in self._data:
            del self._data[key]

    def __contains__(self, item):
        return item in self._data.values()

    def __getattr__(self, name):
        if name in self._metaData:
            return self._metaData[name]
        raise AttributeError

    def __setattr__(self, name, value):
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._metaData[name] = value

    def __iter__(self):
        return iter([self[i] for i in self.keys()])

    def keys(self):
        return range(len(self))

    def index(self, item):
        for key, value in self._data.items():
            if value == item:
                return key
        return -1

    def remove(self, item):
        idx = self.index(item)
        if idx >= 0:
            del self._data[idx]

    def glyphNames(self):
        for i in sorted(self._data.keys()):
            yield self._data[i]
        # return self._data.values()

    def isSupportedBy(self, other):
        return all(n in other for n in self._data.values())

    def missingIn(self, other):
        for name in self._data.values():
            if name not in other:
                yield name

    def clear(self):
        self.__dict__["_data"] = {}
        self.__dict__["_metaData"] = dict(name="", ID=None)

    def read(self, path_or_file):
        if hasattr(path_or_file, "read"):  # assume a readable file object
            inFile = path_or_file
            inFile.seek(0)
            closeStream = False
        else:  # assume path as string
            inFile = open(path_or_file, "r")
            closeStream = True
        self.clear()
        header_done = False
        last_index = -1
        for line in inFile:
            line = line.strip()
            if line:
                if line.startswith("%%") and ":" in line and not header_done:
                    line = line[2:]
                    name, value = line.split(":", 1)
                    if name == "FONTLAB ENCODING" and ";" in value:
                        _id, _name = value.split(";", 1)
                        self.name = _name.strip()
                        self.ID = _id.strip()
                    else:
                        setattr(self, name.strip(), value.strip())
                elif line[0] in self.commentChars:
                    continue
                else:
                    for commentChar in self.commentChars:
                        line = line.split(commentChar)[0]
                    parts = line.split()
                    if len(parts) == 1:
                        last_index += 1
                        self._data[last_index] = parts[0]
                    else:
                        try:
                            _index = int(parts[1])
                        except ValueError:
                            _index = last_index + 1
                        self._data[_index] = parts[0]
                        last_index = _index
                    header_done = True
        if closeStream:
            inFile.close()

    def save(self, path_or_file, format="FontLab"):
        if hasattr(path_or_file, "write"):  # assume a writeable file object
            outFile = path_or_file
            # inFile.seek(0)
            closeStream = False
        else:  # assume path as string
            outFile = open(path_or_file, "w")
            closeStream = True
        if format == "FontLab":
            if not self.ID:
                self.ID = str(randint(0xFFF, 0xFFFF))
            if not self.name:
                self.name = f"Encoding-{self.ID}"
            self.modified = strftime("%Y.%m.%d-%H:%M:%S")
            outFile.write(f"%%FONTLAB ENCODING: {self.ID}; {self.name}\n")
            for name in [n for n in sorted(self._metaData) if n not in ("name", "ID")]:
                outFile.write(f"%%{name}: {self._metaData[name]}\n")
            outFile.write("\n")
            for i in sorted(self._data):
                outFile.write(f"{self._data[i]}\t{i}\n")
        if closeStream:
            outFile.close()


def test001():
    l = GlyphNameList()
    l.name = "My Encoding"
    l[1] = "a"
    l[5] = "agrave"
    print(l.name)
    print(l[1])
    print(len(l))
    for n in l.glyphNames():
        print(n)
    print("a" in l)
    print("b" in l)
    print(l[1:7])
    print(l["ding"])
    print(l)
    l2 = GlyphNameList(l)
    l2[6] = "aacute"
    print(l2)
    print(l.isSupportedBy(l2))
    print(l2.isSupportedBy(l))
    print(l._metaData)
    l2.save(r"D:\User\Eigi\Documents\FontLab\Shared\Encoding\test.enc")


def test002():
    gnl = GlyphNameList(
        r"D:\User\Eigi\Documents\FontLab\Shared\Encoding\adobe_default.enc"
    )
    print(len(gnl))
    gnl.save(r"D:\User\Eigi\Documents\FontLab\Shared\Encoding\adobe_default_test.enc")


if __name__ == "__main__":
    test001()
