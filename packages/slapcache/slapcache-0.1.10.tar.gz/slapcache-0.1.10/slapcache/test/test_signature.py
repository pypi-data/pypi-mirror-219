from slapcache.signature import Signature, Config, strategy
from slapos.libnetworkcache import NetworkcacheClient
import slapos.signature, tempfile, unittest, os, sys
def _fake_call(self, *args, **kw):
  self.last_call = (args, kw)

KEY_CONTENT = """[debian-default]
repository-list = 
	main = http://ftp.fr.debian.org/debian/ wheezy main
	main-src = http://ftp.fr.debian.org/debian/ wheezy main
	update = http://ftp.fr.debian.org/debian/ wheezy-updates main
	update-src = http://ftp.fr.debian.org/debian/ wheezy-updates main
	slapos = http://download.opensuse.org/repositories/home:/VIFIBnexedi:/branches:/home:/VIFIBnexedi/Debian_7.0/ ./
	re6stnet = http://git.erp5.org/dist/deb ./
key-list = 
	slapos = http://git.erp5.org/gitweb/slapos.package.git/blob_plain/HEAD:/debian-preseed/slapos.openbuildservice.key
	re6st = http://git.erp5.org/gitweb/slapos.package.git/blob_plain/HEAD:/debian-preseed/git.erp5.org.key
filter-package-list = 
	ntp
	openvpn
	slapos.node
	re6stnet
filter-promise-list = 
	core
signature-list = 
	debian+++jessie/sid+++
	debian+++7.4+++
	debian+++7.5+++
	debian+++7.3+++
	debian+++7+++

[opensuse-legacy]
repository-list = 
	suse = http://download.opensuse.org/distribution/12.1/repo/oss/
	slapos = http://download.opensuse.org/repositories/home:/VIFIBnexedi:/branches:/home:/VIFIBnexedi/openSUSE_12.1/
	re6st = http://git.erp5.org/dist/rpm
key-list = 
filter-promise-list = 
	core
filter-package-list = 
	ntp
	openvpn
	slapos.node
	re6stnet
signature-list = 
	opensuse+++12.1+++x86_64

[system]
reboot = 2011-10-10
upgrade = 2014-06-04

"""

SIGNATURE = """-----BEGIN CERTIFICATE-----
MIIB8DCCAVmgAwIBAgIJAPFf61p8y809MA0GCSqGSIb3DQEBBQUAMBAxDjAMBgNV
BAMMBUNPTVAtMCAXDTE0MDIxNzE2NDgxN1oYDzIxMTQwMTI0MTY0ODE3WjAQMQ4w
DAYDVQQDDAVDT01QLTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAsiqCyuv1
HO9FmtwnMbEa1/u8Dn7T0k7hVKYXVQYof+59Ltbb3cA3nLjFSJDr/wQT6N89MccS
PneRzkWqZKL06Kmj+N+XJfRyVaTz1qQtNzjdbYkO6RgQq+fvq2CO0+PSnL6NttLU
/a9nQMcVm7wZ8kmY+AG5LbVo8lmxDD16Wq0CAwEAAaNQME4wHQYDVR0OBBYEFEVi
YyWHF3W7/O4NaTjn4lElLpp7MB8GA1UdIwQYMBaAFEViYyWHF3W7/O4NaTjn4lEl
Lpp7MAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAgIPGoxhUa16AgjZx
Jr1kUrs8Fg3ig8eRFQlBSLYfANIUxcQ2ScFAkmsvwXY3Md7uaSvMJsEl2jcjdmdi
eSreNkx85j9GtMLY/2cv0kF4yAQNRtibtDkbg6fRNkmUopDosJNVf79l1GKX8JFL
zZBOFdOaLYY/6dLRwiTUKHU6su8=
-----END CERTIFICATE-----"""


BASE_UPDATE_CFG_DATA = """

[networkcache]
download-binary-cache-url = http://www.shacache.org/shacache
download-cache-url = http://www.shacache.org/shacache
download-binary-dir-url = http://www.shacache.org/shadir
download-dir-url = http://www.shacache.org/shadir
"""

def _fake_upload(self, *args, **kwargs):
    return True


class NetworkCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.original_networkcache_upload = NetworkcacheClient.upload
        NetworkcacheClient.upload = _fake_upload
        self.config_dict = Config()

    def tearDown(self):
        NetworkcacheClient.upload = self.original_networkcache_upload

    def _createConfigurationFile(self, key, with_upload=False, with_signature=None):
        self.tmp_dir = tempfile.mkdtemp()
        assert(not(with_upload and with_signature))
        configuration_file_path = os.path.join(self.tmp_dir, 'slapcache.conf')
        signature_certificate_file = os.path.join(self.tmp_dir, 'shacache.cert')
        signature_private_key_file = os.path.join(self.tmp_dir, 'shacache.key')
        slapos.signature.generateCertificate(signature_certificate_file, signature_private_key_file, 'COMP-123A')
        _fake_signature_path = os.path.join(self.tmp_dir, 'fake_file')
        open(_fake_signature_path, 'w').write('# XXX ...')
        # KEY used by slapcache
        content = """
[shacache]
key = %s

""" % key
        # basic URLS
        content += BASE_UPDATE_CFG_DATA

        if with_signature:
            content += """
signature-certificate-list = %(certificate)s
""" % {'certificate': '\n'.join('  ' + l if l.strip() else '\n' for l in with_signature.splitlines())}

        if with_upload:
            content += """
signature-private-key-file = %(signature_private_key_file)s
upload-cache-url = https://www.shacache.org/shacache
shacache-cert-file = %(tempfile)s
shacache-key-file = %(tempfile)s
upload-dir-url = https://www.shacache.org/shadir
shadir-cert-file = %(tempfile)s
shadir-key-file = %(tempfile)s
signature-certificate-list =
  %(certificate)s
""" % {
        'tempfile': _fake_signature_path,
        'signature_private_key_file': signature_private_key_file,
        'certificate': ''.join('  ' + l if l.strip() else '\n' for l in open(signature_certificate_file, 'r').readlines())
        }

        with open(configuration_file_path, 'w') as configuration_file:
            configuration_file.write(content)
        return configuration_file_path

    def test_basic_configuration(self):
        self.config_dict.slapos_configuration = self._createConfigurationFile("slapos-upgrade-testing-key-with-config-file-invalid")
        shacache = Signature(self.config_dict)
        self.assertEqual(shacache.key, 'slapos-upgrade-testing-key-with-config-file-invalid')

    def test_basic_configuration_with_upload(self):
        self.config_dict.slapos_configuration = self._createConfigurationFile("slapos-upgrade-testing-key-with-config-file-invalid", True)
        shacache = Signature(self.config_dict)
        self.assertEqual(shacache.key, 'slapos-upgrade-testing-key-with-config-file-invalid')

    def test_configuration_file_dont_exist(self):
        self.config_dict.slapos_configuration = '/abc/123'
        if sys.version_info.major < 3:
            self.assertRaises(IOError, Signature, self.config_dict)
        else:
            self.assertRaises(FileNotFoundError, Signature, self.config_dict)

    def test_download_not_existing(self):
        _, path = tempfile.mkstemp()
        self.config_dict.slapos_configuration = self._createConfigurationFile("slapos-upgrade-testing-key-with-config-file-invalid")
        shacache = Signature(self.config_dict)
        self.assertEqual(False, shacache._download(path=path))
        self.assertEqual('', open(path, 'r').read())

    def test_download_existing(self):
        _, path = tempfile.mkstemp()
        # WARNING, the real key has ' inside
        self.config_dict.slapos_configuration = self._createConfigurationFile("'slapos-upgrade-testing-key-with-config-file-valid'")
        shacache = Signature(self.config_dict)
        shacache._download(path=path)
        self.maxDiff = None
        self.assertEqual(KEY_CONTENT.splitlines(), open(path, 'r').read().splitlines())

    def test_download_existing_without_signature_cert(self):
        _, path = tempfile.mkstemp()
        # WARNING, the real key has ' inside
        self.config_dict.slapos_configuration = self._createConfigurationFile("'slapos-upgrade-testing-key-with-config-file-valid'", with_signature=SIGNATURE)
        shacache = Signature(self.config_dict)
        shacache._download(path=path)
        self.maxDiff = None
        self.assertEqual(KEY_CONTENT.splitlines(), open(path, 'r').read().splitlines())

    def test_upload_to_cache(self):
        info, path = tempfile.mkstemp()
        self.config_dict.slapos_configuration = self._createConfigurationFile("slapos-upgrade-testing-key-with-config-file-invalid", True)
        shacache = Signature(self.config_dict)
        shacache._upload(path=path)

    def test_signature_strategy(self):
        entry_list = [{'timestamp': 123824.0}, {'timestamp': 12345.0}, {'timestamp': 13345.0}, {'timestamp': 12344.0}, {'timestamp': 12045.0}]
        self.assertEqual(strategy(entry_list), {'timestamp': 123824.0})
