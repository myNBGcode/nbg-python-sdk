#! /usr/bin/env python

import os

from livereload import Server, shell

PORT = int(os.getenv("PORT", "8000"))

build_docs = shell('./bin/build_docs.sh')
server = Server()

server.watch('docs/**/**.rst', build_docs)
server.watch('docs/*.py', build_docs)
server.watch('nbg/**/*.py', build_docs)

server.serve(port=PORT, root='docs/build/html')
