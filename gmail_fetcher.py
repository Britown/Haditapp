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
