import pytest
from usm.machines.basic_console import BasicConsole

def test_basic_print_run():
    b=BasicConsole()
    b.submit("10 PRINT 2+3")
    assert b.submit("RUN")["output"][-1]=="5"

def test_basic_loop_and_if():
    b=BasicConsole()
    for line in ("10 LET A=0","20 LET A=A+1","30 IF A<3 THEN 20","40 PRINT A"):
        b.submit(line)
    assert b.submit("RUN")["output"][-1]=="3"

def test_basic_list_and_delete():
    b=BasicConsole()
    b.submit("10 PRINT 1")
    assert b.submit("LIST")["listing"]==["10 PRINT 1"]
    b.submit("10")
    assert b.submit("LIST")["listing"]==[]

def test_basic_rejects_python_code():
    b=BasicConsole()
    with pytest.raises(ValueError):
        b.submit('PRINT __IMPORT__("OS")')

def test_basic_loop_budget():
    b=BasicConsole()
    b.submit("10 GOTO 10")
    with pytest.raises(ValueError,match="limit"):
        b.run(12)
