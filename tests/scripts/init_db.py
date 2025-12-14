#!/usr/bin/env python3
"""
Initialize database for Enhanced Budget Pro
"""

import sqlite3
import os
from pathlib import Path

def init_sqlite_db():
    """Initialize SQLite database"""
    db_path = Path("data/budget.db")
    
    # Create data directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active',
        metadata TEXT  -- JSON blob for additional data
    )
    ''')
    
    # Create budgets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT NOT NULL,
        total_amount REAL DEFAULT 0.0,
        currency TEXT DEFAULT 'USD',
        version INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    ''')
    
    # Create budget_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        budget_id INTEGER,
        category TEXT NOT NULL,
        item_name TEXT NOT NULL,
        amount REAL DEFAULT 0.0,
        quantity INTEGER DEFAULT 1,
        unit TEXT DEFAULT 'each',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (budget_id) REFERENCES budgets (id)
    )
    ''')
    
    # Create scripts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scripts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        filename TEXT NOT NULL,
        format TEXT,
        scene_count INTEGER DEFAULT 0,
        character_count INTEGER DEFAULT 0,
        parsed_data TEXT,  -- JSON blob
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    ''')
    
    # Create characters table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        script_id INTEGER,
        name TEXT NOT NULL,
        scene_count INTEGER DEFAULT 0,
        dialogue_lines INTEGER DEFAULT 0,
        estimated_cost REAL DEFAULT 0.0,
        notes TEXT,
        FOREIGN KEY (script_id) REFERENCES scripts (id)
    )
    ''')
    
    # Create exports table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        export_type TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    ''')
    
    # Create indices
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_name ON projects (name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_budgets_project ON budgets (project_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_scripts_project ON scripts (project_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_exports_project ON exports (project_id)')
    
    # Create views
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS v_project_summary AS
    SELECT 
        p.id,
        p.name,
        p.status,
        COUNT(DISTINCT b.id) as budget_count,
        COUNT(DISTINCT s.id) as script_count,
        COALESCE(SUM(b.total_amount), 0) as total_budget_amount
    FROM projects p
    LEFT JOIN budgets b ON p.id = b.project_id
    LEFT JOIN scripts s ON p.id = s.project_id
    GROUP BY p.id, p.name, p.status
    ''')
    
    # Commit changes
    conn.commit()
    
    # Insert sample data if database is empty
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        print("Inserting sample data...")
        
        # Insert sample project
        cursor.execute('''
        INSERT INTO projects (name, description, status) 
        VALUES (?, ?, ?)
        ''', ('Demo Film Project', 'A sample film project for demonstration', 'active'))
        
        project_id = cursor.lastrowid
        
        # Insert sample budget
        cursor.execute('''
        INSERT INTO budgets (project_id, name, total_amount, currency) 
        VALUES (?, ?, ?, ?)
        ''', (project_id, 'Initial Budget', 500000.00, 'USD'))
        
        budget_id = cursor.lastrowid
        
        # Insert sample budget items
        sample_items = [
            (budget_id, 'Crew', 'Director', 50000.00, 1, 'flat', 'Feature film director'),
            (budget_id, 'Crew', 'Cinematographer', 40000.00, 1, 'flat', 'DP for 30 days'),
            (budget_id, 'Equipment', 'Camera Package', 25000.00, 30, 'days', 'ARRI Alexa Mini package'),
            (budget_id, 'Locations', 'Studio Rental', 75000.00, 15, 'days', 'Sound stage rental'),
            (budget_id, 'Post Production', 'Editing', 30000.00, 1, 'flat', 'Editor for 8 weeks'),
        ]
        
        cursor.executemany('''
        INSERT INTO budget_items (budget_id, category, item_name, amount, quantity, unit, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_items)
        
        conn.commit()
        print("Sample data inserted successfully.")
    
    # Close connection
    conn.close()
    
    print(f"Database initialized at: {db_path.absolute()}")
    print(f"Database size: {db_path.stat().st_size / 1024:.2f} KB")

if __name__ == "__main__":
    print("🎬 Enhanced Budget Pro - Database Initialization")
    print("=" * 50)
    
    init_sqlite_db()
    
    print("\n✅ Database setup complete!")
    print("\nYou can now run the application with:")
    print("  make run")
    print("  or")
    print("  streamlit run ui_app.py")