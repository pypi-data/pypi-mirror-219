from sallron.enforcer import *
import os
import pytest

# TODO: test discord message in a separate channel

def test_write_pid():
    write_pid('1234')

def test_kill_pid():
    kill_pid(delete_file=True)

def test_pid_cycle():
    write_pid('1234')
    kill_pid(delete_file=True)
    
def test_eternal_runner():
    os.popen('echo "print()" > test_program.py')
    write_pid('1234')
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        eternal_runner(filepath="test_program.py", test=True)
    assert pytest_wrapped_e.type == SystemExit