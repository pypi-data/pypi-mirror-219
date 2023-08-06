import json
import os

import click as click
from click import prompt
from pathlib import Path

from netsuite.Netsuite import Netsuite
from netsuite.settings import api_settings, IN_MEMORY_STORAGE, JSON_STORAGE, BASE_DIR, BASE_CONFIG_DIR
from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate, X509, X509Name, PKey, TYPE_RSA, X509Req, dump_privatekey, X509Extension)

def link(uri, label=None):
    if label is None:
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

@click.group()
def cli():
    """
    Simple CLI for managing Netsuite API Access
    """
    pass

@cli.command()
def initialize():

    generate_netsuite_client_config()
    # netsuite_app_name = prompt("What is the netsuite application name? (Portion before app.netsuite.com)", hide_input=False)
    #
    # app_name = prompt("App Name", default=api_settings.APP_NAME)
    # allow_none = prompt("Allow None", default=api_settings.ALLOW_NONE)
    # use_datetime = prompt("Use Datetime", default=api_settings.USE_DATETIME)
    # storage_class = prompt("Storage Class", default=api_settings.defaults.get('STORAGE_CLASS'),
    #                        type=click.Choice(api_settings.defaults.get('DEFAULT_STORAGE_CLASSES')),
    #                        show_choices=True)
    #
    # creds = {
    #     'CLIENT_ID': client_id,
    #     'CERT_ID': cert_id,
    #     # 'CLIENT_SECRET': client_secret,
    #     # 'REDIRECT_URL': redirect_url,
    #     'NETSUITE_APP_NAME': netsuite_app_name,
    #     'APP_NAME': app_name,
    #     'ALLOW_NONE': allow_none,
    #     'USE_DATETIME': use_datetime,
    #     'STORAGE_CLASS': storage_class,
    # }
    #
    # if storage_class == JSON_STORAGE:
    #     creds['JSON_STORAGE_PATH'] = prompt("Token Storage File", default=api_settings.JSON_STORAGE_PATH,
    #                                         type=click.Path(readable=True, writable=True))
    #
    # with open(api_settings.CREDENTIALS_PATH, 'w') as f:
    #     creds_json = json.dumps(creds, indent=4)
    #     f.write(creds_json)
    #     print(f"Netsuite Credentials written to: {api_settings.CREDENTIALS_PATH}")

    print("\n Generating Access Token....\n")
    netsuite = Netsuite()
    netsuite.request_access_token()

    if netsuite.token.access_token is None:
        print("Unable to get the access token")
        return

    generate_netsuite_rest_client()







@cli.command()
def generate_certificate():
    generate_netsuite_certificate()

def generate_netsuite_certificate():

    print(f"BASE DIR: {BASE_DIR}")

    CN = prompt("Domain", hide_input=False)
    ORG = prompt("Organization", hide_input=False)
    ORG_UNIT = prompt("Department", hide_input=False)
    L = prompt("City", hide_input=False)
    ST = prompt("State", hide_input=False)
    C = prompt("Country", hide_input=False)
    EMAIL = prompt("Email", hide_input=False)


    key = PKey()
    key.generate_key(TYPE_RSA, 4096)

    cert = X509()

    subject = cert.get_subject()
    subject.CN = CN
    subject.O = ORG
    subject.OU = ORG_UNIT
    subject.L = L
    subject.ST = ST
    subject.C = C
    subject.emailAddress = EMAIL

    cert.set_version(2)
    cert.set_issuer(subject)
    cert.set_subject(subject)
    cert.set_serial_number(int.from_bytes(os.urandom(16), byteorder="big"))
    # cert.set_serial_number(int(rand.bytes(16).encode('hex'), 16))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')


    with open(api_settings.NETSUITE_KEY_FILE, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))
        print(f"Netsuite Key File Created: {api_settings.NETSUITE_KEY_FILE} \n")

    with open(api_settings.NETSUITE_CERTIFICATE_FILE, 'wb+') as f:
        f.write(dump_certificate(FILETYPE_PEM, cert))
        print(f"Netsuite Certificate Created: {api_settings.NETSUITE_CERTIFICATE_FILE} \n")
        print(f"Steps to upload the certificate")
        print(f"  1. Login to Netsuite")
        print(f"  2. On top ribbon, go to Setup -> Integration -> Manage OAuth 2.0 Client Credentials Setup")
        print(f"  3. Click New")
        print(f"  4. Associate with your user, the integration record, and upload the netsuite_certificate.pem file from the path above.")
        print(f"  5. Copy the Certificate ID for when you generate the client config")

@cli.command()
def generate_client_config():
    generate_netsuite_client_config()

def generate_netsuite_client_config():
    try:
        netsuite = Netsuite()
        if netsuite.api_settings.CLIENT_ID is not None:
            from pprint import pprint
            print("Netsuite Credentials Found.")
            print("     CURRENT CONFIG")
            print("-------------------------")
            pprint(netsuite.api_settings.__dict__.get('_user_settings'), indent=4)
            print("\n")
            if prompt("Keep settings?", type=click.BOOL, default=True):
                return
    except Exception:
        print("")
    print("****************************")
    print("  GENERATE NETSUITE CONFIG")
    print("****************************")
    steps_completed = False
    while not steps_completed:
        steps_completed = prompt(f"Have you created the integration record by following the steps in the README?", default='y', type=click.BOOL, show_choices=True)
        if steps_completed:
            client_id = prompt("Client Id", hide_input=False)
        else:
            print('Read it and do the steps hoe https://bitbucket.org/theapiguys/netsuite_python/src/master/')

    print("\n --- Certificate Configuration --- \n ")
    certificate_uploaded = False
    while not certificate_uploaded:
        certificate_uploaded = prompt(f"Have you generated a certificate and uploaded it to Netsuite?", default='n', type=click.BOOL, show_choices=True)
        if certificate_uploaded:
            cert_id = prompt("Certificate ID: ", hide_input=False)
        else:
            generate_netsuite_certificate()

    print("\n --- Certificate has been Configured --- \n ")
    # client_secret = prompt("What is your client secret?", hide_input=True)
    # redirect_url = prompt("Redirect URL", default=api_settings.REDIRECT_URL)
    netsuite_app_name = prompt("What is the netsuite application name (Portion before app.netsuite.com)?", hide_input=False)
    app_name = prompt("App Name (for token storage)", default=api_settings.APP_NAME)
    # storage_class = prompt("Storage Class", default=api_settings.defaults.get('STORAGE_CLASS'),
    #                        type=click.Choice(api_settings.defaults.get('DEFAULT_STORAGE_CLASSES')),
    #                        show_choices=True)
    storage_class = api_settings.defaults.get('STORAGE_CLASS')

    creds = {
        'CLIENT_ID': client_id,
        'CERT_ID': cert_id,
        # 'CLIENT_SECRET': client_secret,
        # 'REDIRECT_URL': redirect_url,
        'NETSUITE_APP_NAME': netsuite_app_name,
        'APP_NAME': app_name,
        'ALLOW_NONE': api_settings.ALLOW_NONE,
        'USE_DATETIME': api_settings.USE_DATETIME,
        'STORAGE_CLASS': storage_class,
    }

    if storage_class == JSON_STORAGE:
        creds['JSON_STORAGE_PATH'] = prompt("Token Storage File", default=api_settings.JSON_STORAGE_PATH,
                                            type=click.Path(readable=True, writable=True))


    with open(api_settings.CREDENTIALS_PATH, 'w') as f:
        creds_json = json.dumps(creds, indent=4)
        f.write(creds_json)
        print(f"Netsuite Credentials path: {api_settings.CREDENTIALS_PATH} ")
    print("\n ----- Configuration Generated -----")



    return creds

@cli.command()
def generate_rest_client():
    generate_netsuite_rest_client()

def generate_netsuite_rest_client():
    ns_records_to_include = []
    print (" ----- Rest Client Generator -----")
    netsuite = Netsuite()
    use_record_wizard = prompt("Use Record Wizard?", type=click.BOOL, default=True)
    if use_record_wizard:
        needs_other_recordtypes = prompt("Will you be using record types other than customer?", type=click.BOOL, default=True)


        if needs_other_recordtypes:

            display_ns_classes = prompt("List available Netsuite Records?", type=click.BOOL, default=True)
            print("")
            print(" Getting Record Types... May take a minute...")
            records = netsuite.get_netsuite_recordtypes()
            if display_ns_classes:
                display_custom = prompt("Display Custom records (probably not)?", type=click.BOOL, default=False)
                print("\n   RECORDS")
                print("-------------------")
                if display_custom:
                    for record in records:
                        print(record)
                else:
                    for record in records:
                        if "customrecord" not in record and "customlist" not in record:
                            print(record)

            print("\n")
            add_more_records = True
            while add_more_records:
                next_record = prompt("Which records do you need?", default='')
                if next_record == '':
                    if prompt("Skip this step and use default (customer)?", type=click.BOOL, default=False):
                        break
                else:
                    if next_record not in records:
                        print("That record is not available.")
                    elif next_record in ns_records_to_include:
                        print("record already included.")
                    else:
                         ns_records_to_include.append(next_record)
                         print(f"Record Added: {next_record}")
                add_more_records = prompt("Add another?", type=click.BOOL, default='yes', show_choices=True)


        if len(ns_records_to_include) >> 0:
            record_str = ''
            index = 0
            for record in ns_records_to_include:
                print(len(ns_records_to_include))
                if index == 0:
                    print('index was 0')
                    record_str += f'{record}'
                    index += 1
                else:
                    record_str += f',{record}'
        else:
            record_str = 'customer'
    else:
        record_str = prompt("Enter Record Types (comma separated)", default='customer')
    print(f"Record STR: record_str")
    netsuite.generate_rest_client(record_types=record_str)


@cli.command()
@click.option('--credentials-file', '--f', type=click.File('r'), default=api_settings.CREDENTIALS_PATH,
              prompt="Path to Credentials File")
@click.pass_context
def get_access_token(ctx, credentials_file):
    """OAuth flow for Netsuite to obtain an access and refresh token"""
    try:
        creds = json.load(credentials_file)
    except Exception as e:
        return

    creds['APP_NAME'] = prompt("What app is being used?", type=click.STRING, default=creds['APP_NAME'])

    netsuite = Netsuite(
        config=creds
    )
    netsuite.request_access_token()
    # auth_url = netsuite.get_authorization_url()
    # click.echo(f"Visit {auth_url}")
    # response_url = prompt("Paste the return url here")
    # query_string = dict(parse.parse_qsl(parse.urlsplit(response_url).query))
    # code = query_string.get('code')
    # if code:
    #     netsuite.request_access_token(code)

    if netsuite.token.access_token:
        if creds.get('STORAGE_CLASS') == IN_MEMORY_STORAGE:
            if prompt("You have chosen memory storage so nothing is saved here. Echo results?", default="y",
                      type=click.BOOL):
                click.echo(netsuite.token.__dict__)
            else:
                click.echo(f"Saved to {credentials_file}")


if __name__ == "__main__":
    cli()
