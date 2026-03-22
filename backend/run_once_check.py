from db import collection

for f in collection.find():
    print(repr(f.get("label")), "|", f.get("claim"))
