#!/usr/bin/env python3
import pathlib, re, shutil
root=pathlib.Path(__file__).resolve().parents[1]
recipe=root/"packages/mesa/build.sh"
patch=root/"maleoon/9999-maleoon-zink-diagnostic.patch"
assert recipe.is_file() and patch.is_file()
s=recipe.read_text()
assert re.search(r'(?m)^TERMUX_PKG_VERSION="?(26\.2\.4)"?$',s), "Mesa version mismatch"
assert "bce5f7fbebb934373b86c999a064d52fb5065878dc57f287f95346648ec832e9" in s, "source checksum mismatch"
dest=root/"packages/mesa/9999-maleoon-zink-diagnostic.patch"
if dest.exists(): assert dest.read_bytes()==patch.read_bytes(), "conflicting patch"
else: shutil.copyfile(patch,dest)
print("Mesa source already 26.2.4; staged diagnostic patch:",dest)
