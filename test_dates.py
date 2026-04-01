import psycopg2
try:
    conn = psycopg2.connect("dbname='SapReport' user='postgres' password='dipek' host='localhost'")
    with conn.cursor() as cur:
        # Check wradate format first
        cur.execute("SELECT wradate FROM warranty_dipek WHERE wradate IS NOT NULL LIMIT 1;")
        res = cur.fetchone()
        print(f"wradate format example: {res[0] if res else 'None'}")
        
        cur.execute("""
        SELECT wradate, sup_date, acceptance_date, crn_date, date_resolution
        FROM warranty_dipek
        WHERE wradate IS NOT NULL AND wradate != '' AND sup_date IS NOT NULL 
          AND acceptance_date IS NOT NULL AND crn_date IS NOT NULL 
          AND date_resolution IS NOT NULL
        LIMIT 5;
        """)
        for row in cur.fetchall():
            print(row)
except Exception as e:
    print("Error:", e)
