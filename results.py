#
# Acorn Ingest Validation
# WCA Equifax Validation
# Chris Macgowan
# 22 Oct 2019
# results.py
#
# This class will be used to collect the test results
#
# Here's how this is going to work
# we will pass

import logging

class Results:

    test_total = 0
    test_passed = 0
    test_failed = 0
    test_no_data = 0
    test_no_data_input = 0
    test_disabled = 0
    test_unknown = 0
    test_exception = 0

    # method: Results()
    # brief: This would be the famous constructor
    def __init__(self):
        logging.info('Inside: Results::Results()')
        self.test_total = 0
        self.test_passed = 0
        self.test_failed = 0
        self.test_no_data = 0
        self.test_no_data_input = 0
        self.test_disabled = 0
        self.test_unknown = 0
        self.test_exception = 0

    # -----------------------------------------------------
    # Add methods

    # method: add_to_passed()
    # brief: Increment the passed count by one (1)
    def add_to_passed(self):
        self.test_passed += 1
        self.test_total += 1

    # method: add_to_failed()
    # brief: Increment the failed count by one (1)
    def add_to_failed(self):
        self.test_failed += 1
        self.test_total += 1

    # method: add_to_no_data()
    # brief: Increment the no data count by one (1)
    def add_to_no_data(self):
        self.test_no_data += 1
        self.test_total += 1

    # method: add_to_no_data_input()
    # brief: Increment the no data input count by one (1)
    def add_to_no_data_input(self):
        self.test_no_data_input += 1
        self.test_total_input += 1

    # method: add_to_disabled()
    # brief: Increment the disabled count by one (1)
    def add_to_disabled(self):
        self.test_disabled += 1
        self.test_total += 1

    # method: add_to_unknown()
    # brief: Increment the test_unknown count by one (1)
    def add_to_unknown(self):
        self.test_unknown += 1
        self.test_total += 1

    # method: add_to_exception()
    # brief: Increment the test_exception count by one (1)
    def add_to_exception(self):
        self.test_exception += 1
        self.test_total += 1

    # -----------------------------------------------------
    # Get methods

    # method: get_total()
    # brief: Get the total
    # return: test_total count
    def get_total(self):
        return self.test_total

    # method: get_passed()
    # brief: Get the total
    # return: test_passed count
    def get_passed(self):
        return self.test_passed

    # method: get_failed()
    # brief: Get the total
    # return: test_failed count
    def get_failed(self):
        return self.test_failed

    # method: get_no_data()
    # brief: Get the total
    # return: test_no_data count
    def get_no_data(self):
        return self.test_no_data

    # method: get_no_data_input()
    # brief: Get the total
    # return: test_no_data_input count
    def get_no_data_input(self):
        return self.test_no_data_input

    # method: get_disabled()
    # brief: Get the total
    # return: test_disabled count
    def get_disabled(self):
        return self.test_disabled

    # method: get_unknown()
    # brief: Get the total
    # return: test_unknown count
    def get_unknown(self):
        return self.test_unknown

    # method: get_exception()
    # brief: Get the total
    # return: test_exception count
    def get_exception(self):
        return self.test_exception

    # -----------------------------------------------------
    # Display message

    # method: get_exception()
    # brief: Get the total
    # return: test_exception count
    def display_totals(self):
        logging.info(' ')
        logging.info("********************************************************************************")
        logging.info("**** TEST RESULTS **************************************************************")
        logging.info("********************************************************************************")
        logging.info("Calling test class: results")
        logging.info("Results - test_passed: %d", self.get_passed())
        logging.info("Results - test_failed: %d", self.get_failed())
        logging.info("Results - test_no_data: %d", self.get_no_data())
        logging.info("Results - test_exception: %d", self.get_exception())
        logging.info("Results - test_total: %d", self.get_total())
        logging.info(' ')
