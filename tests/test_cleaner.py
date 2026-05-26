import os
import pytest
from core.cleaner import get_junk_paths, clean_junk

def test_get_junk_paths():
    paths = get_junk_paths()
    assert isinstance(paths, list)
    # On Windows, at least one path should be found (TEMP)
    if os.name == 'nt':
        assert len(paths) > 0

def test_clean_junk_safe_run():
    """
    Test cleaner with a mock directory to ensure it doesn't delete real system files 
    but correctly identifies files to delete.
    """
    import tempfile
    import shutil
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some junk
        junk_file = os.path.join(tmpdir, "test_junk.tmp")
        with open(junk_file, "w") as f:
            f.write("junk data")
            
        junk_subdir = os.path.join(tmpdir, "junk_dir")
        os.makedirs(junk_subdir)
        
        # Mock get_junk_paths to only return our temp dir
        from unittest.mock import patch
        with patch('core.cleaner.get_junk_paths', return_value=[tmpdir]):
            deleted_count, saved_bytes = clean_junk()
            
            assert deleted_count >= 1
            assert saved_bytes > 0
            assert not os.path.exists(junk_file)
            # shutil.rmtree might fail if files are open, but in this test it should work
            # Note: clean_junk cleans contents, then tries to remove dirs
