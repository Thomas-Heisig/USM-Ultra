"""Regression contract tests for the virtual USM matrix (no native CPU dependency)."""
import threading
import pytest
from usm.core import Matrix, Mapping, RAM, Transaction, VirtualCPU
from usm.advanced import AtomicTaskQueue, WindowManager, MiniM68K

def matrix_with_ram():
    matrix = Matrix()
    matrix.map(Mapping(0, 4096, RAM(4096), "ram"))
    return matrix

@pytest.mark.parametrize("width,value", [(1, 0x12), (2, 0x1234), (4, 0x12345678)])
def test_big_endian_round_trip(width, value):
    m = matrix_with_ram()
    assert m.transact(Transaction("cpu", 0x100, width, True, value)).error is None
    assert m.transact(Transaction("cpu", 0x100, width)).value == value
    assert bytes(m.mappings[0].device.data[0x100:0x100 + width]) == value.to_bytes(width, "big")

@pytest.mark.parametrize("width", [0, 3, 5])
def test_unsupported_width(width):
    assert matrix_with_ram().transact(Transaction("cpu", 0, width)).error is not None

@pytest.mark.parametrize("address,width", [(4096,1), (4095,2), (0x100000,1)])
def test_decode_fault(address, width):
    assert matrix_with_ram().transact(Transaction("cpu", address, width)).error is not None

def test_permission_fault():
    m = Matrix()
    m.map(Mapping(0, 32, RAM(32), "rom", write=False))
    assert m.transact(Transaction("cpu", 0, 1, True, 1)).error is not None

def test_rom_write_fault():
    m = Matrix()
    m.map(Mapping(0, 32, RAM(32, readonly=True), "rom"))
    assert m.transact(Transaction("cpu", 0, 1, True, 1)).error is not None

@pytest.mark.parametrize("width", [2,4])
def test_m68000_odd_address_error(width):
    cpu = VirtualCPU("m68k", "m68000", matrix_with_ram())
    assert "address error" in cpu.access(1, width).error

def test_z80_does_not_inherit_m68000_alignment():
    cpu = VirtualCPU("z80", "z80", matrix_with_ram())
    assert cpu.access(1, 2).error is None

def test_generation_commit_and_reject():
    m = Matrix()
    wm = WindowManager(m)
    first = Mapping(0, 64, RAM(64), "a")
    assert wm.replace([first], 0) == 1
    assert wm.generation == 1
    with pytest.raises(ValueError, match="stale"):
        wm.replace([], 0)
    assert wm.generation == 1
    assert m.mappings[0] is first

def test_generation_failed_overlap_is_not_visible():
    m = Matrix()
    wm = WindowManager(m)
    wm.replace([Mapping(0, 64, RAM(64), "old")], 0)
    with pytest.raises(ValueError):
        wm.replace([Mapping(0, 32, RAM(32), "a"), Mapping(16, 32, RAM(32), "b")], 1)
    assert wm.generation == 1
    assert m.mappings[0].name == "old"

def test_task_concurrent_unique_ownership():
    queue = AtomicTaskQueue()
    for _ in range(60):
        queue.submit("m68000")
    barrier = threading.Barrier(12)
    grants = []
    lock = threading.Lock()
    def worker(index):
        barrier.wait()
        local = []
        for _ in range(8):
            lease = queue.claim(f"w{index}", {"m68000"})
            if lease is not None:
                local.append(lease.task_id)
        with lock:
            grants.extend(local)
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(12)]
    for thread in threads: thread.start()
    for thread in threads: thread.join(timeout=5)
    assert all(not thread.is_alive() for thread in threads)
    assert len(grants) == 60
    assert len(set(grants)) == 60

def test_fake_clock_expiry_requeue():
    now = [10.0]
    queue = AtomicTaskQueue(clock=lambda: now[0])
    task = queue.submit("any")
    assert queue.claim("a", {"any"}, ttl=5).task_id == task
    now[0] = 16.0
    assert queue.claim("b", {"any"}).task_id == task
    with pytest.raises(PermissionError):
        queue.complete(task, "a")

def test_trace_ring_is_bounded():
    m = matrix_with_ram()
    for _ in range(4100):
        m.transact(Transaction("cpu", 0))
    assert len(m.trace) == 4096

def test_mini_core_rejects_unsupported_opcode():
    m = matrix_with_ram()
    m.mappings[0].device.data[:2] = bytes.fromhex("ffff")
    with pytest.raises(NotImplementedError):
        MiniM68K(m).step()
