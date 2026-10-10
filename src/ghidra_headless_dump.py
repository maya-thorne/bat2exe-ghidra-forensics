#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
================================================================================
bat2exe-ghidra-forensics :: Ghidra Headless Automated Triage & Extraction Script
================================================================================
Author: Maya Thorne
Usage:
  analyzeHeadless <project_dir> <project_name> -import <target.exe>
                  -postScript ghidra_headless_dump.py
================================================================================
"""

import sys
import json
import os

# Standalone or Ghidra Headless Environment Dual-Mode
IN_GHIDRA = 'currentProgram' in globals()

def ghidra_analysis():
    program = globals()['currentProgram']
    listing = program.getListing()
    memory = program.getMemory()
    string_table = program.getDefinedData(True)

    results = {
        "program_name": program.getName(),
        "creation_date": str(program.getCreationDate()),
        "language": str(program.getLanguageID()),
        "compiler": str(program.getCompilerSpec().getCompilerSpecID()),
        "min_address": str(program.getMinAddress()),
        "max_address": str(program.getMaxAddress()),
        "extracted_forensic_strings": []
    }

    keywords = [b".bat", b"cmd.exe", b"@echo", b"prompt \\b", b"temp.bat", b"batch_cmd", b"chrmapse"]

    for data in string_table:
        val = data.getValue()
        if val:
            val_str = str(val).lower()
            if any(k.decode() in val_str for k in keywords):
                results["extracted_forensic_strings"].append({
                    "address": str(data.getAddress()),
                    "length": data.getLength(),
                    "string": str(val)
                })

    out_file = os.path.join(os.getcwd(), program.getName() + "_ghidra_re.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print("[✓] Ghidra headless triage artifact exported: " + out_file)

def standalone_triage(filepath):
    print("=" * 70)
    print("Ghidra Headless Analyzer Helper (Standalone Emulation Mode)")
    print("Target: " + filepath)
    print("For full decompilation: execute with analyzeHeadless and -postScript")
    print("=" * 70)

if __name__ == "__main__":
    if IN_GHIDRA:
        ghidra_analysis()
    else:
        if len(sys.argv) > 1:
            standalone_triage(sys.argv[1])
        else:
            print("Usage in standalone mode: python ghidra_headless_dump.py <target_binary>")
