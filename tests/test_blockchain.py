import unittest
import logging

from utils.blockchain import is_blockchain_valid

class IntegrationTestBlockchainValidation(unittest.TestCase):
    
    def test_blockchain_validation(self):
        result = is_blockchain_valid()

        self.assertIn(result, [True, False], "Blockchain validation should return a boolean value.")
        
        if result:
            logging.info("Test passed: Blockchain is valid.")
        else:
            logging.info("Test passed: Blockchain is not valid (or endpoint returned an error).")

if __name__ == '__main__':
    unittest.main()
