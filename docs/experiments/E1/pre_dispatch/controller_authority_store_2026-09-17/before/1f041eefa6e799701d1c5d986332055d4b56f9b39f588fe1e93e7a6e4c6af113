"""Explicit controller transport; no ambient proxies, CA choice or redirects."""
from pathlib import Path
import hashlib, json, ssl, urllib.request, urllib.error

ENDPOINT='https://api.openai.com/v1/responses'
CA='/etc/ssl/certs/ca-certificates.crt'

def configuration():
    return {'endpoint':ENDPOINT,'model':'gpt-5','store':False,
        'credential_environment_reference':'OPENAI_API_KEY','proxy':'NONE',
        'redirects':'DENY','timeout_seconds':60,'tls_minimum':'TLSv1.2',
        'ca_file':CA,'ca_sha256':hashlib.sha256(Path(CA).read_bytes()).hexdigest()}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise urllib.error.HTTPError(req.full_url,code,'redirect denied',headers,fp)

def validate(config,endpoint,model):
    expected=configuration()
    if config!=expected or endpoint!=config['endpoint'] or model!=config['model']:
        raise ValueError('model transport identity/configuration mismatch')

def opener(config):
    validate(config,config['endpoint'],config['model'])
    context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version=ssl.TLSVersion.TLSv1_2
    context.load_verify_locations(cafile=config['ca_file'])
    return urllib.request.build_opener(urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=context),NoRedirect())

def request(config,endpoint,payload,credential):
    validate(config,endpoint,payload.get('model'))
    if payload.get('store') is not False: raise ValueError('model storage denied')
    return urllib.request.Request(endpoint,data=json.dumps(payload).encode(),
        headers={'Authorization':'Bearer '+credential,'Content-Type':'application/json'})
