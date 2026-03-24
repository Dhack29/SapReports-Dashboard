import os
import json
from django.db import connection
# Ensure PyReportJasper finds the JVM natively installed on this machine
os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-17"

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
from pyreportjasper import PyReportJasper
from django.contrib import messages

def index(request):
    """
    Render the main dashboard interface.
    """
    return render(request, 'reportsapp/index.html')

def generate_report(request):
    """
    Generate Jasper PDF Report and return it to the user.
    """
    if request.method == 'POST':
        # Define paths
        reports_dir = os.path.join(settings.BASE_DIR, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        input_file = os.path.join(reports_dir, 'employee_report.jrxml')
        output_file = os.path.join(reports_dir, 'employee_report_output') # extension added by pyreportjasper
        
        # In a real scenario, this file should exist or be created previously
        if not os.path.exists(input_file):
            messages.error(request, f"Report template 'employee_report.jrxml' not found in {reports_dir}")
            return render(request, 'reportsapp/index.html')

        import jpype
        try:
            if jpype.isJVMStarted():
                jpype.attachThreadToJVM()
        except Exception:
            pass

        try:
            # We map the Django DATABASES settings to pyreportjasper connection config
            db_config = settings.DATABASES['default']
            
            # Setup jasper processor
            jasper = PyReportJasper()
            jasper.config(
                input_file=input_file,
                output_file=output_file,
                output_formats=['pdf'],
                db_connection={
                    'driver': 'postgres',
                    'username': db_config.get('USER', 'your_database_user'),
                    'password': db_config.get('PASSWORD', 'your_database_password'),
                    'host': db_config.get('HOST', 'localhost'),
                    'database': db_config.get('NAME', 'your_database_name'),
                    'schema': 'public',
                    'port': str(db_config.get('PORT', '5432')),
                    'jdbc_driver': 'org.postgresql.Driver',
                    'jdbc_dir': os.path.join(settings.BASE_DIR, 'venv', 'Lib', 'site-packages', 'pyreportjasper', 'libs', 'jdbc')
                }
            )
            
            # Process and compile the report
            jasper.process_report()
            
            # Return the generated PDF
            pdf_path = f"{output_file}.pdf"
            if os.path.exists(pdf_path):
                return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
            else:
                messages.error(request, "Failed to generate PDF. The output file was not found.")
                
        except Exception as e:
            messages.error(request, f"Error generating report: {str(e)}")
            
    return render(request, 'reportsapp/index.html')

def dashboard_view(request):
    """
    Render analytical dashboard fetching real-time SQL data.
    """
    with connection.cursor() as cursor:
        # Build dynamic WHERE clause based on request.GET
        filter_map = {
            'mu': 'pu_zone',
            'rs': 'mapped_rs_code',
            'pl': 'part_no',
            'zone': 'zone',
            'depot': '"Depot/Shed"',
            'year': 'wra_year',
        }
        
        where_clauses = []
        params = []
        for key, col in filter_map.items():
            val = request.GET.get(key)
            if val:
                where_clauses.append(f"{col} = %s")
                params.append(val)
                
        month_val = request.GET.get('month')
        if month_val and '-' in month_val:
            y, m_str = month_val.split('-')
            import calendar
            month_map = {v: k for k, v in enumerate(calendar.month_abbr) if k}
            m = month_map.get(m_str)
            if m:
                where_clauses.append("wra_year = %s AND wra_month = %s")
                params.extend([y, float(m)])
            
        where_stmt = ""
        where_and_stmt = ""
        if where_clauses:
            where_stmt = "WHERE " + " AND ".join(where_clauses)
            where_and_stmt = "AND " + " AND ".join(where_clauses)
        
        # 1. KPIs
        cursor.execute(f"SELECT AVG(total_wraval) / 10000000.0, COUNT(*), SUM(total_wraval) / 10000000.0 FROM warranty_dipek {where_stmt}", params)
        kpi_row = cursor.fetchone()
        avg_claim = float(kpi_row[0] or 0)
        total_claims = int(kpi_row[1] or 0)
        total_claim_amount = float(kpi_row[2] or 0)
        
        # Helper to fetch list of dicts with float casting for Decimals
        def dictfetchall(cursor):
            from decimal import Decimal
            columns = [col[0] for col in cursor.description]
            rows = []
            for row in cursor.fetchall():
                row_dict = {}
                for idx, col in enumerate(columns):
                    val = row[idx]
                    if isinstance(val, Decimal):
                        val = float(val)
                    row_dict[col] = val
                rows.append(row_dict)
            return rows
        
        # 2. MU wise Claim amount
        cursor.execute(f"SELECT pu_zone as label, SUM(total_wraval)/10000000.0 as value FROM warranty_dipek {where_stmt} GROUP BY pu_zone ORDER BY value DESC", params)
        mu_wise_claim = dictfetchall(cursor)
        
        # 3. MU wise Complaints Count
        cursor.execute(f"SELECT pu_zone as label, COUNT(*) as value FROM warranty_dipek {where_stmt} GROUP BY pu_zone ORDER BY value DESC", params)
        mu_wise_comp = dictfetchall(cursor)
        
        # 4. Rolling Stock wise Claim amount
        cursor.execute(f"SELECT mapped_rs_code as label, SUM(total_wraval)/10000000.0 as value FROM warranty_dipek {where_stmt} GROUP BY mapped_rs_code ORDER BY value DESC LIMIT 10", params)
        rs_wise_claim = dictfetchall(cursor)
        
        # 5. PL wise Claim amount
        cursor.execute(f"SELECT part_no as label, SUM(total_wraval)/10000000.0 as value FROM warranty_dipek {where_stmt} GROUP BY part_no ORDER BY value DESC LIMIT 10", params)
        pl_wise_claim = dictfetchall(cursor)
        
        # 6. Zone wise
        cursor.execute(f"SELECT zone as label, SUM(total_wraval)/10000000.0 as value FROM warranty_dipek {where_stmt} GROUP BY zone ORDER BY value DESC", params)
        zone_wise = dictfetchall(cursor)
        
        # 7. Depot wise
        cursor.execute(f"SELECT \"Depot/Shed\" as label, SUM(total_wraval)/10000000.0 as value FROM warranty_dipek {where_stmt} GROUP BY \"Depot/Shed\" ORDER BY value DESC LIMIT 15", params)
        depot_wise = dictfetchall(cursor)
        
        # 8. Year wise
        cursor.execute(f"SELECT wra_year as label, SUM(total_wraval)/10000000.0 as value FROM warranty_dipek WHERE wra_year IS NOT NULL {where_and_stmt} GROUP BY wra_year ORDER BY wra_year", params)
        year_wise = dictfetchall(cursor)
        
        # 9. Month wise
        import calendar
        cursor.execute(f"SELECT wra_year, wra_month, SUM(total_wraval)/10000000.0 as value FROM warranty_dipek WHERE wra_year IS NOT NULL AND wra_month IS NOT NULL {where_and_stmt} GROUP BY wra_year, wra_month ORDER BY wra_year, wra_month", params)
        month_rows = dictfetchall(cursor)
        month_wise = [{"label": f"{int(r['wra_year']) if r['wra_year'] else ''}-{calendar.month_abbr[int(r['wra_month'])] if r['wra_month'] else ''}", "value": r['value']} for r in month_rows]
        
    context = {
        'avg_claim': round(avg_claim, 2),
        'total_claims': total_claims,
        'total_claim_amount': round(total_claim_amount, 2),
        'mu_wise_claim_json': json.dumps(mu_wise_claim),
        'mu_wise_comp_json': json.dumps(mu_wise_comp),
        'rs_wise_claim_json': json.dumps(rs_wise_claim),
        'pl_wise_claim_json': json.dumps(pl_wise_claim),
        'zone_wise_json': json.dumps(zone_wise),
        'depot_wise_json': json.dumps(depot_wise),
        'year_wise_json': json.dumps(year_wise),
        'month_wise_json': json.dumps(month_wise),
        'active_filters': request.GET.dict(),
    }
    
    return render(request, 'reportsapp/dashboard.html', context)
