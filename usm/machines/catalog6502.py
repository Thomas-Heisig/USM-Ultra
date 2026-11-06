"""Curated upstream references: metadata only, no third-party code or ROMs."""
SOURCES = [
    {"id":"py65","name":"py65","category":"software_cpu","url":"https://github.com/mnaberez/py65","integration":"optional_dependency","hardware":False},
    {"id":"arlet6502","name":"Arlet 6502 Verilog","category":"fpga_cpu","url":"https://github.com/anders-code/arlet-6502","integration":"reference","hardware":True},
    {"id":"mister_apple2","name":"MiSTer Apple II","category":"system_reference","url":"https://github.com/MiSTer-devel/Apple-II_MiSTer","integration":"reference","hardware":True},
    {"id":"mister_c64","name":"MiSTer C64","category":"system_reference","url":"https://github.com/MiSTer-devel/C64_MiSTer","integration":"reference","hardware":True},
    {"id":"cc65","name":"cc65 compiler/assembler","category":"toolchain","url":"https://github.com/cc65/cc65","integration":"external_tool","hardware":False},
    {"id":"visual6502","name":"Visual6502","category":"research","url":"https://github.com/trebonian/visual6502","integration":"reference","hardware":False},
]
SYSTEMS = [
    {"id":"usm-6502","name":"USM 6502 SBC","cpu":"6502","status":"partial"},
    {"id":"apple1","name":"Apple I","cpu":"6502","status":"not_implemented"},
    {"id":"apple2","name":"Apple II","cpu":"6502","status":"not_implemented"},
    {"id":"pet","name":"Commodore PET","cpu":"6502","status":"not_implemented"},
    {"id":"vic20","name":"Commodore VIC-20","cpu":"6502","status":"not_implemented"},
    {"id":"c64","name":"Commodore 64","cpu":"6510","status":"not_implemented"},
    {"id":"atari800","name":"Atari 400/800","cpu":"6502","status":"not_implemented"},
    {"id":"bbc","name":"BBC Micro","cpu":"6502","status":"not_implemented"},
    {"id":"atari2600","name":"Atari 2600","cpu":"6507","status":"not_implemented"},
    {"id":"nes","name":"Nintendo NES","cpu":"Ricoh 2A03","status":"not_implemented"},
]
