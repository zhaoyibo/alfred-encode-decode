#!/usr/bin/env python3

import sys
from workflow import Workflow3
import traceback
import re

def add_item(wf, title, value):
  it = wf. add_item(title,
                   valid    = True,
                   subtitle = value,
                   arg      = value)

def main(wf):
  try:
    from urllib.parse import unquote, unquote_plus
    from html import unescape
    from base64 import b64decode, urlsafe_b64decode
    from binascii import unhexlify

    item_count = 0
    text = wf.args[0]
    # text = 'c2ZmK3M='
    text_bytes = text.encode('utf-8')

    decoded = unquote(text_bytes)
    if decoded != text:
      item_count += 1
      add_item(wf, u'URLDecode', decoded)

    decoded = unquote_plus(text)
    if decoded != text:
      item_count += 1
      add_item(wf, u'URLDecode(+)', decoded)


    decoded = unescape(text)
    if decoded != text:
      item_count += 1
      add_item(wf, u'HTMLDecode', decoded)


    try:
      decoded = b64decode(text).decode('utf-8')
      item_count += 1
      add_item(wf, u'Base64', decoded)
    except:
      pass

    try:
        decoded = urlsafe_b64decode(text).decode('utf-8')
        item_count += 1
        add_item(wf, u'Base64(URLSafe)', decoded)
    except:
      pass


    try:
      decoded = text.replace(' ', '')
      decoded = decoded.replace('\\x', '')
      decoded = bytearray.fromhex(decoded).decode('utf-8')
      item_count += 1
      add_item(wf, u'Hex', decoded)
    except:
      pass

    try:
      #decoded = text_bytes.decode('unicode-escape')
      decoded = re.sub(r'(\\u[\s\S]{4})',lambda x:x.group(1).encode("utf-8").decode("unicode-escape"), text)
      if decoded != text:
        add_item(wf, u'Unicode', decoded)
        item_count += 1
    except:
      pass


    if item_count == 0: wf.add_item(u'No decode available for "{}".'.format(text))
    wf.send_feedback()
  except Exception as e:
    traceback.print_exc()
    sys.exit( "Unable to decode : " + str(e) )

if __name__ == '__main__':
  wf = Workflow3()
  sys.exit(wf.run(main))
