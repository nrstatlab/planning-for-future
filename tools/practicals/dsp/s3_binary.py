# Stage 2 -- BINARY files: struct for fixed-width records, array for
# homogeneous numbers, pickle for Python objects.  All three are standard
# library; none of them is readable in a text editor, and that is the point.
import array
import io
import pickle
import struct

# Step 1: The records
RECORDS = [(1, b"Asha Rao  ", 40, 7.25),
           (2, b"Biju Menon", 57, 5.50),
           (3, b"Chitra Das", 37, 8.00)]

# Step 2: struct: one format string describes every record
FMT = "<i10sif"          # '<' little-endian, no padding; i=int32 10s=bytes i=int32 f=float32
SIZE = struct.calcsize(FMT)
print(f"format {FMT!r}  record size {SIZE} bytes")
print(f"format '@i10sif' (native, padded) would be "
      f"{struct.calcsize('@i10sif')} bytes -- alignment is not free")

buf = io.BytesIO()
for rec in RECORDS:
    buf.write(struct.pack(FMT, *rec))
raw = buf.getvalue()
print(f"wrote {len(RECORDS)} records, {len(raw)} bytes")
print("first 22 bytes:", raw[:SIZE].hex(" "))

back = []
for off in range(0, len(raw), SIZE):
    i, name, income, visits = struct.unpack_from(FMT, raw, off)
    back.append((i, name.rstrip(b" ").decode(), income, round(visits, 2)))
print("read back:")
for r in back:
    print("  ", r)

# Step 3: Byte order: the same bytes, read the other way round
one = struct.pack("<i", 1)
print()
print("the integer 1 packed little-endian:", one.hex(" "),
      "-> read as big-endian:", struct.unpack(">i", one)[0])
print("a file written on one machine and read with the wrong byte order is not")
print("corrupt, it is WRONG -- which is far harder to notice.  Always fix the")
print("byte order in the format string; never rely on the native default.")

# Step 4: array: homogeneous numbers, far more compact than a list
a = array.array("i", [40, 57, 37, 69, 36, 38])
print()
print(f"array('i') of {len(a)} ints -> {len(a.tobytes())} bytes "
      f"({a.itemsize} each)")
b = array.array("i")
b.frombytes(a.tobytes())
print("round trip identical:", list(b) == list(a))

# Step 5: pickle: any Python object, at a price
obj = {"rows": RECORDS, "source": "customers.bin", "clean": True}
blob = pickle.dumps(obj, protocol=4)   # pin the protocol: the default moves
                                      # with the Python version, and so does the size
print()
print(f"pickle: {len(blob)} bytes, round trip identical:",
      pickle.loads(blob) == obj)
print("pickle executes code while loading, so NEVER unpickle a file you did")
print("not write.  For data that leaves your own machine use JSON, CSV or a")
print("declared binary layout like the struct format above.")
