import imaplib
import email
from email.header import decode_header
import toml
import re
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(ttl=3600)
def fetch_bice_transfers_from_gmail(month_str=None):
    """
    Fetches Bank BICE transfer emails, parses amount, name, and message.
    Returns a dictionary mapping: monto_int -> list of { nombre, mensaje, fecha_op }
    """
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        user = secrets.get("gmail", {}).get("email")
        pwd = secrets.get("gmail", {}).get("app_password")
        if not user or not pwd:
            return {}
    except:
        return {}

    bice_data = {}
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, pwd)
        mail.select("inbox")
        # Search last 150 BICE emails to cover a few months
        status, messages = mail.search(None, '(FROM "reply@info.bice.cl" SUBJECT "transferencia")')
        
        if status == "OK":
            email_ids = messages[0].split()
            # We don't want to parse all 300+, just the last 150 to be fast
            recent_ids = email_ids[-150:]
            for e_id in recent_ids:
                res, msg_data = mail.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/html":
                                    try:
                                        body = part.get_payload(decode=True).decode(errors='ignore')
                                        break
                                    except:
                                        pass
                        else:
                            try:
                                body = msg.get_payload(decode=True).decode(errors='ignore')
                            except:
                                pass
                        
                        if not body: continue
                        
                        soup = BeautifulSoup(body, 'html.parser')
                        text = soup.get_text(separator=' ')
                        text = re.sub(r'\s+', ' ', text)
                        if month_str:
                            meses_map = {
                                "enero": ["ene", "jan"], "febrero": ["feb", "feb"], "marzo": ["mar", "mar"],
                                "abril": ["abr", "apr"], "mayo": ["may", "may"], "junio": ["jun", "jun"],
                                "julio": ["jul", "jul"], "agosto": ["ago", "aug"], "septiembre": ["sep", "sep"],
                                "octubre": ["oct", "oct"], "noviembre": ["nov", "nov"], "diciembre": ["dic", "dec"]
                            }
                            parts = month_str.lower().split()
                            if len(parts) == 2:
                                mes, ano = parts[0], parts[1]
                                if mes in meses_map:
                                    valid = False
                                    for short_m in meses_map[mes]:
                                        if f"{short_m} {ano}" in text.lower():
                                            valid = True
                                            break
                                    if not valid:
                                        continue

                        
                        monto_match = re.search(r'Monto \$([\d\.]+)', text)
                        if not monto_match:
                            monto_match = re.search(r'\$([\d\.]+)', text)
                            
                        if not monto_match: continue
                        monto_str = monto_match.group(1).replace('.', '')
                        try:
                            monto_int = int(monto_str)
                        except:
                            continue
                            
                        nombre_match = re.search(r'Nombre(.*?)(?:RUT|Banco|Tipo|Número)', text, flags=re.IGNORECASE)
                        nombre = nombre_match.group(1).strip() if nombre_match else ""
                        
                        mensaje_match = re.search(r'Mensaje(.*?)(?:$|Cuenta|Banco|Rut|Tipo|Operación)', text, flags=re.IGNORECASE)
                        mensaje = mensaje_match.group(1).strip() if mensaje_match else ""
                        if "Operación Número" in mensaje:
                            mensaje = mensaje.split("Operación Número")[0].strip()
                            
                        # Avoid saving empties if not useful
                        if not nombre and not mensaje:
                            continue
                            
                        if monto_int not in bice_data:
                            bice_data[monto_int] = []
                            
                        bice_data[monto_int].append({
                            "nombre": nombre,
                            "mensaje": mensaje
                        })
        mail.logout()
    except Exception as e:
        print(f"IMAP Error: {e}")
        pass
        
    return bice_data

import io
from datetime import datetime
import email.utils

def get_month_index(month_str):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    try:
        return meses.index(month_str.lower()) + 1
    except:
        return 1

def fetch_statement_pdfs_from_gmail(month_str, year_int):
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        user = secrets.get("gmail", {}).get("email")
        pwd = secrets.get("gmail", {}).get("app_password")
        if not user or not pwd:
            return []
    except:
        return []

    target_m = get_month_index(month_str)
    receive_m = target_m + 1
    receive_y = year_int
    if receive_m > 12:
        receive_m = 1
        receive_y += 1
        
    pdfs = []
    
    searches = [
        ('bancobice@eeccvirtual.cl', 'Estado de Cuenta Tarjeta de Credito BICE'),
        ('reply@info.bice.cl', 'Tu Cartola de Cuenta Corriente Banco BICE')
    ]
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, pwd)
        mail.select("inbox")
        
        for sender, subject in searches:
            status, messages = mail.search(None, f'(FROM "{sender}" SUBJECT "{subject}")')
            if status == "OK" and messages[0]:
                email_ids = messages[0].split()
                # Check up to the last 15 emails to find the correct month
                for e_id in reversed(email_ids[-15:]):
                    res, msg_data = mail.fetch(e_id, '(RFC822)')
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            
                            # Check date
                            date_tuple = email.utils.parsedate_tz(msg['Date'])
                            if date_tuple:
                                msg_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                                if msg_date.month == receive_m and msg_date.year == receive_y:
                                    # Extract PDF
                                    for part in msg.walk():
                                        if part.get_content_maintype() == 'multipart':
                                            continue
                                        if part.get('Content-Disposition') is None:
                                            continue
                                        filename = part.get_filename()
                                        if filename and filename.lower().endswith('.pdf'):
                                            payload = part.get_payload(decode=True)
                                            if payload:
                                                pdf_io = io.BytesIO(payload)
                                                pdf_io.name = filename
                                                pdfs.append(pdf_io)
                                                break # Found PDF
                                    break # Found matching email for this sender
        mail.logout()
    except Exception as e:
        print(f"Error fetching PDFs: {e}")
        
    return pdfs
