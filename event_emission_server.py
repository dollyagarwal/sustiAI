
import sqlite3
import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP

DB_PATH = "event_emissions.db"

# Initialize FastMCP
mcp = FastMCP("carbon_accounting_expert")

def get_db_connection():
    """Establishes a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query(sql: str, params=()) -> List[Dict[str, Any]]:
    """Helper to run queries and return clean dictionaries."""
    conn = get_db_connection()
    try:
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

# ---------------------------------------------------------------------
# CORE DISCOVERY TOOLS
# ---------------------------------------------------------------------

@mcp.tool()
def describe_database() -> str:
    """
    Returns the exact CREATE TABLE statements for the database.
    Use this to understand table relationships and column names.
    """
    conn = get_db_connection()
    rows = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    conn.close()
    return "\n".join([row[0] for row in rows if row[0] is not None])

@mcp.tool()
def search_entities(query_string: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search for Companies or Events by name to find their IDs.
    Useful when the user asks for 'Tech Expo' but you need the ID to fetch data.
    """
    wildcard = f"%{query_string}%"

    companies = query("SELECT id, name FROM company WHERE name LIKE ?", (wildcard,))
    events = query("""
        SELECT e.id, e.name, e.start_time, c.name as company_name 
        FROM event e 
        JOIN company c ON e.company_id = c.id 
        WHERE e.name LIKE ?
    """, (wildcard,))

    return {"companies": companies, "events": events}

@mcp.tool()
def get_branding_config(company_id: int) -> Dict[str, Any]:
    """
    Retrieves the UI/UX branding guidelines (colors, logo) for a specific company.
    Returns a parsed dictionary from the stored JSON.
    """
    res = query("SELECT branding_config FROM company WHERE id = ?", (company_id,))
    if not res or not res[0]['branding_config']:
        return {"error": "No branding config found"}

    try:
        return json.loads(res[0]['branding_config'])
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in branding_config column"}

# ---------------------------------------------------------------------
# REPORTING LEVEL 1: EVENT SPECIFIC
# ---------------------------------------------------------------------

@mcp.tool()
def get_event_kpis(event_id: int) -> Dict[str, Any]:
    """
    Fetches high-level Key Performance Indicators (KPIs) for a single event.
    Calculates Total Emissions, Intensity per Attendee, and Intensity per SqFt.
    """
    sql = """
    SELECT 
        e.name as event_name,
        c.name as company_name,
        e.total_attendees,
        v.size_in_square_feet,
        COALESCE(SUM(em.calculated_emission_in_kgC02e), 0) as total_emissions_kg,
        COALESCE(SUM(em.calculated_emission_in_kgC02e) / 1000.0, 0) as total_emissions_tonnes
    FROM event e
    JOIN company c ON e.company_id = c.id
    JOIN venue v ON e.venue_id = v.id
    LEFT JOIN emission em ON e.id = em.event_id
    WHERE e.id = ?
    GROUP BY e.id
    """
    data = query(sql, (event_id,))
    if not data:
        return {"error": "Event not found"}

    row = data[0]
    # Calculate Intensities safely
    attendees = row['total_attendees'] or 1 # avoid div by zero
    sq_ft = row['size_in_square_feet'] or 1

    row['intensity_per_attendee_kg'] = round(row['total_emissions_kg'] / attendees, 2)
    row['intensity_per_sqft_kg'] = round(row['total_emissions_kg'] / sq_ft, 4)

    return row

@mcp.tool()
def get_event_emissions_breakdown(event_id: int) -> List[Dict[str, Any]]:
    """
    Returns the detailed emission inventory for an event.
    Grouped by Scope and Category.
    Essential for generating Scope 3 charts.
    """
    sql = """
    SELECT 
        gs.name as scope_name,
        ec.category as category_name,
        SUM(em.calculated_emission_in_kgC02e) as total_kg
    FROM emission em
    JOIN ghg_scope gs ON em.scope = gs.id
    JOIN emission_category ec ON em.category_id = ec.id
    WHERE em.event_id = ?
    GROUP BY gs.name, ec.category
    ORDER BY total_kg DESC
    """
    return query(sql, (event_id,))

# ---------------------------------------------------------------------
# REPORTING LEVEL 2: COMPANY PORTFOLIO
# ---------------------------------------------------------------------

@mcp.tool()
def get_company_portfolio_summary(company_id: int) -> Dict[str, Any]:
    """
    Aggregates data across ALL events for a specific company.
    Returns total events count and total carbon footprint.
    """
    sql = """
    SELECT 
        c.name as company_name,
        COUNT(DISTINCT e.id) as total_events_held,
        SUM(e.total_attendees) as total_attendees_impacted,
        COALESCE(SUM(em.calculated_emission_in_kgC02e), 0) as total_portfolio_emissions_kg
    FROM company c
    LEFT JOIN event e ON c.id = e.company_id
    LEFT JOIN emission em ON e.id = em.event_id
    WHERE c.id = ?
    GROUP BY c.id
    """
    data = query(sql, (company_id,))
    return data[0] if data else {"error": "Company not found"}

@mcp.tool()
def get_company_monthly_emissions(company_id: int, year: str) -> List[Dict[str, Any]]:
    """
    Time-series data: Returns total emissions grouped by month for a specific company and year.
    Useful for Line Charts showing trends.
    """
    sql = """
    SELECT 
        strftime('%Y-%m', e.start_time) as month,
        COUNT(DISTINCT e.id) as events_count,
        SUM(em.calculated_emission_in_kgC02e) as total_kg
    FROM event e
    JOIN emission em ON e.id = em.event_id
    WHERE e.company_id = ? AND strftime('%Y', e.start_time) = ?
    GROUP BY month
    ORDER BY month ASC
    """
    return query(sql, (company_id, year))

# ---------------------------------------------------------------------
# UTILITY: SQL EXPLORATION
# ---------------------------------------------------------------------

@mcp.tool()
def run_sql(query_text: str) -> List[Dict[str, Any]]:
    """
    Executes a custom READ-ONLY SQL query.
    Use this only if the specific reporting tools do not provide the data you need.
    IMPORTANT: Only 'SELECT' statements are allowed.
    """
    cleaned = query_text.strip().upper()
    if not cleaned.startswith("SELECT") and not cleaned.startswith("WITH"):
        return [{"error": "Security Restriction: Only SELECT queries allowed."}]

    return query(query_text)

if __name__ == "__main__":
    mcp.run(transport="stdio")
