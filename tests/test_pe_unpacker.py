#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bat2exe-ghidra-forensics :: Automated Test Suite for PE32 Unpacker
"""

import os
import sys
import unittest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from pe_stub_unpacker import PE32Bat2ExeUnpacker

class TestPE32Bat2ExeUnpacker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        cls.sample_exe = os.path.join(
            cls.base_dir,
            'references',
            'batch_corpus_28',
            'Bat2Exe-dehoisted',
            'Example',
            'example.exe'
        )

    def test_sample_exists(self):
        self.assertTrue(os.path.exists(self.sample_exe), f"Sample binary not found: {self.sample_exe}")

    def test_pe_header_parsing(self):
        unpacker = PE32Bat2ExeUnpacker(self.sample_exe)
        self.assertTrue(unpacker.is_pe, "File should be recognized as a valid PE binary")
        self.assertEqual(unpacker.metadata.get('magic'), 'PE32 (32-bit)')
        self.assertGreater(len(unpacker.sections), 0, "Sections list should not be empty")

    def test_packer_classification(self):
        unpacker = PE32Bat2ExeUnpacker(self.sample_exe)
        self.assertIn('.NET', unpacker.stub_type, "Packer stub should be classified as .NET assembly")

    def test_payload_recovery(self):
        unpacker = PE32Bat2ExeUnpacker(self.sample_exe)
        method, payload = unpacker.extract_payload()
        self.assertIsNotNone(payload, "Payload should be recovered from sample binary")
        self.assertIn("@echo off", payload.lower(), "Recovered script should contain batch command")
        self.assertGreater(len(payload), 100, "Payload length should exceed 100 characters")

if __name__ == '__main__':
    unittest.main()
