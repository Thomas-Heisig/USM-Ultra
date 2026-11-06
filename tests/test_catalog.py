import pytest
from usm.catalog import components, component, summary

def test_catalog_has_planned_chips():
    ids = {c["id"] for c in components()}
    assert {"m68000", "z80", "mos6502", "sid6581", "paula", "agnus", "denise", "vicii", "wd1772"} <= ids

def test_stub_is_not_full_emulation():
    m = component("m68000")
    assert m["implementation"] == "stub"
    assert m["available_virtual"] is False

def test_virtual_ram_is_available():
    assert component("ram")["available_virtual"] is True

def test_hardware_unknown_not_false_claim():
    assert all(c["hardware"] == "not_probed" for c in components())
    assert summary()["hardware_present"] == 0

def test_filter_by_family():
    assert all(c["family"] == "CPU" for c in components("cpu"))

def test_unknown_chip():
    assert component("no-such-chip") is None

def test_summary_consistent():
    s = summary()
    assert s["emulated"] + s["stub"] + s["not_implemented"] == s["total"]

def test_dependencies_are_explicit():
    assert "agnus" in component("paula")["dependencies"]
