#
# Acorn Ingest Validation
# WCA Equifax Validation
# Chris Macgowan
# 22 Oct 2019
# app.py
#
# This is app help with ingest data validation. It will be used to read the
# input file that was used during the ingest process. We will parse the input
# and then we will compare the data to the data in the database.
#
# When testing against a sample of Equifax data we are are only selecting a sample size of 15-20 records.
# typically we will pull from the top, middle and end of the data set in a random and unified manner.
# The Equifax consists of some ~54 million rows - and we are pulling 20, so that is about a
# %0.00003704 sample size.
#

import logging
import sys
import traceback
import psycopg2

import results as module_results

import db_organization_name as module_db_organization_name

import pandas as pd

file_handler = logging.FileHandler(filename='blue_dog.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    handlers=handlers
)

logging.info('Acorn Ingest Validation - WCA Equifax Validation')
logging.info('The application is starting')
logging.debug("Starting postgresql-connect")
logging.debug("Set input source")

# Input file options

# Full original file
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc9 in position 37: invalid continuation byte
source_file = 'C://macgowan//projects//qa//ingest_test_20191009//data//wca//full//wca_equifaxid//WCA_EQUIFAX_split_13.csv'

# Test oo version
source_file = 'C://macgowan//projects//qa//ingest_test_20191009//data//wca//full//wca_equifaxid//WCA_EQUIFAX_split_13__test00.csv'


logging.debug("Source file: %s", source_file)
logging.debug("Read the input file using pandas")
pipe_data = pd.read_csv(source_file, sep=',')

# Here is the plan
# We will iterate the file able and we will then process a selected number
# of the rows for testing
# passing the row to the validation method

results = module_results.Results()

db_organization_name = module_db_organization_name.DbOrganizationName()

# The interval is used to select a row each interneal. Ie if the interablt is 1000
# we will wait until a though rowna na bee aj drawn t he table

internal_count = 0
internal_set = 1

logging.debug("internal_count: %i", internal_count)
logging.debug("internal_set: %i", internal_set)

for index, row in pipe_data.iterrows():
    if index > internal_count:
        internal_count += internal_set
        logging.debug("Process for internal: %i", internal_count)
        # print(index, row['EFXID'], row['EFX_ADDRESS'])
        db_organization_name.validation(row, results)

# prints Time_(s), Mass_Flow_(kg/s), ...
logging.debug("Print columns: %s", pipe_data.columns)

# print the EFXID column
# print("Print data: ", pipe_data['EFX_ADDRESS'])
# COMPANY_ID,CANONICAL_NAME,EQUIFAX_ID
# 30172671,INFINITE POTENTIAL ENTERPRISES,52291821

pipe_company_id_array = pipe_data['COMPANY_ID']
pipe_canonical_name_array = pipe_data['CANONICAL_NAME']
pipe_equifax_id_array = pipe_data['EQUIFAX_ID']

logging.debug("Data - pipe_company_id_array : %s", pipe_company_id_array[0])
logging.debug("Print - pipe_canonical_name_array: %s", pipe_canonical_name_array[0])
logging.debug("Print - pipe_equifax_id_array: %s", pipe_equifax_id_array[0])

try:
    logging.debug("Attempting to connect o the database")
    conn = psycopg2.connect(dbname='a205718_troa_authority_entity_db_us_east_1_dev',
                            user='acorn_readwrite_user_dev',
                            password='y9Tz9D^PWvMM$o*4@!*J',
                            host='localhost',
                            port='1234',
                            sslmode='require')
    logging.debug("Connection was successful")

    cursor = conn.cursor()
    postgreSQL_select_Query = "SELECT * FROM troa_dev.organization_name where partitionid = '52'"

    cursor.execute(postgreSQL_select_Query)
    logging.debug("Selecting rows from mobile table using cursor.fetchall")
    mobile_records = cursor.fetchall()

    logging.debug("Print each row and it's columns values")
    for row in mobile_records:
        logging.debug("partition = %s", row[0])
        logging.debug("partitionid = %s", row[1])
        logging.debug("addresstype  = %s", row[2])
        logging.debug("streetaddress1  = %s", row[3])

except Exception as err:
  logging.error("An exception occurred")
  # print Exception, err
  traceback.print_tb(err.__traceback__)

logging.info(' ')
logging.info("********************************************************************************")
logging.info("**** TEST RESULTS **************************************************************")
logging.info("********************************************************************************")
logging.info("Calling test class: results")
logging.info("Results - test_passed: %d", results.get_passed())
logging.info("Results - test_failed: %d", results.get_failed())
logging.info("Results - test_no_data: %d", results.get_no_data())
logging.info("Results - test_exception: %d", results.get_exception())
logging.info("Results - test_total: %d", results.get_total())
logging.info(' ')
logging.info(' ')

logging.info('The end if near!')
logging.info('blue-dog Ingest Validation Utility')
logging.info('The application is stopping')
logging.info('Have a nice day')
