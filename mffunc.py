"""This module contains 'mailfile' helper functions."""

import mailbox
from email.header import decode_header,make_header

def can_decode(data,encoding):
    try:
        text = data.decode(encoding=encoding)
    except:
        return False
    return True

def get_encoding(data):
    for encoding in ('ascii','latin-1','utf-8','cp1252','iso-8859-1'):
        if can_decode(data,encoding):
            return encoding

def mbox_reader(stream):
    """
    This func is an hack to fix encoding problem

    More info
        https://stackoverflow.com/questions/37890123/how-to-trap-an-exception-that-occurs-in-code-underlying-python-for-loop
    """
    data = stream.read()
    encoding=get_encoding(data)
    text = data.decode(encoding=encoding)
    return mailbox.mboxMessage(text)

def create_new_mailbox(path):
    mbox = mailbox.mbox(path)
    mbox.lock()
    return mbox

def get_mailboxes(path):
    mailboxes=mailbox.mbox(path,factory=mbox_reader)
    return mailboxes

def extract_subject(message):
    #head=decode_header(message['subject'])
    head=decode_header(message['subject'] or '') # the >>>or ''<<< part is an hack to prevent malfunction with Python 3.

    #subject, encoding = head[0] # doesn't work well (encoding problem)
    subject=make_header(head) # works well. More info => https://stackoverflow.com/questions/7331351/python-email-header-decoding-utf-8

    subject=str(subject)
    assert isinstance(subject,str)
    return subject

def print_body(message):
    if message.is_multipart():
        body = ''.join(part.get_payload(decode=True) for part in message.get_payload())
    else:
        body = message.get_payload(decode=True)

    # debug
    #print(type(body))
    #print(body)

    body=body.decode('iso-8859-1') #'utf-8','ascii','latin-1','cp1252','iso-8859-1'

    assert isinstance(body,str)
    print(body)

def print_attachements(message):
    if message.get_content_maintype() == 'multipart':
        for part in message.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            filename = part.get_filename()
            print('    ====> {}'.format(filename,))

def extract_attachements(message):
    """Not used."""
    if message.get_content_maintype() == 'multipart':
        for part in message.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            filename = part.get_filename()
            print(filename)
            fb = open(filename,'wb')
            fb.write(part.get_payload(decode=True))
            fb.close()

