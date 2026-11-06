import threading
import pytest
from usm.core import Matrix, RAM, Mapping, Transaction
from usm.advanced import WindowManager, AtomicTaskQueue, RomLibrary, MiniM68K

def test_windows():
    m=Matrix(); w=WindowManager(m); r=RAM(128)
    assert w.replace([Mapping(0,128,r,"ram")],0)==1
    with pytest.raises(ValueError): w.replace([],0)
    with pytest.raises(ValueError): w.replace([Mapping(0,80,r,"a"),Mapping(40,80,r,"b")],1)

def test_memory():
    m=Matrix();m.map(Mapping(0,16,RAM(16),"ram"))
    assert m.transact(Transaction("cpu",0,2,True,0x1234)).error is None
    assert m.transact(Transaction("cpu",0,2)).value==0x1234
    assert m.transact(Transaction("cpu",32)).error=="unmapped address"

def test_concurrent_claim():
    q=AtomicTaskQueue();q.submit("m68000"); results=[]
    def claim(i):results.append(q.claim(str(i),{"m68000"}))
    threads=[threading.Thread(target=claim,args=(i,)) for i in range(20)]
    for t in threads:t.start()
    for t in threads:t.join()
    assert len([r for r in results if r is not None])==1

def test_lease():
    now=[0.0];q=AtomicTaskQueue(lambda:now[0]);tid=q.submit("any")
    q.claim("a",{"any"},ttl=2);now[0]=3
    assert q.claim("b",{"any"}).task_id==tid
    with pytest.raises(PermissionError):q.complete(tid,"a")

def test_rom(tmp_path):
    root=tmp_path/"roms";root.mkdir();(root/"test.rom").write_bytes(b"abc")
    result=RomLibrary(root).inventory(tmp_path/"rom_manifest.json")
    assert len(result)==1 and result[0]["bytes"]==3

def test_m68k_machine_code():
    code=bytes.fromhex("702a 23c0 00000100 2239 00000100 4e72 2700")
    m=Matrix();ram=RAM(1024);ram.data[:len(code)]=code;m.map(Mapping(0,1024,ram,"ram"))
    result=MiniM68K(m).run()
    assert result["stopped"] and result["d"][1]==42
