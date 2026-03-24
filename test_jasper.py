import os
os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-17"

from pyreportjasper import PyReportJasper
import sys

def run_report():
    print("Initializing PyReportJasper...")
    jasper = PyReportJasper()
    
    input_file = os.path.abspath(os.path.join('reports', 'employee_report.jrxml'))
    output_file = os.path.abspath(os.path.join('reports', 'employee_report_output'))
    jdbc_dir = os.path.abspath(os.path.join('venv', 'Lib', 'site-packages', 'pyreportjasper', 'libs', 'jdbc'))
    
    print(f"Input: {input_file}")
    
    jasper.config(
        input_file=input_file,
        output_file=output_file,
        output_formats=['pdf'],
        db_connection={
            'driver': 'postgres',
            'username': 'postgres',
            'password': 'dipek',
            'host': 'localhost',
            'database': 'SapReport',
            'schema': 'public',
            'port': '5432',
            'jdbc_driver': 'org.postgresql.Driver',
            'jdbc_dir': jdbc_dir
        }
    )
    
    print("Processing report...")
    try:
        jasper.process_report()
        print("Success! PDF generated at:", f"{output_file}.pdf")
    except Exception as e:
        print("Error:", str(e))

if __name__ == '__main__':
    run_report()
