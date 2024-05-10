import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, WriteToBigQuery
import logging
import os

# Define a function to process the CSV line
class DataTransformation(beam.DoFn):

    def process(self,element):
        # Parse the CSV line
        columns = element.split(',')

        # Unpack the fields (assuming the order is EmployeeID, Name, DateOfJoining)
        employee_id, name, date_of_joining = columns[0], columns[1], columns[2]
        from datetime import datetime
        date_obj = datetime.strptime(date_of_joining,'%d-%m-%Y')
        new_date_of_joining = date_obj.strftime('%Y-%m-%d')

        # Create a dictionary with processed data
        processed_data = {
            'EmployeeID': employee_id,
            'Name': name,
            'DateOfJoining': new_date_of_joining,
            # Add more columns if necessary
        }
        
        return processed_data

def run_pipeline(argv=None):
    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',dest='input', default='gs://sample-data-bkt1/sampledata.csv'  , help='GCS file path for input CSV file')
    parser.add_argument('--output',dest='output', default= 'smart-quasar-342413:test_data_1.emp2 ' , help='BigQuery table in the format dataset.table')
    
    # Parse the command-line arguments
    known_args, pipeline_args = parser.parse_known_args(argv)
    
    # Create PipelineOptions using the parsed arguments
    pipeline_options = PipelineOptions(pipeline_args)
    
    data_trans = DataTransformation()
    # Create the pipeline
    with beam.Pipeline(options=pipeline_options) as p:
        # Read data from the GCS CSV file
        lines = p | 'ReadFromGCS' >> ReadFromText(known_args.input)

        # Process each CSV line using the `process_csv_line` function
        final_data = lines | 'ProcessData' >> beam.Map(data_trans.process)
        

        # Write the processed data to BigQuery
        final_data | 'WriteToBigQuery' >>  WriteToBigQuery(
         
            table=known_args.output,
            schema='EmployeeID:STRING, Name:STRING, DateOfJoining:STRING',
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,

        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run_pipeline()
