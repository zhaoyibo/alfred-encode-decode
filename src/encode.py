#!/usr/bin/env python3

import sys
from workflow import Workflow3
import traceback

def add_item(wf, title, value):
  it = wf. add_item(title,
                   valid    = True,
                   subtitle = value,
                   arg      = value)

def main(wf):
  try:
    from urllib.parse import quote, quote_plus
    from html import escape
    from base64 import b64encode, urlsafe_b64encode
    
    text = wf.args[0]
    text_bytes = text.encode('utf-8')

    encoded = quote(text_bytes)
    add_item(wf, u'URLEncode', encoded)
    encoded = quote_plus(text_bytes)
    add_item(wf, u'URLEncode(+)', encoded)
    encoded = escape(text)
    add_item(wf, u'HTMLEncode', encoded)
    add_item(wf, u'Base64', b64encode(text_bytes).decode('utf-8'))
    add_item(wf, u'Base64(URLSafe)', urlsafe_b64encode(text_bytes).decode('utf-8'))
    encoded = text_bytes.hex()
    add_item(wf, u'Hex', encoded)
    add_item(wf, u'Escaped Hex', '\\x' + '\\x'.join(encoded[i:i+2] for i in range(0, len(encoded), 2)))
    encoded = text.encode('unicode_escape').decode('utf-8')
    add_item(wf, u'Unicode', encoded)
    wf.send_feedback()
  except Exception as e:
    traceback.print_exc()
    sys.exit( "Unable to encode : " + str(e) )

if __name__ == '__main__':
  wf = Workflow3()
  sys.exit(wf.run(main))
