import os
import jpype
import time

os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-17"
import jpype.imports

def test_jdbc():
    print("Starting JVM...")
    jdbc_jar = os.path.abspath(os.path.join('venv', 'Lib', 'site-packages', 'pyreportjasper', 'libs', 'jdbc', '*'))
    jpype.startJVM(classpath=[jdbc_jar])
    
    java_sql = jpype.JPackage('java').sql
    print("Loading driver...")
    jpype.JPackage('java').lang.Class.forName("org.postgresql.Driver")
    
    connect_string = "jdbc:postgresql://127.0.0.1:5432/SapReport"
    
    # Let's set a login timeout so it doesn't hang forever!
    java_sql.DriverManager.setLoginTimeout(3)
    
    print(f"Connecting to {connect_string}...")
    try:
        conn = java_sql.DriverManager.getConnection(connect_string, "postgres", "dipek")
        print("Connected!")
        conn.close()
    except Exception as e:
        print("Failed:", e)

if __name__ == '__main__':
    test_jdbc()
