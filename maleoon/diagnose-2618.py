#!/usr/bin/env python3
"""Read-only Zink 26.1.8 extension and feature diagnostics; no capability spoofing."""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
info = root / "src/gallium/drivers/zink/zink_device_info.py"
screen = root / "src/gallium/drivers/zink/zink_screen.c"

s = info.read_text()
target_lines = [line for line in s.splitlines() if 'debug_printf("ZINK: ${ext.name} required!' in line]
assert len(target_lines) == 1, f"Expected 1 required-extension marker, got {len(target_lines)}"
line = target_lines[0]
indent = line[:len(line) - len(line.lstrip())]
extra = indent + 'fprintf(stderr, "[maleoon-2618] missing required extension: ${ext.name}\\n");'
s = s.replace(line, line + "\n" + extra, 1)
header_line = '#include "zink_screen.h"'
assert header_line in s, "generated device-info header marker missing"
s = s.replace(header_line, header_line + '\n#include <stdio.h>', 1)
info.write_text(s)

t = screen.read_text()
p1 = r'(if\s*\(!zink_get_physical_device_info\(screen\)\)\s*\{)'
t, cnt = re.subn(p1, r'\1\n      fprintf(stderr, "[maleoon-2618] device-info returned false\\n");', t, count=1)
assert cnt == 1, "Could not identify Zink device-info failure checkpoint"
p2 = r'(if\s*\(!screen->info.rb2_feats.nullDescriptor\)\s*\{)'
t, cnt2 = re.subn(p2, r'fprintf(stderr, "[maleoon-2618] nullDescriptor=%u\\n", (unsigned)screen->info.rb2_feats.nullDescriptor);\n   \1', t, count=1)
if not cnt2:
    print("NOTE: nullDescriptor specific check not present in this Mesa source")
screen.write_text(t)
print("Mesa 26.1.8 diagnostic instrumentation added (no required-feature changes)")
