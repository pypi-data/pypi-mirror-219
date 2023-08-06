# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012-2014 Vifib SARL and Contributors.
# All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from six.moves import configparser
import os
import time
import traceback
import tempfile
import datetime
import shutil
import hashlib
import base64
from random import choice
from string import ascii_lowercase

from slapos.libnetworkcache import NetworkcacheClient


def strategy(entry_list):
  """Get the latest entry. """
  timestamp = 0
  best_entry = None
  for entry in entry_list:
    if entry['timestamp'] > timestamp:
      best_entry = entry
      timestamp = entry['timestamp']

  return best_entry

class Signature:

  def __init__(self, config, logger=None):
    self.config = config
    self.logger = logger
    self.shacache = NetworkcacheClient(open(self.config.slapos_configuration, 'r'))
    network_cache_info = configparser.RawConfigParser()
    network_cache_info.read(self.config.slapos_configuration)
    if network_cache_info.has_section('shacache'):
      self.key = network_cache_info.get('shacache', 'key')
    else:
      self.key = "slapos-upgrade-testing-key"

  def log(self, message, *args):
    if self.logger is not None:
      self.logger.debug(message, *args)
    elif args:
      print(message % args)
    else:
      print(message)

  def get_file_hash(self, path):
    with open(path, 'rb') as f:
      h = hashlib.sha256()
      h.update(f.read())
      base = base64.b64encode(h.digest())
    return base

  def save_file_hash(self, path, destination):
    base = self.get_file_hash(path)
    with open(destination, "wb") as f:
      f.write(base)

  def _download_once(self, path, wanted_metadata_dict={},
                 required_key_list=[], is_sha256file=False):

    if is_sha256file:
      key = self.key + "-sha256-content"
    else:
      key = self.key

    self.log('Downloading %s...', key)
    result = self.shacache.select(key, wanted_metadata_dict, required_key_list)
    entry = None
    result = list(result)
    if result:
      entry = strategy(result)
      if not entry: # XXX: this should be the choice of 'strategy' function
        self.log("Can't find best entry matching strategy, selecting "
            "random one between acceptable ones.")
        entry = result[0]
    if not entry:
      self.log('No entry matching key %s', key)
    else:
      # XXX check if nc filters signature_certificate_list!
      # Creates a file with content to desired path.
      f = open(path, 'w+b')
      fd_download = self.shacache.download(entry['sha512'])
      try:
        shutil.copyfileobj(fd_download, f)
        # XXX method should check MD5.
        return entry
      finally:
        f.close()
        fd_download.close()
    return False

  def _download(self, path):
    """
    Download a tar of the repository from cache, and untar it.
    """
    try:
      download_metadata_dict = self._download_once(path=path,
              required_key_list=['timestamp'])
    except:
      return False
    if download_metadata_dict:
      self.log('File downloaded in %s', path)
      current_sha256 = self.get_file_hash(path)
      with tempfile.NamedTemporaryFile() as f_256:
        sha256path = f_256.name
        try:
          sha256sum_present = self._download_once(path=sha256path, required_key_list=['timestamp'], is_sha256file=True)
          self.log('sha 256 downloaded in %s', sha256path)
        except:
          sha256sum_present = False

        if sha256sum_present:
          expected_sha256 = f_256.read()
          if current_sha256 == expected_sha256:
            return True
          else:
            raise ValueError("%s != %s" % (current_sha256, expected_sha256))

  def download(self):
    """
    Get status information and return its path
    """
    info, path = tempfile.mkstemp()
    if self._download(path):
      try:
        shutil.move(path, self.config.destination)
      except Exception as e:
        self.log(e)
        self.log('Fail to move %s to %s, maybe permission problem?', path, self.config.destination)
        os.remove(path)
    else:
      os.remove(path)
      raise ValueError("No result from shacache")

  def _upload(self, path):
    """
    Creates uploads repository to cache.
    """
    sha256path = path + ".sha256"
    self.save_file_hash(path, sha256path)

    metadata_dict = {
      # XXX: we set date from client side. It can be potentially dangerous
      # as it can be badly configured.
      'timestamp': time.time(),
      'token': ''.join([choice(ascii_lowercase) for _ in range(128)]),
      # backward compatibility
      'file': 'notused',
      'urlmd5': 'notused'
    }
    try:
      sha512sum = self.shacache.upload(open(path, 'rb'), self.key, **metadata_dict)
      if sha512sum:
        self.log(
          'Uploaded %s to cache (using %s key) with SHA512 %s.', path,
          self.key, sha512sum)
        sha512sum_path = self.shacache.upload(
            open(sha256path, 'rb'),
            self.key + "-sha256-content",
            **metadata_dict)
        if sha512sum_path:
          self.log(
            'Uploaded %s to cache (using %s key) with SHA512 %s.', sha256path,
            self.key, sha512sum_path)
        else:
          self.log('Fail to upload sha256file file to cache.')
      else:
        self.log('Fail to upload %s to cache.', path)
    except Exception:
      self.log('Unable to upload to cache:\n%s.', traceback.format_exc())
      return

  def upload(self):
    self._upload(self.config.file)

# Class containing all parameters needed for configuration
class Config:
  def __init__(self, option_dict=None):
    if option_dict is not None:
      # Set options parameters
      for option, value in option_dict.__dict__.items():
        setattr(self, option, value)

