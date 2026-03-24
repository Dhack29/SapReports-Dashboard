# SapReports Dashboard

A real-time analytical dashboard built with Django, PostgreSQL, and Chart.js, designed to handle volumetric warranty claims data efficiently with rich 3D UI visuals and embedded JasperReport PDF generation.

## 🚀 Setup Instructions

If you have downloaded or cloned this repository, follow these exact steps to get the application running on your local machine:

### 1. System Prerequisites
You must install the following software on your machine:
* **Python 3.9+**: For the backend server.
* **PostgreSQL**: To host the application's database securely.
* **Java Development Kit (JDK) 17**: This is **strictly required** by the `pyreportjasper` library to compile the PDF reports correctly. 

### 2. Configure Your Environment
Before running the application, you must configure two environment parameters specific to your PC:
1. **Database Credentials:** Open `config/settings.py` and update the `DATABASES` block with your local PostgreSQL username, password, and port. The dashboard draws data from a table named `warranty_dipek`—ensure this exists.
2. **Java Home Path:** Open `reportsapp/views.py` and modify line 5 to explicitly point to where you installed Java on your system:
   ```python
   os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-17" # Ensure this path is correct!
   ```

### 3. Install Dependencies
Open your terminal in the downloaded project folder and prepare your isolated Python environment:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install required Python packages
pip install -r requirements.txt
```

### 4. Launch the Server
Start the Django development server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/dashboard/` in your web browser to view the interactive cross-filtering dashboard!
