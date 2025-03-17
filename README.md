# SAC Management System

A Flask-based web application for managing Sports Activity Center (SAC) equipment, bookings, and resources.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/sac-management-system.git
```

### Step 2: Set Up the Virtual Environment
Navigate to the project directory and create a virtual environment:
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

**For Windows:**
```bash
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
With the virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```

### Step 5: Configure the Database
Ensure your MySQL server is running and update your configuration settings (e.g., in a `.env` or `config.py` file) with your database credentials.

### Step 6: Create and Initialize the Database
Log in to your MySQL server and create a database named `SAC`:
```sql
CREATE DATABASE SAC;
USE SAC;
```
Execute the provided SQL scripts to set up the database schema and initial data:
```bash
mysql -u your_username -p SAC < sqls/tables.sql
mysql -u your_username -p SAC < sqls/users.sql
```

### Step 7: Start the Application
Launch the Flask development server:
```bash
flask run
```

