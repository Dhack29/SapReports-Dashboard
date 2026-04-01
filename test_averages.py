import psycopg2

try:
    conn = psycopg2.connect("dbname='SapReport' user='postgres' password='dipek' host='localhost'")
    with conn.cursor() as cur:
        # Test 1: Original assumption
        cur.execute("""
        SELECT 
            AVG(sup_date - TO_DATE(wradate, 'DD-MM-YYYY')) as lodge,
            AVG(acceptance_date - sup_date) as accept,
            AVG(crn_date - acceptance_date) as wra,
            AVG(date_resolution - crn_date) as res,
            AVG(date_resolution - TO_DATE(wradate, 'DD-MM-YYYY')) as overall,
            COUNT(*)
        FROM warranty_dipek
        WHERE wradate IS NOT NULL AND wradate != '' AND sup_date IS NOT NULL 
          AND acceptance_date IS NOT NULL AND crn_date IS NOT NULL 
          AND date_resolution IS NOT NULL;
        """)
        row1 = cur.fetchone()
        
        cur.execute("""
        SELECT 
            AVG(TO_DATE(wradate, 'DD-MM-YYYY') - sup_date),
            AVG(acceptance_date - TO_DATE(wradate, 'DD-MM-YYYY')),
            AVG(crn_date - TO_DATE(wradate, 'DD-MM-YYYY')),
            AVG(crn_date - acceptance_date),
            AVG(date_resolution - crn_date),
            AVG(date_resolution - acceptance_date),
            AVG(acceptance_date - sup_date)
        FROM warranty_dipek
        WHERE wradate IS NOT NULL AND wradate != '' AND sup_date IS NOT NULL 
          AND acceptance_date IS NOT NULL AND crn_date IS NOT NULL 
          AND date_resolution IS NOT NULL;
        """)
        row2 = cur.fetchone()

        with open('tests_out.txt', 'w') as f:
            f.write(f"Test 1: Lodge={row1[0]}, Acc={row1[1]}, WRA={row1[2]}, Res={row1[3]}, Over={row1[4]}, Count={row1[5]}\n")
            f.write(f"Pairs: wra-sup={row2[0]}, acc-wra={row2[1]}, crn-wra={row2[2]}, crn-acc={row2[3]}, res-crn={row2[4]}, res-acc={row2[5]}, acc-sup={row2[6]}\n")

        # Check `date_rep_recti`
        cur.execute("""
        SELECT date_rep_recti FROM warranty_dipek WHERE date_rep_recti IS NOT NULL LIMIT 2;
        """)
        print("date_rep_recti sample:", cur.fetchall())

except Exception as e:
    print("Error:", e)
