#!/usr/bin/python3

"""This script extracts informations from a mailbox file."""

import sys
import argparse
import mffunc

def run(path):
    mailboxes=mffunc.get_mailboxes(path)

    if args.dest:
        dest_mailbox=mffunc.create_new_mailbox(args.dest)

    for i,message in enumerate(mailboxes):

        # extract subject
        try:
            subject=mffunc.extract_subject(message)
        except UnicodeDecodeError as e:
            sys.stderr.write('ERR-001 - Encoding problem occured with message {}\n'.format(message['Message-ID']))
            continue

        # filter (fulltext pattern matching in 'subject' field)
        if args.filter is not None:
            if args.filter in subject.lower():
                pass
            else:
                continue

        # display
        if args.subject:
            print(subject)
        if args.attachement:
            mffunc.print_attachements(message)
        if args.body:
            mffunc.print_body(message)

        # copy
        if args.dest:
            try:
                dest_mailbox.add(message)
                dest_mailbox.flush()
            except:
                sys.stderr.write('ERR-002 - Encoding problem occured with message {}\n'.format(message['Message-ID']))


        if args.count:
            if i>=(int(args.count)-1): # enumerate starts at 0
                break

    if args.dest:
        dest_mailbox.unlock()
# init.

args=None # this is to be explicit that args is global and can be used anywhere in this file.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path',help='mailbox path')
    parser.add_argument('-a','--attachement',action='store_true')
    parser.add_argument('-b','--body',action='store_true',help='Display body')
    parser.add_argument('-c','--count',default=None,help='Process COUNT message (if not set, process all messages)')
    parser.add_argument('-d','--dest',help='Copy messages to DEST mailbox')
    parser.add_argument('-f','--filter',help='Process message containing FILTER substring in subject, discard other.')
    parser.add_argument('-s','--subject',action='store_true',help='Display subject')
    args = parser.parse_args()

    run(args.path)
