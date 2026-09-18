import re

def format_clp(amount):
    """Format amount as Chilean Peso: 1.339.261"""
    try:
        val = int(float(amount))
        return f"{val:,}".replace(",", ".")
    except:
        return str(amount)

def standardize_date(date_str):
    """Normalize messy bank dates into DD/MM/YYYY or DD/MM"""
    if not date_str or str(date_str).strip() in ["N/A", ""]:
        return "N/A"
    
    date_str = str(date_str).strip()
    months = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    
    # Check numeric DD/MM or DD/MM/YY
    match = re.search(r'(\d{1,2})[\-/](\d{1,2})(?:[\-/](\d{2,4}))?', date_str)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = match.group(3)
        if 1 <= month <= 12:
            if year:
                if len(year) == 2: year = "20" + year
                return f"{day:02d}/{month:02d}/{year}"
            return f"{day:02d}/{month:02d}"
            
    # Check textual DD-May or DD-May-YYYY
    match = re.search(r'(\d{1,2})[\-/]([a-zA-Z]+)(?:[\-/](\d{2,4}))?', date_str)
    if match:
        day = int(match.group(1))
        m_str = match.group(2).lower()
        year = match.group(3)
        
        month_idx = 0
        for i, m in enumerate(months):
            if i > 0 and m in m_str:
                month_idx = i
                break
                
        if month_idx > 0:
            if year:
                if len(year) == 2: year = "20" + year
                return f"{day:02d}/{month_idx:02d}/{year}"
            return f"{day:02d}/{month_idx:02d}"

    return date_str
