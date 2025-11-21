import sys
import os
import pytest
import time
import psutil

# Add the workspace root to sys.path to import MemoryLeak
# Assuming the test file is in Ana Simülasyon/tests/
# and MemoryLeak.py is in the workspace root (../../)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from MemoryLeak import EVChargingStation
except ImportError:
    # If running from a different context, try to find the file
    # This is a fallback for different environment setups
    sys.path.append(os.getcwd())
    try:
        from MemoryLeak import EVChargingStation
    except ImportError:
        raise ImportError("Could not import MemoryLeak.py. Please ensure it exists in the workspace root.")

class TestMemoryLeakAnomaly:
    
    @pytest.fixture
    def station(self):
        """Fixture to create a fresh station instance for each test."""
        return EVChargingStation()

    def test_normal_operation_memory_stability(self, station):
        """
        Test that normal operation does not cause significant memory growth.
        Reference: MemoryLeak.py normal_operation
        """
        print("\nTesting Normal Operation...")
        
        # Force garbage collection before starting to get a clean baseline
        import gc
        gc.collect()
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Run normal operation for a few cycles
        # In normal mode, data (2MB) is created and then discarded.
        iterations = 5
        for _ in range(iterations):
            station.normal_operation()
            
        gc.collect()
        final_memory = process.memory_info().rss
        
        growth = final_memory - initial_memory
        print(f"Normal Operation Memory Growth: {growth / 1024 / 1024:.2f} MB")
        
        # We expect growth to be minimal. 
        # 5 iterations * 2MB = 10MB if leaked.
        # We assert that growth is significantly less than what would be leaked.
        # Allowing 2MB overhead for python objects etc.
        assert growth < 2 * 1024 * 1024, "Memory grew significantly in normal mode, possible leak or unstable baseline"
        assert len(station.session_logs) == 0, "Session logs should be empty in normal mode"

    def test_leak_operation_memory_growth(self, station):
        """
        Test that anomalous operation causes memory growth.
        Reference: MemoryLeak.py anomalous_operation
        """
        print("\nTesting Leak Operation...")
        
        import gc
        gc.collect()
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Run leak operation for a few cycles
        # In leak mode, data (5MB) is appended to session_logs.
        iterations = 3
        data_size_mb = 5
        for _ in range(iterations):
            station.anomalous_operation()
            
        final_memory = process.memory_info().rss
        growth = final_memory - initial_memory
        print(f"Leak Operation Memory Growth: {growth / 1024 / 1024:.2f} MB")
        
        # Expected growth: ~15MB (3 * 5MB)
        # We assert that growth is at least close to the expected data size.
        expected_min_growth = iterations * data_size_mb * 1024 * 1024 * 0.8 # 80% of expected
        
        assert growth > expected_min_growth, "Memory did not grow as expected in leak mode"
        assert len(station.session_logs) == iterations, "Session logs should accumulate in leak mode"

    def test_monitor_status_alert(self, station, capsys):
        """
        Test that the monitor detects the leak when threshold is exceeded.
        Reference: MemoryLeak.py monitor_status
        """
        # Set a baseline memory
        station.previous_memory = 100 # Fake 100 MB
        
        # Mock the process memory info to simulate growth
        # We need to mock psutil.Process.memory_info or station.process.memory_info
        # Since station.process is an instance attribute, we can mock it.
        
        class MockMemoryInfo:
            def __init__(self, rss):
                self.rss = rss

        class MockProcess:
            def __init__(self, memory_mb):
                self.memory_mb = memory_mb
            
            def memory_info(self):
                return MockMemoryInfo(self.memory_mb * 1024 * 1024)

        # Case 1: No significant growth
        station.process = MockProcess(110) # 110 MB (10% increase)
        station.monitor_status()
        captured = capsys.readouterr()
        assert "BELLEK SIZINTISI TESPİT EDİLDİ" not in captured.out
        
        # Case 2: Significant growth (>20%)
        # previous_memory is updated to 110 in the previous call
        # We need > 110 * 1.20 = 132 MB
        
        station.process = MockProcess(140) # 140 MB
        station.monitor_status()
        captured = capsys.readouterr()
        assert "BELLEK SIZINTISI TESPİT EDİLDİ" in captured.out

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
