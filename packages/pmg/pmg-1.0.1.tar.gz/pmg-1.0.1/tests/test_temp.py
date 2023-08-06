import os
import shutil
import pmg.temp

def test_tempdir():
    with pmg.temp.tempdir() as path:
        assert os.path.isdir(path)
    assert not os.path.isdir(path)
    with pmg.temp.tempdir(remove_upon_completion=False) as path:
        assert os.path.isdir(path)
    assert os.path.isdir(path)
    shutil.rmtree(path)
    assert not os.path.isdir(path)
