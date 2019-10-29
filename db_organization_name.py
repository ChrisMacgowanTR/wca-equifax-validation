#
# Acorn Ingest Validation
# WCA Equifax Validation
# Validate data in the Name Table
# Chris Macgowan
# 22 Oct 2019
# db_organization_name.py
#
# We will use this to validation
# We are testing this here
# have a nice day
#
# Here's how this is going to work
# we will pass

import datetime
import logging

import traceback
import psycopg2

class DbOrganizationName:

    display_log_on_pass = False

    # method: DbOrganizationName()
    # brief: This would be the famous constructor
    # param: name - the name of the house you want
    # param: age - the age of the house you want
    def __init__(self):
        logging.debug('Inside: DbOrganizationName::DbOrganizationName()')

    # We will use this to display the return of the test
    def display_loginfo(self, context, assert_message, file_equifax_id, db_partition, db_idvaluetarget):

        # The context can be pass, fail and what ever. We will use this
        # content to enable or disable the logging

        if context == 'pass':
            if self.display_log_on_pass:
                logging.info("------------------------------------------------------------")
                logging.info("Test Result")
                logging.info("Test: PASS")
                current_datetime = datetime.datetime.today()
                #logging.info("Test Class: DbOrganizationName")
                #logging.info("Test Method: validation()")
                #logging.info("Target Database: troa_dev_archive.organization_name")
                #logging.info("Report Datetime:  %s", current_datetime)
                logging.info("File Equifax id: %s", file_equifax_id)
                logging.info("Db Partition: %s", db_partition)
                logging.debug("Db id Value Target: %s", db_idvaluetarget)
                logging.info(assert_message)

        else:
            logging.info("------------------------------------------------------------")
            logging.info("Test Result")
            logging.info("Test: FAIL")
            current_datetime = datetime.datetime.today()
            #logging.info("Test Class: DbOrganizationName")
            #logging.info("Test Method: validation()")
            #logging.info("Target Database: troa_dev_archive.organization_name")
            #logging.info("Report Datetime:  %s", current_datetime)
            logging.info("File Equifax id: %s", file_equifax_id)
            logging.info("Db Partition: %s", db_partition)
            logging.debug("Db id Value Target: %s", db_idvaluetarget)
            logging.info(assert_message)

    # method: validation()
    # brief: Validate the data in the row with the database
    # param: row - The row we are going to validate
    # param: age - the age of the house you want
    def validation(self, row, results):

        # Set data from the file
        file_company_id = row['COMPANY_ID']
        file_canonical_name = row['CANONICAL_NAME']
        file_equifax_id = row['EQUIFAX_ID']

        db_partition = ''
        db_idvaluetarget = ''

        logging.debug('------------------------------------------------------------')
        logging.debug('Inside: DbOrganizationName::validation()')
        logging.debug("File data:")
        logging.debug("Data: file_company_id_array: %s", file_company_id)
        logging.debug("Data: file_canonical_name_array: %s", file_canonical_name)
        logging.debug("Data: file_equifax_id_array: %s", file_equifax_id)

        try:
            logging.debug("Attempting to connect to the database")
            conn = psycopg2.connect(dbname='a205718_troa_authority_entity_db_us_east_1_dev',
                                    user='acorn_readwrite_user_dev',
                                    password='y9Tz9D^PWvMM$o*4@!*J',
                                    host='localhost',
                                    port='1234',
                                    sslmode='require')
            logging.debug("Connection was successful")

            cursor = conn.cursor()
            logging.debug("Cursor was created successfully")

            partition = 'Equifax_Domestic'
            #name_type = 'Official'
            name_type = 'Doing Business As'
            #schema = 'troa_dev'
            schema = 'troa_dev_archive'

            postgreSQL_select_Query = f"SELECT {schema}.idmap.partition, {schema}.idmap.idtype, {schema}.idmap.idvaluetarget, {schema}.idmap.idvalue, {schema}.organization_name.troaid, {schema}.organization_name.name FROM {schema}.idmap INNER JOIN {schema}.organization_name ON {schema}.idmap.idvalue = {schema}.organization_name.troaid WHERE {schema}.idmap.idvaluetarget = '{file_equifax_id}' AND {schema}.idmap.partition = '{partition}' AND {schema}.organization_name.nametype = '{name_type}'"

            # postgreSQL_select_Query2 = f"SELECT * FROM troa_dev.organization_name where partitionid = '{file_partitionid_in}' AND partition = '{partition_In}'"
            logging.debug("SQL string: %s", postgreSQL_select_Query)

            logging.debug("Execute the cursor")
            cursor.execute(postgreSQL_select_Query)

            logging.debug("Selecting rows from mobile table using cursor.fetchall")
            mobile_records = cursor.fetchall()

            # We will test the row count. We can use this to skip the validation below
            # and report to the user that three is No data

            count = 0
            test_dataset = True

            for row in mobile_records:
                count += 1

            if count == 0:
                logging.debug("Cursor is empty")
                test_dataset = False

            if count != 1:
                logging.debug("Cursor returned more than one results")
                test_dataset = False

            logging.debug("Row count: %i", count)

            logging.debug("Print each row and it's columns values")
            for row in mobile_records:
                # Set the data to compare
                db_partition = row[0]
                db_idtype = row[1]
                db_idvaluetarget = row[2]
                db_idvalue = row[3]
                db_troaid = row[4]
                db_name_in = row[5]

                logging.debug("db_partition: %s", db_partition)
                logging.debug("db_idtype: %s", db_idtype)
                logging.debug("db_idvaluetarget: %s", db_idvaluetarget)
                logging.debug("db_idvalue: %s", db_idvalue)
                logging.debug("db_troaid: %s", db_troaid)
                logging.debug("db_name_in: %s", db_name_in)

            logging.debug('Close the database connection')
            conn.close()

        except Exception as err:
            logging.error("An exception occurred")
            # print Exception, err
            traceback.print_tb(err.__traceback__)
            results.add_to_exception()
            return
            # sys.exit(100)

        # Now we are going to do he data validation asserts
        # this will be fund !!!

        if test_dataset:

            # ------------
            try:
                assert int(file_equifax_id) == int(db_idvaluetarget)
                assert_message = f"Test Successful - file_equifax_id: {file_equifax_id} is equal to db_idvaluetarget: {db_idvaluetarget}"
                self.display_loginfo('pass', assert_message, file_equifax_id, db_partition, db_idvaluetarget)
                results.add_to_passed()
            except:
                assert_message = f"Test Failed - file_equifax_id: {file_equifax_id} Not Equal db_idvaluetarget: {db_idvaluetarget}"
                self.display_loginfo('fail', assert_message, file_equifax_id, db_partition, db_idvaluetarget)
                results.add_to_failed()

            # ------------
            try:
                assert file_canonical_name == db_name_in
                assert_message = f"Test Successful - file_canonical_name: {file_canonical_name} is equal to db_name_in: {db_name_in}"
                self.display_loginfo('pass', assert_message, file_equifax_id, db_partition, db_idvaluetarget)
                results.add_to_passed()
            except:
                assert_message = f"Test Failed - file_canonical_name: {file_canonical_name} Not Equal db_name_in: {db_name_in}"
                self.display_loginfo('fail', assert_message, file_equifax_id, db_partition, db_idvaluetarget)
                results.add_to_failed()

        else:
            assert_message = "Test Failed - No record were found matching the query"
            self.display_loginfo('fail', assert_message, file_equifax_id, db_partition, db_idvaluetarget)
            results.add_to_no_data()
