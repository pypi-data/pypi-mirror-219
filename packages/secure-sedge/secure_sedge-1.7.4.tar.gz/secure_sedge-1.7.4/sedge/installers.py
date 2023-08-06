# pylint: disable=line-too-long
# flake8: noqa
import os
import posixpath
from io import BytesIO

from raft import task
from raft.collection import Collection


@task
def pan(ctx, host, bucket, namespace, cert,
        profile=None, region=None, passphrase=None):
    """
    uploads the specified cert and key files to a panos device.  the username
    and password used to access the api must be specified by the
    PALO_ALTO_USERNAME and PALO_ALTO_PASSWORD environment variables
    """
    import requests
    from boto3 import Session
    from xml.etree import ElementTree as ET
    from OpenSSL.crypto import dump_privatekey
    from OpenSSL.crypto import load_privatekey
    from OpenSSL.crypto import FILETYPE_PEM
    session = requests.Session()
    session.verify = False
    aws_session = Session(profile_name=profile, region_name=region)
    s3 = aws_session.client('s3')
    s3_key = posixpath.join(namespace, cert)
    username = os.environ['PALO_ALTO_USERNAME']
    password = os.environ['PALO_ALTO_PASSWORD']
    base_url = f'https://{host}/api/'

    print('generating api key')
    data = dict(user=username, password=password)
    data['type'] = 'keygen'
    doc = session.post(base_url, data=data)
    root = ET.fromstring(doc.text)
    api_key = root.find('result/key').text
    session.headers = {
        'X-PAN-KEY': api_key,
    }

    print(f'reading cert from s3://{bucket}/{s3_key}')
    response = s3.get_object(Bucket=bucket, Key=f'{s3_key}.crt')

    print(f'importing certificate as {cert}')
    params = {
        'type': 'import',
        'category': 'certificate',
    }
    data = {
        'type': 'import',
        'category': 'certificate',
        'certificate-name': cert,
        'format': 'pem',
        'key': api_key,
    }
    files = dict(file=response['Body'].read())
    response = session.post(base_url, params=params, data=data, files=files)
    print(f'{response.text}')

    print(f'reading key from s3://{bucket}/{s3_key}.key')
    response = s3.get_object(Bucket=bucket, Key=f'{s3_key}.key')
    print(f'importing key to {cert}')
    params['category'] = data['category'] = 'private-key'
    # all private keys uploaded to the palo alto require a passphrase.
    # when the cert has no passphrase, add a passphrase of `stupid_palo_alto`
    # because, well, that's stupid.
    stupid_palo_alto = 'stupid_palo_alto'
    data['passphrase'] = passphrase or stupid_palo_alto
    x509_key = response['Body'].read()
    if not passphrase:
        x509_key = load_privatekey(FILETYPE_PEM, x509_key)
        x509_key = dump_privatekey(
            FILETYPE_PEM,
            x509_key,
            passphrase=stupid_palo_alto.encode())
    files = dict(file=x509_key)
    response = session.post(base_url, params=params, data=data, files=files)
    print(f'{response.text}')

    print('committing')
    xml = '<commit><description>imported certificate from secure_sedge</description></commit>'
    data = {
        'type': 'commit',
        'cmd': xml,
        'key': api_key,
    }
    response = session.post(base_url, data=data)
    print(f'{response.text}')


@task
def linux(ctx, bucket, cert_key, private_key, services=None, profile=None):
    """
    installs certs to /etc/ssl/certs
    installs keys to /etc/ssl/private
    services is a comma separated list of services to reload once
    the keys have been updated
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    filename = os.path.join('/etc/ssl/certs', os.path.basename(cert_key))
    s3.download_file(bucket, cert_key, filename)
    filename = os.path.join('/etc/ssl/private', os.path.basename(private_key))
    s3.download_file(bucket, private_key, filename)
    if services:
        services = services.split(',')
        services = [ x.strip() for x in services ]
        for x in services:
            ctx.run(f'systemctl reload {x}')


@task
def redis(
        ctx, bucket, cert_key, private_key, redis_dir='/var/lib/redis',
        host=None, port=6379, profile=None):
    """
    installs certs and keys to redis_dir
    uses the redis-cli to update the certs
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    cert = os.path.join(redis_dir, 'redis.crt')
    s3.download_file(bucket, cert_key, cert)
    key = os.path.join(redis_dir, 'redis.key')
    s3.download_file(bucket, private_key, key)
    host = host or os.environ.get('HOST')
    with ctx.cd(redis_dir):
        for x in cert, key:
            ctx.run(f'chown redis:redis {x}')
        ctx.run(f'chmod 0640 {key}')
        ctx.run(f'chmod 0644 {cert}')
    ctx.run(
        f'redis-cli --tls -h {host} -p {port} config '
        f'set tls-cert-file "{os.path.basename(cert)}"')
    ctx.run(
        f'redis-cli --tls -h {host} -p {port} config '
        f'set tls-key-file "{os.path.basename(key)}"')


@task
def postgres(
        ctx, bucket, cert, key, dest_dir='/etc/postgresql/ssl',
        reload=True, command='pg_ctlcluster 15 main reload',
        config_file=None, profile=None):
    """
    installs certs and keys to dest_dir as postgres.crt and postgres.key
    by default, we will call the reload command specified after downloading
    to force postgres to reload the ssl certs
    if config_file is specified, the installer will update the
    `ssl_cert_file` and `ssl_key_file` parameters using sed
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    dest_cert = os.path.join(dest_dir, 'postgres.crt')
    s3.download_file(bucket, cert, dest_cert)
    dest_key = os.path.join(dest_dir, 'postgres.key')
    s3.download_file(bucket, key, dest_key)
    for x in dest_cert, dest_key:
        ctx.run(f'chown postgres:postgres {x}')
    ctx.run(f'chmod 0600 {dest_key}')
    ctx.run(f'chmod 0644 {dest_cert}')
    if config_file:
        ctx.run(f"sed -i -e 's,^ssl_cert_file.*,ssl_cert_file = '\"'\"'{dest_cert}'\"'\"',g' {config_file}")
        ctx.run(f"sed -i -e 's,^ssl_key_file.*,ssl_key_file = '\"'\"'{dest_key}'\"'\"',g' {config_file}")
    if reload:
        ctx.run(command)


@task
def xrdp(ctx, bucket, cert_key, private_key, profile=None):
    """
    installs certs to /etc/ssl/certs
    installs keys to /etc/ssl/private
    services is a comma separated list of services to reload once
    the keys have been updated
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    filename = '/etc/xrdp/cert.pem'
    s3.download_file(bucket, cert_key, filename)
    filename = '/etc/xrdp/key.pem'
    s3.download_file(bucket, private_key, filename)


@task
def iis(ctx, bucket, key, sites='', password=None, profile=None):
    """
    installs pfx to `cert:/localmachine/my`
    installs cert to one or more iis sites (separate with comma)
    if no sites are specified, will install the ssl certs to any unnamed sites
      e.g., *:443:

    example:

        sedge install.iis -b ssl.example.com -k wildcard.pfx `
            --sites www.example.com,site2.example.com
    """
    from .sewer import install_cert_on_windows
    # import clr
    # ref = 'c:/Windows/System32/inetsrv/Microsoft.Web.Administration.dll'
    # clr.AddReference(ref)
    thumbprint = install_cert_on_windows(ctx, bucket, key, profile, password)
    sites = sites.split(',')
    suffix = """
    ipmo webadministration
    $bindings = Get-WebBinding -Name $site -Protocol https
    foreach ($binding in $bindings) {
        $pieces = $binding.bindingInformation.split(':')
        $bsite = $pieces[-1]
        if ($bsite -ne $site) {
            Write-Host "skipping $($bsite), not a match"
            continue
        }
        if ($binding.certificateHash -eq $thumbprint) {
            Write-Host "skipping $($binding.bindingInformation), cert already installed"
            continue
        }
        Write-Host "updating certificate for $($binding.bindingInformation)"
        $binding.addSslCertificate($thumbprint, 'my')
    }
    """
    for site in sites:
        lines = [
            f"$site = '{site}'",
            f"$thumbprint = '{thumbprint}'",
            suffix,
        ]
        c = '\n'.join(lines)
        ctx.run(c)


def update_private_key_permissions(ctx, thumbprint):
    """
    updates the windows file access permissions on a certificate
    to make the certificate readible by the network user
    """
    c = rf"""
    $thumbprint = '{thumbprint}'
    $cert = Get-Item "cert:/localmachine/my/$($thumbprint)"
    $filename = $cert.privatekey.cspkeycontainerinfo.uniquekeycontainername
    $root = 'c:\programdata\microsoft\crypto\rsa\machinekeys'
    $p = [io.path]::combine($root, $filename)
    $root = 'c:\programdata\microsoft\crypto\keys'
    $private_key = [Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
    $q = $private_key.key.UniqueName
    $q = [io.path]::combine($root, $q)
    $rule = new-object security.accesscontrol.filesystemaccessrule 'NETWORK SERVICE', 'Read', allow
    if ([io.file]::exists($p)) {'{'}
        $acl = get-acl -path $p
        $acl.addaccessrule($rule)
        echo 'modifying acl'
        echo $p
        set-acl $p $acl
    {'}'}
    if ([io.file]::exists($q)) {'{'}
        $acl = get-acl -path $q
        $acl.addaccessrule($rule)
        echo 'modifying acl'
        echo $q
        set-acl $q $acl
    {'}'}
    """
    print(f'updating file permissions on {thumbprint}')
    ctx.run(c)


@task
def rds(ctx, bucket, key, password=None, profile=None):
    """
    installs pfx to `cert:/localmachine/my`
    installs cert for use with rds
    """
    from .sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(
        ctx, bucket, key, profile, password, 'my')
    update_private_key_permissions(ctx, thumbprint)
    c = (
        rf"""
        $klass = 'Win32_TSGeneralSetting'
        $ns = 'root\cimv2\terminalservices'
        $thumbprint = '{thumbprint}'
        $path = Get-WmiObject -class $klass -Namespace $ns -Filter "TerminalName=`'RDP-tcp`'"
        if ($path.sslcertificatesha1hash -ne $thumbprint) {'{'}
            Write-Host 'updating certificate'
            $hash = @{'{'}SSLCertificateSHA1Hash=$thumbprint{'}'}
            Set-WmiInstance -Path $path.__path -argument $hash
        {'}'}
        """
    )
    ctx.run(c)


@task
def winrm(ctx, bucket, key, password=None, profile=None):
    """
    installs pfx to `cert:/localmachine/my`
    installs cert for use with winrm

    if you encounter ssl error 234, check the sslbindings https://stackoverflow.com/questions/21859308/failed-to-enumerate-ssl-bindings-error-code-234
    if you encounter internal error with SSL library, that usually means you have to enable schannel for tls 1.2
      https://docs.rackspace.com/support/how-to/enabling-tls-1.2-on-windows-server/
    """
    from .sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(
        ctx, bucket, key, profile, password, 'my')
    update_private_key_permissions(ctx, thumbprint)
    c = (
        rf"""
        $thumbprint = '{thumbprint}'
        $cert = Get-Item "cert:/localmachine/my/$($thumbprint)"
        $valueset = @{'{'}
            Hostname = $cert.subject.split('=', 2)[1]
            CertificateThumbprint = $thumbprint
        {'}'}

        $selectorset = @{'{'}
            Transport = 'HTTPS'
            Address = '*'
        {'}'}
        Write-Host 'removing old winrm https certificate'
        Remove-WSManInstance -ResourceURI 'winrm/config/Listener' -SelectorSet $selectorset
        Write-Host 'configuring new winrm https certificate'
        New-WSManInstance -ResourceURI 'winrm/config/Listener' -SelectorSet $selectorset -ValueSet $valueset
        """
    )
    ctx.run(c)


@task
def exchange(ctx, bucket, key, connector=None, password=None, profile=None):
    from sedge.sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(
        ctx, bucket, key, profile, pfx_password=password)
    lines = [ f"""
    Add-PSSnapin -Name Microsoft.Exchange.Management.PowerShell.SnapIn
    ipmo webadministration
    Enable-ExchangeCertificate -Thumbprint '{thumbprint}' -services 'iis,smtp'
    """, ]
    if connector:
        lines. append(f"""
        $pfx = Get-Item 'cert:/localmachine/my/{thumbprint}'
        $name = "<I>$($pfx.issuer)<S>$($pfx.subject)"
        Write-Host $name
        Set-SendConnector -Identity '{connector}' -TLSCertificateName $name
        """)
    lines.append('Restart-Service -Name MSExchangeTransport')
    c = '\n'.join(lines)
    ctx.run(c)


@task
def update_trusted_rds_publishers(ctx, bucket, key, password=None, profile=None, gpo='cert_distribution', ou='computers' ):
    """
    installs pfx to `cert:/localmachine/my`
    cert thumbprint is then used to update the windows gpo cert_distribution this ensures that the cert
    is put into the trusted publisher store on all computers impacted by the gpo. it will also sign .rdp files.
    this task should be run on 1 domain controller per windows domain.

    if the gpo does not exist inside the domain please run the following command on a domain controller
    New-GPO -Name cert_distribution
    now link that gpo to the target organization unit
    New-GPLink -Name cert_distribution -Target "OU=some_server_ou,DC=example,DC=com,"
    is put into the trusted publisher store on all computers impacted by the gpo. it will also sign .rdp files.
    this task should be run on 1 domain controller per windows domain.

    the ou variable will default to run against the computers container if you wish to run against a specific ou,
    please do the following example syntax lets say we want to run against the domain controllers ou
    example: ou='Domain Controllers'
    """
    from .sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(
        ctx, bucket, key, profile, password, 'my')
    update_private_key_permissions(ctx, thumbprint)
    c = (
        rf"""
        $thumbprint = '{thumbprint}'
        $cert = Get-Item "cert:/localmachine/my/$($thumbprint)"
        $gponame = '{gpo}'
        $domain = get-addomain
        $ou = '{ou}'
        $key = \"HKLM\SOFTWARE\Policies\Microsoft\SystemCertificates\TrustedPublisher\Certificates\$($thumbprint)\"
        $certkey = \"HKLM:\SOFTWARE\Microsoft\SystemCertificates\MY\Certificates\$($thumbprint)\"
        $certblob = Get-ItemProperty -Path $certkey -Name 'blob' | Select -Expand 'blob'
        $blob = $cert.rawdata
        $trustedpub = Set-GPRegistryValue -Name $gponame -Key $key -ValueName 'Blob' -Type Binary -Value $certblob
        $key1 = \"HKCU\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\"
        $rdpsign = Set-GPRegistryValue -Name $gponame -Key $key1 -ValueName 'TrustedCertThumbprints' -Type 'String' -Value $thumbprint
        if ($ou -eq 'computers'){'{'}
            write-host 'performing gpo updates on computers ou' 
            Get-ADComputer -Filter * -SearchBase $domain.ComputersContainer | foreach {'{'}
                write-host \"performing gpo updates on $($_.name)\"
                Invoke-GPUpdate -Computer $_.name -Force -ErrorAction silentlycontinue
            {'}'}                         
        {'}'}
        else
        {'{'}
            write-host 'looking for ou named {ou}'
            $org = Get-ADOrganizationalUnit -LDAPFilter '(name={ou})'
            write-host $org
            Get-ADComputer -Filter * -SearchBase $org.DistinguishedName | foreach {'{'}
                write-host \"performing gpo updates on $($_.name)\"
                Invoke-GPUpdate -Computer $_.name -Force -ErrorAction silentlycontinue
            {'}'}
        {'}'}
        """
    )
    ctx.run(c)


def trusted_cert_entries(certs, seen):
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    from jks.jks import TrustedCertEntry
    entries = []
    for cert in certs:
        alias = cert.subject.rfc4514_string()
        i = 0
        original_alias = alias
        while alias in seen:
            i += 1
            alias = f'{original_alias}{i:02d}'
        der = cert.public_bytes(serialization.Encoding.DER)
        seen[alias] = cert
        entries.append(TrustedCertEntry.new(alias, der))
    return entries


@task
def trust_keystore(
        ctx, keystore_filename, bucket, cert_object,
        ca_bundle='/etc/ssl/certs/ca-bundle.crt', password=None,
        profile=None, region=None):
    """
    builds a trust keystore from the specified cert bundle and sedge cert

    password may be specified via the SEDGE_KEYSTORE_PASSWORD command
    """
    from cryptography import x509
    from jks.jks import KeyStore
    from boto3 import Session
    session = Session(profile_name=profile, region_name=region)
    password = password or os.environ.get('SEDGE_KEYSTORE_PASSWORD')
    seen = dict()
    entries = []
    with open(ca_bundle, 'rb') as f:
        data = f.read()
    certs = x509.load_pem_x509_certificates(data)
    print(f'found {len(certs)} certs in {ca_bundle}')
    entries = trusted_cert_entries(certs, seen)

    s3 = session.resource('s3')
    s3_cert = s3.Object(bucket, cert_object)
    response = s3_cert.get()
    data = response['Body'].read()
    certs = x509.load_pem_x509_certificates(data)
    entries += trusted_cert_entries(certs[1:], seen)
    k = KeyStore.new('jks', entries)
    k.save(keystore_filename, password)


@task
def keystore(ctx, keystore_filename, name, bucket, cert_object, key_object,
             password=None, private_key_password=None, profile=None, region=None):
    """
    builds a keystore from the specified bucket cert and key objects

    password may be specified via the SEDGE_KEYSTORE_PASSWORD environment variable,
      this is the password for the keystore
    private_key_password may be specified via the SEDGE_PRIVATE_KEY_PASSWORD
      environment variable; this is the password used to encrypt the private
      key in the keystore
    """
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from jks.jks import PrivateKeyEntry
    from jks.jks import KeyStore
    from boto3 import Session
    session = Session(profile_name=profile, region_name=region)
    password = password or os.environ.get('SEDGE_KEYSTORE_PASSWORD')
    private_key_password = private_key_password or os.environ.get(
        'SEDGE_PRIVATE_KEY_PASSWORD'
    )
    backend = default_backend()
    s3 = session.resource('s3')
    s3_cert = s3.Object(bucket, cert_object)
    s3_private_key = s3.Object(bucket, key_object)
    response = s3_cert.get()
    data = response['Body'].read()
    certs = x509.load_pem_x509_certificates(data)
    print(f'found {len(certs)} certs in s3://{bucket}/{cert_object}')
    seen = dict()
    cert_chain = []
    for cert in certs:
        alias = cert.subject.rfc4514_string()
        i = 0
        original_alias = alias
        while alias in seen:
            i += 1
            alias = f'{original_alias}{i:02d}'
        der = cert.public_bytes(serialization.Encoding.DER)
        seen[alias] = cert
        cert_chain.append(der)
    response = s3_private_key.get()
    data = response['Body'].read()
    private_key = serialization.load_pem_private_key(data, None, backend)
    key = private_key.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    entry = PrivateKeyEntry.new(name, cert_chain, key)
    entry.encrypt(private_key_password)
    if os.path.exists(keystore_filename):
        k = KeyStore.load(keystore_filename, password)
        k.entries[name] = entry
    else:
        k = KeyStore.new('jks', [ entry ])
    k.save(keystore_filename, password)


installers_collection = Collection(
    pan,
    linux,
    iis,
    exchange,
    rds,
    xrdp,
    winrm,
    redis,
    postgres,
    update_trusted_rds_publishers,
    trust_keystore,
    keystore,
)
