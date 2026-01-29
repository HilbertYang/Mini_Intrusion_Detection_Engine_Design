# Hardware-Based Mini Intrusion Detection Engine

## Overview
This project implements a **hardware-based intrusion detection engine** that performs **real-time pattern matching on streaming packet data** and selectively drops malicious traffic.

The design demonstrates how **intrusion detection logic can be offloaded into hardware** to achieve deterministic timing and high-throughput packet processing, making it suitable for network security and data-plane acceleration use cases.

---

## Key Features
- **Parallel hardware pattern matching**
  - Byte-level comparisons with **mask / wildcard support**
  - Multiple packet offsets evaluated concurrently
- **Streaming packet processing**
  - Operates directly on packet data paths
  - Correct handling of packet headers and tails
- **Attack detection and packet dropping**
  - Detects predefined malicious signatures
  - Uses FIFO-based buffering to safely drop entire packets
- **Fully synchronous RTL design**
  - Clean separation of datapath and control logic
  - Deterministic, pipeline-friendly timing behavior

---

## Architecture
The design is composed of modular hardware blocks:

- **Data Aggregation**
  - Combines incoming packet data into a wide comparison bus
- **Comparator Array**
  - Masked byte-level comparators enabling wildcard matching
- **Match Qualification Logic**
  - Ensures detection occurs only on valid packet payloads
- **Drop Control & FIFO**
  - Buffers packets and prevents partial packet corruption during drops

Each block is independently testable and integrates into a streaming pipeline.

---

## Implementation Details
- Written in **Verilog HDL**
- Combines **schematic-based design** and hand-written RTL
- Utilizes reusable comparator and register modules
- Designed with synthesis and timing closure in mind

---

## Verification
- Verified using a cycle-accurate simulation environment
- Testbench injects normal and malicious packet streams
- Waveform inspection confirms:
  - Correct match detection timing
  - Proper assertion of drop signals
  - No corruption of non-malicious traffic
