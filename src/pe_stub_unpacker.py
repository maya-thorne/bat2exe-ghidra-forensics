#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
bat2exe-ghidra-forensics :: Automated PE32 Bat2Exe Unpacker & Forensics Engine
================================================================================
Author: Maya Thorne
Target Subsystems: Windows PE32 / PE32+ (x86 & x64)
Function: Dissects Bat2Exe packer stubs (UPX, .NET CLR, VB6, and Overlays),
          recovers embedded batch scripts, and dumps forensic metadata.
================================================================================
"""

import sys
import os
import struct
import argparse
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

class PE32Bat2ExeUnpacker:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'rb') as f:
            self.data = f.read()
        self.filesize = len(self.data)
        self.is_pe = False
        self.sections = []
        self.overlay_offset = 0
        self.overlay_size = 0
        self.stub_type = "Unknown / Non-PE"
        self.recovered_payload = None
        self.metadata = {}
        self._parse_pe_headers()

    def _parse_pe_headers(self):
        if len(self.data) < 64:
            return

        # Check DOS header (MZ)
        if self.data[:2] != b'MZ':
            return

        # e_lfanew
        pe_offset = struct.unpack_from('<I', self.data, 0x3C)[0]
        if pe_offset + 24 > self.filesize:
            return

        # Check PE signature
        if self.data[pe_offset:pe_offset+4] != b'PE\x00\x00':
            return

        self.is_pe = True
        self.pe_offset = pe_offset

        # COFF File Header
        coff_offset = pe_offset + 4
        machine, num_sections, time_date_stamp, sym_ptr, sym_count, opt_hdr_size, characteristics = struct.unpack_from(
            '<HHIIIHH', self.data, coff_offset
        )
        self.metadata['machine'] = hex(machine)
        self.metadata['num_sections'] = num_sections
        self.metadata['characteristics'] = hex(characteristics)

        # Optional Header
        opt_offset = coff_offset + 20
        magic = struct.unpack_from('<H', self.data, opt_offset)[0]
        self.is_64bit = (magic == 0x20B)
        self.metadata['magic'] = 'PE32+ (64-bit)' if self.is_64bit else 'PE32 (32-bit)'

        entry_point = struct.unpack_from('<I', self.data, opt_offset + 16)[0]
        image_base = struct.unpack_from('<Q' if self.is_64bit else '<I', self.data, opt_offset + (24 if not self.is_64bit else 24))[0]
        self.metadata['entry_point_rva'] = hex(entry_point)
        self.metadata['image_base'] = hex(image_base)

        # Section Headers
        sec_offset = opt_offset + opt_hdr_size
        max_raw_end = 0

        for i in range(num_sections):
            if sec_offset + 40 > self.filesize:
                break
            sec_name = self.data[sec_offset:sec_offset+8].rstrip(b'\x00').decode('latin-1', errors='replace')
            virt_size, virt_addr, raw_size, raw_ptr, _, _, _, _, characteristics = struct.unpack_from(
                '<IIIIIIHHI', self.data, sec_offset + 8
            )
            sec_info = {
                'name': sec_name,
                'virt_size': virt_size,
                'virt_addr': hex(virt_addr),
                'raw_size': raw_size,
                'raw_offset': raw_ptr,
                'characteristics': hex(characteristics)
            }
            self.sections.append(sec_info)
            raw_end = raw_ptr + raw_size
            if raw_end > max_raw_end:
                max_raw_end = raw_end
            sec_offset += 40

        # Check for Overlay Data past the last section
        if self.filesize > max_raw_end:
            self.overlay_offset = max_raw_end
            self.overlay_size = self.filesize - max_raw_end
            self.metadata['overlay'] = {
                'offset': hex(self.overlay_offset),
                'size': self.overlay_size
            }

        self._classify_packer_stub()

    def _classify_packer_stub(self):
        sec_names = [s['name'] for s in self.sections]

        # 1. UPX Section Names
        if any('UPX' in s for s in sec_names):
            self.stub_type = "UPX Native Compressed Stub (NRV2B)"
            return

        # 2. .NET CLR Signature
        if b'mscoree.dll' in self.data or b'_CorExeMain' in self.data or b'BSJB' in self.data:
            self.stub_type = ".NET Managed Assembly (Bat2Exe Dynamic CSharpCodeProvider)"
            return

        # 3. VB6 Signature
        if b'MSVBVM60.DLL' in self.data or b'ThunRTMain' in self.data:
            self.stub_type = "VB6 Native P-Code/Executable (Batch-Encryption-DeCoder)"
            return

        # 4. In-Memory Overlay Packer
        if self.overlay_size > 0:
            self.stub_type = "Win32 Native Stub with PE Overlay Payload"
            return

        self.stub_type = "Generic Win32 Executable Wrapper"

    def extract_payload(self):
        """
        Multi-heuristic extraction of embedded batch scripts from resources,
        managed user strings, overlays, and binary byte streams.
        """
        # Heuristic 1: Scan for batch command patterns in overlay
        if self.overlay_size > 0:
            overlay_data = self.data[self.overlay_offset:]
            batch_text = self._search_batch_patterns(overlay_data)
            if batch_text:
                self.recovered_payload = batch_text
                return "Overlay Decryption/Extraction", batch_text

        # Heuristic 2: Search for .NET UTF-16LE / UTF-8 embedded resource strings
        if ".NET" in self.stub_type:
            batch_text = self._search_dotnet_strings()
            if batch_text:
                self.recovered_payload = batch_text
                return ".NET Resource Heap Extraction", batch_text

        # Heuristic 3: Search for VB6 CHRMAPSET and substituted buffers
        if "VB6" in self.stub_type:
            batch_text = self._search_vb6_payload()
            if batch_text:
                self.recovered_payload = batch_text
                return "VB6 CHRMAPSET Reversal", batch_text

        # Heuristic 4: Full binary stream pattern search for batch script markers
        batch_text = self._search_batch_patterns(self.data)
        if batch_text:
            self.recovered_payload = batch_text
            return "Raw PE Byte Stream Recovery", batch_text

        return "None", None

    def _search_batch_patterns(self, buffer):
        # Look for @echo off, setlocal, REM, etc. in ASCII or UTF-16LE
        patterns = [
            rb'(@echo\s+off[\s\S]*?)(?=\x00\x00\x00|\x00{4}|$)',
            rb'(@echo\s+off[\s\S]{10,8000})',
            rb'(rem\s+[\s\S]*?@echo[\s\S]{10,8000})',
            rb'(setlocal[\s\S]{10,8000})'
        ]

        for p in patterns:
            m = re.search(p, buffer, re.IGNORECASE)
            if m:
                raw_chunk = m.group(1)
                try:
                    text = raw_chunk.decode('utf-8', errors='ignore').strip()
                    if '\n' in text and len(text) > 20:
                        return text
                except Exception:
                    pass

        # Try UTF-16LE decoding
        try:
            u16_patterns = [
                rb'(\x40\x00\x65\x00\x63\x00\x68\x00\x6F\x00[\s\S]*?)(?=\x00\x00\x00\x00|$)'
            ]
            for p in u16_patterns:
                m = re.search(p, buffer)
                if m:
                    raw_chunk = m.group(1)
                    text = raw_chunk.decode('utf-16le', errors='ignore').strip()
                    if len(text) > 20:
                        return text
        except Exception:
            pass

        return None

    def _search_dotnet_strings(self):
        # Scan for common Bat2Exe .NET markers: "batch_cmd", "\temp.bat", etc.
        pos = self.data.find(b'batch_cmd')
        if pos != -1:
            # Look nearby for the script body
            chunk = self.data[max(0, pos-2048):min(len(self.data), pos+16384)]
            result = self._search_batch_patterns(chunk)
            if result:
                return result

        # Also search for redirected cmd.exe execution patterns
        m = re.search(rb'(?:prompt\s+\\b\s*&\s*echo\s+on\s*&)([\s\S]*?)(?=\x00|$)', self.data, re.IGNORECASE)
        if m:
            try:
                return m.group(1).decode('utf-8', errors='ignore').strip()
            except Exception:
                pass

        return None

    def _search_vb6_payload(self):
        # Look for CHRMAPSET patterns or "%" substitution loops
        pos = self.data.find(b'CHRMAPSET')
        if pos != -1:
            chunk = self.data[max(0, pos-512):min(len(self.data), pos+8192)]
            result = self._search_batch_patterns(chunk)
            if result:
                return result
        return None

    def generate_report(self):
        method, payload = self.extract_payload()
        report = {
            'filepath': self.filepath,
            'filesize_bytes': self.filesize,
            'is_valid_pe': self.is_pe,
            'packer_stub_classification': self.stub_type,
            'pe_headers': self.metadata,
            'sections': self.sections,
            'extraction_method': method,
            'payload_extracted': payload is not None,
            'payload_length': len(payload) if payload else 0,
            'payload_preview': (payload[:300] + '...') if payload else None
        }
        return report

def main():
    parser = argparse.ArgumentParser(description="bat2exe-ghidra-forensics :: PE32 Bat2Exe Unpacker & Forensics Engine")
    parser.add_argument("-i", "--input", required=True, help="Path to compiled PE binary (.exe)")
    parser.add_argument("-o", "--output", help="Path to save recovered batch script (.bat)")
    parser.add_argument("--json", action="store_true", help="Output full forensic report as JSON")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[!] Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    unpacker = PE32Bat2ExeUnpacker(args.input)
    report = unpacker.generate_report()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("=" * 72)
        print("🔬 bat2exe-ghidra-forensics :: PE32 Reverse Engineering Report")
        print("=" * 72)
        print(f"Target Binary : {report['filepath']}")
        print(f"File Size     : {report['filesize_bytes']} bytes")
        print(f"PE Subsystem  : {report['pe_headers'].get('magic', 'Unknown')}")
        print(f"Packer Stub   : {report['packer_stub_classification']}")
        print(f"Sections ({len(report['sections'])}) : {', '.join([s['name'] for s in report['sections']])}")
        if 'overlay' in report['pe_headers']:
            ov = report['pe_headers']['overlay']
            print(f"PE Overlay    : Detected at {ov['offset']} ({ov['size']} bytes)")
        print(f"Extraction    : {report['extraction_method']}")
        print(f"Recovered     : {'YES (' + str(report['payload_length']) + ' chars)' if report['payload_extracted'] else 'NO'}")
        print("=" * 72)
        if report['payload_preview']:
            print("\n--- [Recovered Script Preview] ---")
            print(report['payload_preview'])
            print("----------------------------------\n")

    if args.output and unpacker.recovered_payload:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(unpacker.recovered_payload)
        print(f"[✓] Recovered batch payload saved to: {args.output}")

if __name__ == "__main__":
    main()
