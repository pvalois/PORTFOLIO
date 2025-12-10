import pytest

import testinfra.utils.ansible_runner

@pytest.mark.parametrize('pkg', [
  'php-fpm'
])

def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed

@pytest.mark.parametrize('svc', [
  'mariadb',
  'nginx'
])

def test_svc(host, svc):
    service = host.service(svc)
    assert service.is_running
    assert service.is_enabled

@pytest.mark.parametrize('file', [
  ("/var/www/html/magento/.installed")
])

def test_files(host, file):
    file = host.file(file)
    assert file.exists

