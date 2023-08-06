#!/usr/bin/env python
# coding: utf-8

import os

HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', '6006')
server_url = f'ws://{HOST}:{PORT}'