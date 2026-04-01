import psycopg2

try:
    conn = psycopg2.connect("dbname='SapReport' user='postgres' password='dipek' host='localhost'")
    with conn.cursor() as cur:
        # Create a giant select of every pairwise difference
        # Dates: sup_date, acceptance_date, crn_date, date_resolution
        # Text Dates: wradate, date_rep_recti
        
        query = """
        SELECT 
            AVG(ABS(sup_date - TO_DATE(wradate, 'DD-MM-YYYY'))) as d1,
            AVG(ABS(acceptance_date - TO_DATE(wradate, 'DD-MM-YYYY'))) as d2,
            AVG(ABS(crn_date - TO_DATE(wradate, 'DD-MM-YYYY'))) as d3,
            AVG(ABS(date_resolution - TO_DATE(wradate, 'DD-MM-YYYY'))) as d4,
            AVG(ABS(TO_DATE(date_rep_recti, 'DD-MM-YYYY') - TO_DATE(wradate, 'DD-MM-YYYY'))) as d5,
            
            AVG(ABS(acceptance_date - sup_date)) as d6,
            AVG(ABS(crn_date - sup_date)) as d7,
            AVG(ABS(date_resolution - sup_date)) as d8,
            AVG(ABS(TO_DATE(date_rep_recti, 'DD-MM-YYYY') - sup_date)) as d9,
            
            AVG(ABS(crn_date - acceptance_date)) as d10,
            AVG(ABS(date_resolution - acceptance_date)) as d11,
            AVG(ABS(TO_DATE(date_rep_recti, 'DD-MM-YYYY') - acceptance_date)) as d12,
            
            AVG(ABS(date_resolution - crn_date)) as d13,
            AVG(ABS(TO_DATE(date_rep_recti, 'DD-MM-YYYY') - crn_date)) as d14,
            
            AVG(ABS(date_resolution - TO_DATE(date_rep_recti, 'DD-MM-YYYY'))) as d15
        FROM warranty_dipek
        WHERE wradate IS NOT NULL AND wradate != '' 
          AND date_rep_recti IS NOT NULL AND date_rep_recti != '';
        """
        cur.execute(query)
        res = cur.fetchone()
        
        with open('tests_out2.txt', 'w') as f:
            f.write(str(res))
            
except Exception as e:
    print("Error:", e)
