<div align="center">

<p align="center">
  <a href="../../README.md">🇺🇸 English</a> · <a href="./ko.md">🇰🇷 한국어</a> · <a href="./zh-CN.md">🇨🇳 中文</a> · <a href="./es.md">🇪🇸 Español</a> · <a href="./hi.md">🇮🇳 हिन्दी</a><br />
  <a href="./ar.md">🇸🇦 العربية</a> · <a href="./pt-BR.md">🇧🇷 Português</a> · <a href="./ru.md">🇷🇺 Русский</a> · <strong>🇫🇷 Français</strong> · <a href="./id.md">🇮🇩 Bahasa Indonesia</a>
</p>

<p align="center">
  <a href="https://github.com/maya-thorne/bat2exe-ghidra-forensics"><img src="../assets/locales/fr/banner.svg" alt="bat2exe-ghidra-forensics banner" width="100%" /></a>
</p>

# 🔬 bat2exe-ghidra-forensics

**Rétro-Ingénierie Ghidra des Packers Bat2Exe et Dissection du Code Source d’Obfuscation Batch**

[![Ghidra MCP RE](https://img.shields.io/badge/Ghidra_MCP-PE32_Binary_Disassembly-f43f5e.svg)](../../DEEP_REVERSE_ENGINEERING_AND_SOURCE_ANALYSIS.md)
[![8 Core Dissections](https://img.shields.io/badge/Source_Teardown-8_Obfuscators_%26_Hookers-f59e0b.svg)](../../BATCH_OBFUSCATION_ARCHITECTURE_AND_CODE_ANALYSIS.md)
[![Deobfuscator Engine](https://img.shields.io/badge/Engine-Python_Multi--Pass_AST-38bdf8.svg)](../../src/deobfuscator_engine.py)
[![Sigma & YARA](https://img.shields.io/badge/Detection-Sigma_%26_YARA_Rules-10b981.svg)](../../04_탐지규칙_및_자체엔진/rules)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

<sub>Engineered &amp; Audited by **[Maya Thorne](https://github.com/maya-thorne)** · Binary Forensics &amp; Systems Reverse Engineering</sub>

</div>

---

## 📑 Executive Summary & Master Whitepapers (핵심 역공학 백서 색인)

| # | Document / Artifact | Core Scope & Forensic Coverage | Size |
| :-: | :--- | :--- | :-: |
| **1** | 🔬 **[DEEP_REVERSE_ENGINEERING_AND_SOURCE_ANALYSIS.md](../../DEEP_REVERSE_ENGINEERING_AND_SOURCE_ANALYSIS.md)** | **Ghidra MCP PE Binary Disassembly** (`bat2exe_12.exe`, `example.exe`, `BEDeCode.exe`) + **Line-by-Line Source Code Teardown of 8 Core Tools** (`Bat2Exe-dehoisted`, `Batch-Encryption-DeCoder`, `BatCloak`, `Invoke-DOSfuscation`, `SomalifuscatorV2`, `0xidiz3r`, `batch_deobfuscator`, `Exorcism`) | **42.8 KB** |
| **2** | 🏗️ **[BATCH_OBFUSCATION_ARCHITECTURE_AND_CODE_ANALYSIS.md](../../BATCH_OBFUSCATION_ARCHITECTURE_AND_CODE_ANALYSIS.md)** | **Architectural Taxonomy & Parser Mechanics**: `cmd.exe` 5-Phase Expansion Order, Polyglot Header Exploitation, Pushdown Automaton AST Reconstruction, API Hooking (`FindFixAndRun`) | **43.7 KB** |
| **3** | ⚙️ **[GHIDRA_BINARY_RE_AND_DEOBFUSCATOR_ENGINE_ANALYSIS.md](../../GHIDRA_BINARY_RE_AND_DEOBFUSCATOR_ENGINE_ANALYSIS.md)** | **Static & Dynamic Unpacking Pipeline**: PE Overlay Extraction, CLR `#US` Stream Recovery, Multi-Pass Regex/AST Deobfuscation Engine (`src/deobfuscator_engine.py`) | **44.4 KB** |
| **4** | 📖 **[BATCH_OBFUSCATION_ENCYCLOPEDIA.md](../../BATCH_OBFUSCATION_ENCYCLOPEDIA.md)** | **48+ Open-Source & Hugging Face Reference Encyclopedia**: Complete classification of obfuscators, compilers, deobfuscators, and ML datasets | **30.3 KB** |
| **5** | 🛡️ **[BATCH_OBFUSCATION_MASTER_GUIDE.md](../../BATCH_OBFUSCATION_MASTER_GUIDE.md)** | **30-Year Evolution (1990s–2026) & Defense Matrix**: Historical timeline, Mandiant/Unit 42 threat intelligence, production Sigma & YARA rulesets | **33.6 KB** |

---

## 🖥️ Live Forensics & Decompilation Terminal Demo

<p align="center">
  <a href="https://github.com/maya-thorne/bat2exe-ghidra-forensics">
    <img src="../../docs/assets/diagrams/ghidra_re_terminal_demo.svg" alt="Ghidra RE Live Terminal Demo" width="100%" />
  </a>
</p>

---

## 🧬 End-to-End Binary Packing & Deobfuscation Topology

```mermaid
flowchart TD
    subgraph "Layer 1: Source-Level Batch Obfuscation"
        S1["Plaintext Batch (.bat / .cmd)"] --> O1["Invoke-DOSfuscation\nEnv Slicing & Reversed FOR Loop"]
        S1 --> O2["BatCloak / Batch-Encryption-DeCoder\nUTF-16LE BOM (0xFF 0xFE &cls) & CHRMAPSET"]
        S1 --> O3["SomalifuscatorV2 & 0xidiz3r\nDynamic Caesar Cipher & 3-Seed Zero-Literal"]
    end

    subgraph "Layer 2: Bat2Exe Binary Compilation (Ghidra MCP Targets)"
        O1 & O2 & O3 --> P1["bat2exe_12.exe (PE32 Native UPX)\nEntry RVA 0x20ea0: PUSHAD -> NRV2B Unpack -> JMP 0x12475"]
        O1 & O2 & O3 --> P2["example.exe (PE32 .NET CLR)\nEntry RVA 0x337e: FF 25 00 20 40 00 -> _CorExeMain\nMethod1 (%TEMP% Drop) vs Method2 (Fileless StandardInput Pipe)"]
        O1 & O2 & O3 --> P3["BEDeCode.exe (PE32 VB6 Native)\nEntry RVA 0x1670: PUSH 0x401968 -> ThunRTMain (MSVBVM60.DLL)"]
    end

    subgraph "Layer 3: Forensic Extraction & Deobfuscation Engine"
        P1 & P2 & P3 --> D1["Ghidra MCP Binary Triage & Disassembly\n(re_triage_binary / re_search_strings / re_disassemble_offset)"]
        D1 --> D2["src/pe_stub_unpacker.py & src/deobfuscator_engine.py\nAutomated PE32 Dissector & AST Pushdown Automaton"]
        D1 --> D3["Exorcism (cmd.exe Runtime Detour)\ncmd.exe!FindFixAndRun (RVA 0x116B0) In-Memory Interceptor"]
        D2 & D3 --> R1["Recovered Plaintext Script + Sigma/YARA Signatures"]
    end
```

---

## ⚙️ Automated PE32 Bat2Exe Unpacking Pipeline

<p align="center">
  <a href="https://github.com/maya-thorne/bat2exe-ghidra-forensics">
    <img src="../../docs/assets/diagrams/pe_stub_unpacking_pipeline.svg" alt="PE Stub Unpacking Pipeline" width="100%" />
  </a>
</p>

---

## 🔬 x86 Execution State & UPX NRV2B Register Transition Matrix

<p align="center">
  <a href="https://github.com/maya-thorne/bat2exe-ghidra-forensics">
    <img src="../../docs/assets/diagrams/x86_register_schematic.svg" alt="x86 Register Schematic" width="100%" />
  </a>
</p>

---

## 🔍 Ghidra MCP Binary Reverse Engineering Matrix (`ghidra-re-operator`)

All 3 compiled PE32 executables in the archive were dissected using `re_triage_binary`, `re_search_strings`, and `re_disassemble_offset`:

| Target Binary | Architecture & Subsystem | Entry Point RVA | Sections & Entropy | Key Disassembly & Runtime Mechanism |
| :--- | :--- | :-: | :--- | :--- |
| **`bat2exe_12.exe`** | PE32 x86 (32-bit) · Windows GUI (`2`) | `0x20ea0` | `UPX0` (Virt `0x17000`, Raw `0`), `UPX1` (7.89 bits/byte), `.rsrc` | `0x20ea0: PUSHAD` ➔ `MOV ESI, 0x417000` ➔ `LEA EDI, [ESI - 0x16000]` ➔ NRV2B bit-stream decompression loop ➔ IAT rebuild (`LoadLibraryA`/`GetProcAddress`) ➔ `0x20ffd: JMP 0x00412475` (OEP). |
| **`example.exe`** (`Bat2Exe-dehoisted`) | PE32 x86 (.NET CLR Managed) · Windows CUI (`3`) | `0x337e` | `.text` (5.64), `.rsrc` (3.99), `.reloc` (0.18) | `0x337e: FF 25 00 20 40 00 (JMP dword ptr [0x00402000])` ➔ `mscoree.dll!_CorExeMain`. Embeds UTF-16LE user strings at `0x143b` (`"batch_cmd"`), `0x1465` (`"\\temp.bat"`), `0x1541` (`"/c prompt \b & echo on"`). |
| **`BEDeCode.exe`** (`Batch-Encryption-DeCoder`) | PE32 x86 (VB6 Native Code) · Windows GUI (`2`) | `0x1670` | `.text` (5.43), `.data` (0.00), `.rsrc` (3.55) | `0x1670: 68 68 19 40 00 (PUSH 0x401968)` ➔ `E8 EF FF FF FF (CALL ThunRTMain)` in `MSVBVM60.DLL`. Implements `CmdCode_Click` (`%%a` + `CHRMAPSET` substitution) and `CmdDeCode_Click` (`Replace(txt, "%", "")`). |

---

## 🛠️ 8 Core Tools Source Code Dissection Summary

1. **[`Bat2Exe-dehoisted`](../../01_배치난독화_GitHub_28종/Compilations_And_Packers/Bat2Exe-dehoisted)** (`Batch2Exe.MainWindow` & `CMethods.cs`):
   - Uses `CSharpCodeProvider.CompileAssemblyFromSource` to dynamically compile an in-memory stub with embedded resource `batch_cmd`.
   - Compares **`Method1` (Disk Drop to `%TEMP%\temp.bat`)** vs **`Method2` (Fileless Pipe Injection via `RedirectStandardInput = true` + `StandardInput.WriteLine`)**.
2. **[`Batch-Encryption-DeCoder`](../../01_배치난독화_GitHub_28종/Deobfuscators_And_Unpackers/Batch-Encryption-DeCoder)** (`frmMain.frm`):
   - Dissects the VB6 `CHRMAPSET` lookup table, `@echo off & SetLocal EnableDelayedExpansion` header validation, and 2-stage reversal algorithm.
3. **[`BatCloak`](../../01_배치난독화_GitHub_28종/Obfuscators/BatCloak)**:
   - Exploits the **UTF-16LE BOM Polyglot (`0xFF 0xFE 26 63 6C 73 0D 0A` = `??&cls`)**: text editors decode garbage CJK glyphs while `cmd.exe` runs in Single-Byte ANSI mode, fails on `0xFF 0xFE`, executes `&cls`, and evaluates the remainder.
4. **[`Invoke-DOSfuscation`](../../01_배치난독화_GitHub_28종/Obfuscators/Invoke-DOSfuscation)** (Mandiant / Daniel Bohannon):
   - Formalizes `cmd.exe` AST token-layer vs character-layer obfuscation, zero-alphabetic environment slicing (`%COMSPEC:~-1%`), and reversed `FOR /L` execution loops.
5. **[`SomalifuscatorV2`](../../01_배치난독화_GitHub_28종/Obfuscators/SomalifuscatorV2)**:
   - Combines dynamic Caesar cipher environment tables, UTF-16LE BOM headers, fake `certutil` X.509 certificate padding, and anti-VM/anti-sandbox traps.
6. **[`0xidiz3r`](../../01_배치난독화_GitHub_28종/Obfuscators/0xidiz3r)** (Rust):
   - Bootstraps the entire ASCII printable set from only **3 initial seed characters (`@`, `~`, `=`)** using `%=exitcodeAscii%` and `cmd /c exit /b <N>`.
7. **[`batch_deobfuscator`](../../01_배치난독화_GitHub_28종/Deobfuscators_And_Unpackers/batch_deobfuscator)** (DissectMalware):
   - Implements a **Single-Character Pushdown Automaton (PDA)** state machine in `BatchDeobfuscator.read_logical_line()` and full `%var:str1=str2%` / `%var:~start,len%` emulation.
8. **[`Exorcism`](../../01_배치난독화_GitHub_28종/Runtime_Hook_And_Monitor/Exorcism)**:
   - Injects `payload_dll.dll` into `cmd.exe` and hooks the internal command dispatcher **`FindFixAndRun` (RVA `0x116B0`)** via MS Detours to intercept every expanded command node right before execution.

---

## 🚀 Quickstart: Running the Automated Forensics & Unpacker Engine

```bash
# 1. Automated PE32 Bat2Exe unpacker and payload extractor
python src/pe_stub_unpacker.py --input "01_배치난독화_GitHub_28종/Bat2Exe-dehoisted/Example/example.exe" --output "recovered.bat"

# 2. Run the 6-pass static batch deobfuscator & PE overlay analyzer
python src/deobfuscator_engine.py --input "03_고전_및_실전_연구샘플/samples/05_layered_complex_obf.bat"
```


---

## 📂 Repository Directory Structure

- 📄 [`DEEP_REVERSE_ENGINEERING_AND_SOURCE_ANALYSIS.md`](../../DEEP_REVERSE_ENGINEERING_AND_SOURCE_ANALYSIS.md) — Complete Ghidra MCP binary disassembly & 8-tool source code teardown.
- 📄 [`BATCH_OBFUSCATION_ARCHITECTURE_AND_CODE_ANALYSIS.md`](../../BATCH_OBFUSCATION_ARCHITECTURE_AND_CODE_ANALYSIS.md) — `cmd.exe` parser internals & architectural code analysis.
- 📄 [`GHIDRA_BINARY_RE_AND_DEOBFUSCATOR_ENGINE_ANALYSIS.md`](../../GHIDRA_BINARY_RE_AND_DEOBFUSCATOR_ENGINE_ANALYSIS.md) — PE overlay unpacking & static AST deobfuscator engine design.
- 📁 [`src/`](../../src) — Executable Python multi-pass deobfuscator engine (`deobfuscator_engine.py`).
- 📁 [`01_배치난독화_GitHub_28종/`](../../01_배치난독화_GitHub_28종) — Flattened source code trees of 40+ open-source obfuscators, deobfuscators, runtime hookers, and Bat2Exe packers.
- 📁 [`02_HuggingFace_AI_자원/`](../../02_HuggingFace_AI_자원) — Hugging Face AI deobfuscation metadata, JFrog Token Entropy Dataset (ArXiv:2510.26847), EDR telemetry & SigmaForge rules.
- 📁 [`03_고전_및_실전_연구샘플/`](../../03_고전_및_실전_연구샘플) — Step-by-step obfuscated/deobfuscated PoC samples & BatCloak 3-stage forensic deep dive.
- 📁 [`04_탐지규칙_및_자체엔진/`](../../04_탐지규칙_및_자체엔진) — Production Sigma & YARA detection rulesets and PE binary forensic index (`pe_binaries.json`).
