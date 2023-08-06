#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The gwdatafind server is a Python application that runs as a Daemon under
Apache.  see the README file for details.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gwdatafind_server import create_app
application = create_app()
application.logger.info('app created.')
application.logger.info('urls: {0}'.format(application.url_map))
