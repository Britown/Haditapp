"""Read-only Gmail import. Reception dates narrow search, not statement identity."""
import io
import imaplib
import email
from email.header import decode_header,make_header
from datetime import date,timedelta
import calendar
import hashlib
import streamlit as st
from processor_v3 import MONTHS


def get_month_index(month_str):
    try:return MONTHS.index(month_str.lower())+1
    except ValueError:raise ValueError('Mes inválido') from None


def _credentials():
    try:
        settings=st.secrets['gmail']
        user=settings['email'];password=settings['app_password']
        if not user or not password:raise KeyError()
        return user,password
    except Exception:
        raise ValueError('Configura gmail.email y gmail.app_password en los secretos de la plataforma.') from None


def fetch_statement_pdfs_from_gmail(month_str,year_int,pdf_password=""):
    """Return all unique candidate PDFs for explicit period review in the UI."""
    m=get_month_index(month_str);start=date(year_int,m,1)-timedelta(days=40)
    end=date(year_int,m,calendar.monthrange(year_int,m)[1])+timedelta(days=65)
    user,password=_credentials();mail=None;files=[];seen=set()
    try:
        mail=imaplib.IMAP4_SSL('imap.gmail.com',timeout=20);mail.login(user,password)
        status,folders=mail.list()
        mailbox='INBOX'
        if status=='OK':
            import re
            for folder in folders:
                decoded=folder.decode(errors='replace')
                if '\\All' in decoded:
                    match=re.search(r'"([^"]+)"\s*$',decoded)
                    if match:mailbox='"'+match[1]+'"'
        mail.select(mailbox,readonly=True)
        for sender in ['bancobice@eeccvirtual.cl','reply@info.bice.cl']:
            query=f'(FROM "{sender}" SINCE {start.strftime("%d-%b-%Y")} BEFORE {end.strftime("%d-%b-%Y")})'
            status,data=mail.search(None,query)
            if status!='OK':raise RuntimeError('Búsqueda de correo rechazada')
            for eid in data[0].split():
                status,parts=mail.fetch(eid,'(BODY.PEEK[])')
                if status!='OK':raise RuntimeError('No se pudo leer un correo')
                for part in parts:
                    if not isinstance(part,tuple):continue
                    message=email.message_from_bytes(part[1])
                    for attachment in message.walk():
                        filename=attachment.get_filename()
                        if filename:filename=str(make_header(decode_header(filename)))
                        if attachment.get_content_type()!='application/pdf' and not (filename and filename.lower().endswith('.pdf')):continue
                        payload=attachment.get_payload(decode=True)
                        if not payload:continue
                        digest=hashlib.sha256(payload).hexdigest()
                        if digest in seen:continue
                        seen.add(digest);file=io.BytesIO(payload);file.name=filename or 'cartola.pdf'
                        file.received=message.get('Date','');files.append(file)
        from processor_v3 import extract_text_from_pdf, transaction_lines, date_from_line
        from collections import Counter
        selected=[]; unreadable=[]
        for file in files:
            try:
                text=extract_text_from_pdf(file,pdf_password)
                import re
                billing=re.search(r'PER[IÍ]ODO\s+FACTURADO\s+DESDE\s+(\d{2}/\d{2}/\d{4})',text,re.I)
                dates=[date_from_line(line,year_int) for line in transaction_lines(text)]
                counts=Counter(d[3:] for d in dates if d!='N/A' and len(d)==10)
                # Use transaction period rather than reception month. For billing cycles
                # ending early next month, August still has the majority of transactions.
                detected=billing[1][3:] if billing else (counts.most_common(1)[0][0] if counts else None)
                if detected==f'{m:02}/{year_int}':selected.append(file)
            except ValueError:
                unreadable.append(file.name)
        if unreadable:
            raise ValueError('Hay PDF candidatos que no se pudieron leer. Ingresa la contraseña correcta o súbelos manualmente; no se procesó una selección incompleta.')
        return selected
    except (ValueError,RuntimeError):raise
    except Exception:
        raise RuntimeError('No se pudo consultar Gmail. Revisa la conexión y la contraseña de aplicación.') from None
    finally:
        if mail:
            try:mail.logout()
            except Exception:pass


def fetch_bice_transfers_from_gmail(month_str=None):
    # Do not attach another person's transfer solely by a shared amount.
    return {}
