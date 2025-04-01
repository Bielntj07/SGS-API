import unittest
import os

if __name__ == "__main__":
    loader = unittest.TestLoader()
    
    test_dir = os.path.join(os.path.dirname(__file__), 'test')  
    
    suite = loader.discover(test_dir, pattern="test_*.py")  
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        exit(1)  
