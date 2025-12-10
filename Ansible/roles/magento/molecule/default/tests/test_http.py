
import requests 

def test_redirection(host):
    cmd = host.run("curl -v http://localhost")
    assert "HTTP/1.1 200" in cmd.stderr

