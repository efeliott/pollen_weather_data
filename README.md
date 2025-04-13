```markdown
# 🐍 Python Project - Météo Pollen Data Pipeline

This repository contains the Python scripts used for processing, cleaning, and storing pollen, weather, and pollution data for the **Météo Pollen** project.

## 📦 Features

- 📥 Fetch and parse JSON & CSV data from public sources  
- 🧹 Clean and normalize historical datasets  
- 🐘 Insert data into a PostgreSQL database  
- 📊 Prepare data for analytics and dashboard integration  
- 🔁 Reusable functions and modular structure  

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Set up the Python environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a `.env` file in the root directory with the following variables:

```env
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-username
DB_PASSWORD=your-password
SSL_MODE=require
```

## 🛠️ Project Structure

```
📂 your-repo-name/
├── 📁 data/               # Raw or processed data files
├── 📁 scripts/            # Python scripts for import, clean, insert
│   ├── import_pollen.py
│   ├── import_meteo.py
│   └── import_pollution.py
├── 📄 requirements.txt    # List of dependencies
├── 📄 .env.example        # Example env config
└── 📄 README.md
```

## 📌 Usage

Run the scripts manually or automate via a scheduler (e.g. cron):

```bash
python scripts/import_pollen.py
```

## 📥 Requirements

Install dependencies via:

```bash
pip install -r requirements.txt
```

Main libraries used:

- `pandas`
- `requests`
- `psycopg2-binary`
- `python-dotenv`
- `sqlalchemy`

## 🤝 Contributing

Feel free to open issues, fork the repository, or submit pull requests.

## 📄 License

This project is licensed under the MIT License.
```
