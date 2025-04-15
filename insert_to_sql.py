"""
Insert cleaned energy data into a PostgreSQL database.

This script prompts the user for database credentials via a GUI
and inserts data into both dimension and fact tables. Cleaned CSV
files are expected to be located in `data/cleaned/`.

Usage:
- Run this script after `main.py` to populate the PostgreSQL database.
- Tables must already be created using `00_create_table.sql`.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import psycopg2
from pathlib import Path

def get_db_credentials_gui():
    """Prompt the user for PostgreSQL credentials using GUI dialogs."""
    root = tk.Tk()
    root.withdraw()

    creds = {
        'host': simpledialog.askstring("Database Login", "Host (e.g., localhost):", initialvalue="localhost"),
        'port': simpledialog.askstring("Database Login", "Port (e.g., 5432):", initialvalue="5432"),
        'user': simpledialog.askstring("Database Login", "Username (e.g., postgres):", initialvalue="postgres"),
        'password': simpledialog.askstring("Database Login", "Password:", show='*'),
        'dbname': simpledialog.askstring("Database Login", "Database name (e.g., de_energy):")
    }

    if not all(creds.values()):
        messagebox.showerror("Input Error", "All fields are required.")
        raise SystemExit

    return creds

def insert_all_data():
    """Connect to the database and insert dimension and fact data."""
    creds = get_db_credentials_gui()

    try:
        conn = psycopg2.connect(**creds)
        conn.autocommit = True
        cursor = conn.cursor()

        # Dimension tables
        cursor.execute("""
            INSERT INTO zone_dim (zone_name)
            VALUES 
                ('50Hertz'),
                ('Amprion'),
                ('TenneT'),
                ('TransnetBW');
        """)

        cursor.execute("""
            INSERT INTO month_dim (date)
            SELECT generate_series('2015-01-01'::DATE, '2025-03-01'::DATE, INTERVAL '1 month')::DATE;
        """)

        cursor.execute("""
            INSERT INTO day_dim (date)
            SELECT generate_series('2015-01-05'::DATE, '2025-03-31'::DATE, INTERVAL '1 day')::DATE;
        """)

        # Fact tables from cleaned CSVs
        base_path = Path("data/cleaned")
        file_map = {
            "production_type_actual": base_path / "cleaned_generation.csv",
            "total_load": base_path / "cleaned_consumption.csv",
            "congestion_costs": base_path / "cleaned_costs.csv",
            "day_ahead_price": base_path / "cleaned_day_ahead_price.csv",
            "price_stats": base_path / "cleaned_price_stats.csv"
        }

        for table, filepath in file_map.items():
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    cursor.copy_expert(
                        f"COPY {table} FROM STDIN WITH CSV HEADER DELIMITER ','",
                        f
                    )
            else:
                print(f"⚠️ File not found and skipped: {filepath}")

        messagebox.showinfo("Success", "Data successfully inserted into PostgreSQL.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    insert_all_data()