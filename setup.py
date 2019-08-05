#!/usr/bin/env python

from distutils.core import setup

setup(name='mavlinkinterface',
      version='1.0',
      description='A Python interface for mavlink, expanding on pymavlink',
      author='Devin Driggs',
      author_email='drig3819@vandals.uidaho.edu',
      url='uidaho.edu',
      packages=['mavlinkinterface',
                'mavlinkinterface/enum',
                'mavlinkinterface/commands',
                'mavlinkinterface/commands/active',
                'mavlinkinterface/commands/passive',
                'mavlinkinterface/commands/configuration'],
      )
