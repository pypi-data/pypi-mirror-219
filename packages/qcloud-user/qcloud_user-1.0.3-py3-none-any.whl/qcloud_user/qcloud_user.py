#!/usr/bin/env python3

import boto3
import botocore
from botocore.exceptions import ClientError

from jose import jwt, jwk
from jose.utils import base64url_decode

import os
import dbm
import sys
import json
import time
import base64
import getpass
import pathlib
import tarfile
import argparse
import requests
import traceback
import configparser


from shutil import rmtree
from pprint import pprint
from datetime import datetime


DEBUG = False


def debug(s):
    if DEBUG: pprint(s)



class QCloudError(Exception):
    pass


def checklist(key, value="", check=False):
    verbose = True
    tick = u'\u2713'
    if verbose and check:
       print("[{0}] {1: <42} {2}".format(tick,key,value))
    elif verbose:
       print("[ ] {0: <42} {1}".format(key,value), end='\r')



class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)



class JobDB():
    def __init__(self):
        db_file = os.path.join(pathlib.Path.home(), ".qcloud_jobs.db")
        self.db = dbm.open(db_file,'c')

    def __del__(self):
        self.db.close()

    def dump(self):
        for key in self.db.keys():
            value = self.db[key]
            print("{} -> {}".format(key.decode(), value.decode()))

    def all_job_ids(self):
        keys = []
        for k in self.db.keys():
            keys.append(k.decode())
        return keys

    def matching_jobs(self, patterns):
        jobs = []
        for k in self.db.keys():
            key = k.decode()
            value = self.db[k].decode()
            for pattern in patterns:
                if pattern in key or pattern in value:
                   jobs.append(key)
        return jobs

    def jobs_match(self, job_ids, pattern):
        jobs = []
        for k in job_ids:
            value = self.db[k].decode()
            #print("Searching for {}:   {} -> {}".format(pattern, k, value))
            if pattern in k or pattern in value:
               jobs.append(k)
        return jobs

    def jobs_not_match(self, job_ids, pattern):
        jobs = []
        for k in job_ids:
            value = self.db[k].decode()
            if pattern not in k and pattern not in value:
               jobs.append(k)
        return jobs

    def get_job_name(self,id):
        job = self.get_job(id)
        name = ''
        if len(job) > 0: name = job[0]
        return name

    def job_exists(self,id):
        job = self.get_job(id)
        return len(job) > 0

    def get_job(self, id):
        fields = []
        id = id.encode()
        if id in self.db.keys():
           value = self.db[id].decode()
           fields = value.split("::")
        return fields

    def set_job(self, id, name, status="BEGIN", date=""):
        values = [name, status, date]
        value = "::".join(values)
        debug("Setting job {} to {}".format(id, value))
        self.db[id] = value

    def remove(self, job_id):
        try:
           del self.db[job_id]
        except KeyError:
           pass
            


def create_session(region):
    session = boto3.Session(region_name=region)
    return session



def reset_password(session, config, session_key):
    cognito   = session.client('cognito-idp')
    username  = config.get("USER", "username")
    client_id = config.get("AWS", "appclientid")

    print("Password reset required for {}".format(username))

    password = None
    while (password == None):
        pw1 = getpass.getpass("Enter new password: ")
        pw2 = getpass.getpass("Confirm password: ")
        if (pw1 == pw2):
           password = pw1
        else:
           print("Passwords do not match")
           
    response = cognito.respond_to_auth_challenge(
        ChallengeName = 'NEW_PASSWORD_REQUIRED',
        ClientId = client_id,
        ChallengeResponses = {
            'USERNAME': username,
            'NEW_PASSWORD': password
         },
         Session = session_key,
    );

    token = update_tokens(config, response)
    return token



def forgot_password(session, config):
    cognito   = session.client('cognito-idp')
    username  = config.get("USER", "username")
    client_id = config.get("AWS", "appclientid")

    code = input("Reset code {}: ".format(username))

    password = None
    while (password == None):
        pw1 = getpass.getpass("Enter new password: ")
        pw2 = getpass.getpass("Confirm password: ")
        if (pw1 == pw2):
           password = pw1
        else:
           print("Passwords do not match")
 
    response = cognito.confirm_forgot_password(
        ClientId = client_id,
        Username = username,
        ConfirmationCode = code,
        Password = password
    )

    debug(response)

    # while we have the password, let's update the tokens
    response = cognito.initiate_auth(
            AuthFlow = 'USER_PASSWORD_AUTH',
            AuthParameters = {
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId = client_id
    )

    token = update_tokens(config, response)
    return token



def get_new_token(session, config):
    cognito   = session.client('cognito-idp')
    username  = config.get("USER", "username")
    client_id = config.get("AWS", "appclientid")

    password  = getpass.getpass("Password for {}: ".format(username))

    response = cognito.initiate_auth(
            AuthFlow = 'USER_PASSWORD_AUTH',
            AuthParameters = {
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId = client_id
    )

    token = update_tokens(config, response)

    if token is None and 'ChallengeName' in response:
       if response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
          session_key = response['Session']
          token = reset_password(session, config, session_key)
       else:
          raise QCloudError("Unhandled authentication challenge: ".format(response['ChallengeName']))

    return token



def update_tokens(config, response):
    # AWS official docs on using tokens with user pools:
    # https://amzn.to/2HbmJG6
    debug("----- Token request response -----")
    debug(response)
    debug("----------------------------------")

    token = None
    region = config.get("AWS", "region")
    userpool = config.get("AWS", "userpoolid")

    if 'AuthenticationResult' in response:
       id_token = response['AuthenticationResult']['IdToken']
       if check_token(id_token, region, userpool):
          config.set("USER", "IdToken", id_token)

       access_token = response['AuthenticationResult']['AccessToken']
       if check_token(access_token, region, userpool):
          config.set("USER", "AccessToken", access_token)

       refresh_token = response['AuthenticationResult']['RefreshToken']
       config.set("USER", "RefreshToken", refresh_token)

       write_config(config)
       token = id_token # this is the one we want to use

    return token



def get_token(session, config):
    region = config.get("AWS", "region")
    userpool = config.get("AWS", "userpoolid")

    token = None
    if config.has_option("USER", "IdToken"):
       token = config.get("USER", "IdToken")

    if token is not None:
       if check_token(token, region, userpool): return token

    token = get_new_token(session, config)

    if (token is None):
       raise QCloudError("Failed to obtain valid access token")

    return token



def check_token(token, region, userpool):
    verified = False
    expired  = False

    token_header = jwt.get_unverified_header(token)
    token_claims = jwt.get_unverified_claims(token)

	# The token header contains Key ID (kid which determines which public key
	# to use to verify the signature
    kid = token_header['kid']

    debug('Token header:')
    debug(token_header)
    debug('Token claims:')
    debug(token_claims)

	# The JSON Web Key Set contains two public keys corresponding to the two
	# private keys that could have been used to sign the token.
    url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region,userpool)
    response = requests.get(url)

    if response.status_code != 200:
       raise QCloudError('Failed to retrieve JWKS: received {}'.format(r.status_code))

    jwks = response.json()
    key_index = -1
    for i in range(len(jwks['keys'])):
        if kid == jwks['keys'][i]['kid']:
            key_index = i
            break

    if key_index == -1:
        raise QCloudError("Failed to verify token: Public key not found")

    public_key = jwk.construct(jwks['keys'][key_index])
    message, encoded_signature = token.rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    if public_key.verify(message.encode("utf8"),decoded_signature):
       verified = True

    claims = jwt.get_unverified_claims(token)
    exp_time = claims["exp"] - time.time()
    if (exp_time < 0):
       expired = True
       debug("Now: {}".format(int(time.time())))
       debug("Exp: {}".format(claims["exp"]))

    debug("Signature verified: {}".format(verified))
    debug("Token expired:      {}".format(expired))
    debug("Time left:          {}s".format(int(exp_time)))

    return verified and not expired



#################################################################################


def base_url(config):
    region = config.get("AWS", "region")
    api_id = config.get("AWS", "apigatewayid")
    url = 'https://{}.execute-api.{}.amazonaws.com/exec/qcloud?function='.format(api_id, region)
    return url



def submit(token, filenames, ncpu, config, db):
    for filename in filenames:
        if not os.path.exists(filename):
           raise QCloudError("No such file or directory: {}".format(filename))

    headers = {'Authorization': token, 
               'slurm_options': '--cpus-per-task={}'.format(ncpu)}

    url = base_url(config) + "submit"
    debug("Sending request to URL: {}".format(url))

    for filename in filenames:
        with open(filename) as file:
            body = file.read(); 
        if not filename.endswith('.json'):
           inp = body.splitlines()
           body = json.dumps({ "input_file": inp })

        response = requests.post(url, headers=headers, data=body)
        if "Submitted job id" in response.text: 
           job_id   = response.text.replace("Submitted job id ","")
           job_name = pathlib.Path(filename).stem
           db.set_job(job_id, job_name)
           #print("{}:  {}".format(response.text, job_name))
           checklist("{}: ".format(response.text), job_name, True)
        else:
           print("[x] Problem submitting job: {}".format(repsonse))



def tail(token, job_ids, config, db):
    if not job_ids: return ""
    headers = {'Authorization': token}
    job_id = ",".join(job_ids)

    url = base_url(config) + "tail&job_id={}".format(job_id)
    debug("Sending request to URL: {}".format(url))

    response = requests.get(url, headers=headers)
    text = response.text.strip()
    for id in job_ids:
        name = db.get_job_name(id)
        text = text.replace(id, "{} [{}]".format(name, id))
    
    return text



def cancel(token, job_ids, config, db):
    if not job_ids: return ""

    active  = db.jobs_match(job_ids, "BEGIN") 
    active += db.jobs_match(job_ids, "QUEUED") 
    active += db.jobs_match(job_ids, "RUNNING")
             
    jobs = list(set(job_ids) & set(active))
    job_id = ",".join(jobs)

    headers = {'Authorization': token}
    url = base_url(config) + "cancel&job_id={}".format(job_id)
    debug("Sending request to URL: {}".format(url))
    response = requests.get(url, headers=headers)
    text = response.text.strip()

    return status(token, jobs, config, db)


def valid_status(line):
    statuses = [
        'BEGIN', 
        'COPIED', 
        'COPY FAILED', 
        'QUEUED', 
        'RUNNING', 
        'FINISHED', 
        'ERROR', 
        'ARCHIVED', 
        'ARCHIVED FAILED', 
        'DOWNLOADED', 
        'CANCELLED' 
    ]
    res = [s for s in statuses if(s in line)]
    return bool(res)


def status(token, job_ids, config, db):
    if not job_ids: return ""
    # These statuses do not change remotely
    no_change  = db.jobs_match(job_ids, "ARCHIVED") 
    no_change += db.jobs_match(job_ids, "DOWNLOADED")
    no_change += db.jobs_match(job_ids, "CANCELLED")
    #no_change += db.jobs_match(job_ids, "ERROR")

    jobs = list(set(job_ids)-set(no_change))
    all  = info(token, jobs, config, db).splitlines()
    all  = reversed(all)  # get the latest status update
    id   = None
    ret  = []

    for line in all:
        if 'Job' in line and valid_status(line):
           tokens = line.split()
           debug(tokens)

           if id != tokens[4] and len(tokens) == 6:
              id = tokens[4]
              status = tokens[5]
              date = " ".join(tokens[:3])
              name = db.get_job_name(id)
              db.set_job(id, name, status, date)
              ret.append("Job ID {}:  {}  {:10}  {}  ".format(id,date,status,name))
        else:
            ret.append(line)

    for id in no_change:
        name,status,date = db.get_job(id)
        ret.append("Job ID {}:  {}  {:10}  {}  ".format(id,date,status,name))

    return "\n".join(ret)



def info(token, job_ids, config, db):
    if not job_ids: return ""
    headers = {'Authorization': token}
    job_id = ",".join(job_ids)

    url = base_url(config) + "status&job_id={}".format(job_id)
    debug("Sending request to URL: {}".format(url))

    response = requests.get(url, headers=headers)
    text = response.text.strip()
    return text



def download(token, job_ids, config, db):
    if not job_ids: return ""
    headers = {'Authorization': token}
    region  = config.get("AWS", "region")
    api_id  = config.get("AWS", "apigatewayid")
    
    #jobs = db.jobs_match(job_ids, "ARCHIVED")
    #jobs = jobs + db.jobs_match(job_ids, "DOWNLOADED")
    jobs = job_ids

    arrow = u'\u23AF\u2192'
    for job_id in jobs:
        checklist("Downloading {}".format(job_id))
        url = base_url(config) + "download&job_id={}".format(job_id)
        debug("Sending request to URL: {}".format(url))

        response = requests.get(url, headers=headers)
        contents = response.text
        decoded  = base64.b64decode(contents)

        tar = "{}.tgz".format(job_id)
        debug("Writing {}".format(tar))
        with open(tar,'wb') as file:
            file.write(decoded)

        try: 
           with tarfile.open(tar) as file:
               file.extractall("./")
        except tarfile.ReadError:
           if os.path.exists(tar):
              os.remove(tar)
           print("[x] Download  {} failed, check job status".format(job_id))
           continue

        os.remove(tar)

        name = db.get_job_name(job_id)
        move = True
        dest = job_id
        if os.path.exists(name):
           response = input("Directory {} exists, overwrite? [y/N] ".format(name))
           move = (response == "y" or response == "yes")
           if move: rmtree(name)

        if move and name: 
           os.rename(job_id, name)
           dest = name

        path = os.path.join(dest, "input")
        if os.path.exists(path):
           newpath = os.path.join(dest, "{}.inp".format(dest))
           os.rename(path, newpath)

        path = os.path.join(dest, "output")
        if os.path.exists(path):
           newpath = os.path.join(dest, "{}.out".format(dest))
           os.rename(path, newpath)

        path = os.path.join(dest, "input.fchk")
        if os.path.exists(path):
           newpath = os.path.join(dest, "{}.fchk".format(dest))
           os.rename(path, newpath)

        checklist("Downloaded  {}".format(job_id),"{} {}".format(arrow, dest), True)
        date = datetime.now()
        date = date.strftime("%b %d %H:%M:%S")
        db.set_job(job_id, name, "DOWNLOADED", date)



def clear(token, job_ids, config, db):
    jobs  = db.jobs_match(job_ids, "DOWNLOADED")
    jobs += db.jobs_match(job_ids, "CANCELLED")
    jobs += db.jobs_match(job_ids, "ERROR")
    jobs += db.jobs_match(job_ids, "FAILED")

    for job in jobs:
        checklist("Clearing {}".format(job))
        db.remove(job)
        checklist("Cleared  {}".format(job),"", True)


def remove(token, job_ids, config, db):
    for job in job_ids:
        if db.job_exists(job):
           checklist("Removing {}".format(job))
           db.remove(job)
           checklist("Removed  {}".format(job),"", True)




###########################################################################


def config_file_path():
    config_file = os.path.join(pathlib.Path.home(), ".qcloud_client.cfg")
    return config_file




def load_config():
    path = config_file_path()
    debug('Using config file {}'.format(path))
    config = configparser.ConfigParser()
    config.read(path)
    return config


def write_config(config):
    path = config_file_path()
    with open(path, 'w') as cfg:
       config.write(cfg)


def set_config_option(config, section, option, prompt):
    value = ''
    if config.has_option(section, option):
       default = config.get(section, option)
       value = input("{} [{}]: ".format(prompt, default)) or default
    else:
       value = input("{}: ".format(prompt))
    config.set(section, option, value)


def configure(settings):
    config = load_config()
    print("Please contact your Q-Cloud administrator for required values")

    if ("AWS" not in config): config.add_section("AWS")
    set_config_option(config, "AWS", "Region", "AWS Region")
    set_config_option(config, "AWS", "UserPoolId", "User pool ID")
    set_config_option(config, "AWS", "AppClientId", "App client ID")
    set_config_option(config, "AWS", "ApiGatewayId", "API gateway ID")

    if ("USER" not in config): config.add_section("USER")
    set_config_option(config, "USER", "username", "User name")
    config.remove_option("USER", "refreshtoken")
    config.remove_option("USER", "accesstoken")
    config.remove_option("USER", "idtoken")

    write_config(config)
    return




###########################################################################


def main():
    try:
        parser = MyParser();

        parser.add_argument("--configure", dest="config", action='store_true',
            help="configure qcloud settings")

        parser.add_argument("--pwreset", dest="pwreset", action='store_true',
            help="password reset using a code")

        parser.add_argument("--submit", dest="submit", action='store_true',
            help="submit job(s)")

        parser.add_argument("--ncpu", dest="ncpu", default = 1,
            help="specify the number of openmp threads to use.")
        parser.add_argument("--ncpus", dest="ncpu", default = 1,
            help="specify the number of openmp threads to use.")

        parser.add_argument("--cancel", dest="cancel", action='store_true',
            help="cancel queued or running job(s)")

        parser.add_argument("--info", dest="info", action='store_true',
            help="print the timestamps for each state for each job")

        parser.add_argument("--status", dest="status", action='store_true',
            help="print the status of the specified job(s)")

        parser.add_argument("--tail", dest="tail", action='store_true',
            help="print the last lines of the specified job(s)")

        parser.add_argument("--download", dest="get", action='store_true',
            help="download the ouput from the specified job(s)")

        parser.add_argument("--get", dest="get", action='store_true',
            help="download the ouput from the specified job(s)")

        parser.add_argument("--clear", dest="clear", action='store_true',
            help="clear downloaded jobs from registry")

        parser.add_argument("--remove", dest="remove", action='store_true',
            help="remove jobs from registry regardless of status")

        parser.add_argument("--dump", dest="dump", action='store_true',
            help="dump contents of local job database")

        parser.add_argument("--debug", dest="debug", action='store_true',
            help="add debug printing")

        args, extra_args = parser.parse_known_args()

        if args.debug:
           global DEBUG 
           DEBUG = True

        if not os.path.exists(config_file_path()) or args.config:
           configure(extra_args)
           exit()
           
        config = load_config()
        session = create_session(config.get("AWS", "Region"))

        if args.pwreset:
           forgot_password(session, config)
           exit()

        token = get_token(session, config)
        debug("Using token:\n{}".format(token))

        if token is None:
           raise QCloudError("Failed to obtain a vaild token")

        db = JobDB()

        if args.tail:
           jobs = db.matching_jobs(extra_args)
           ret  = tail(token, jobs, config, db)
           print(ret)

        elif args.info:
           jobs = db.matching_jobs(extra_args)
           ret  = info(token, jobs, config, db)
           print(ret)

        elif args.status:
           if len(extra_args) > 0:
              jobs = db.matching_jobs(extra_args)
           else:
              jobs = db.all_job_ids()
           ret  = status(token, jobs, config, db)
           print(ret)

        elif args.cancel:
           if len(extra_args) > 0:
              ret  = cancel(token, extra_args, config, db)
              print(ret)

        elif args.get:
           jobs = db.matching_jobs(extra_args)
           download(token, jobs, config, db)

        elif args.clear:
           if len(extra_args) > 0:
              jobs = db.matching_jobs(extra_args)
           else:
              jobs = db.all_job_ids()
           clear(token, jobs, config, db)

        elif args.remove:
           if len(extra_args) > 0:
              remove(token, extra_args, config, db)

        elif args.submit:
           ret = submit(token, extra_args, args.ncpu, config, db)

        elif args.dump:
           db.dump()

        else:
           print("Invalid option")


    except KeyboardInterrupt:
        print("\n")
        pass 

    except FileNotFoundError as e:
        print(e)

    except QCloudError as e:
        print("\nERROR: ",e)

    except configparser.NoOptionError as e:
        print("Invalid qcloud configuration file: {}".format(e))

    except botocore.exceptions.ClientError as e:
        print(e)

    except botocore.exceptions.ProfileNotFound as e:
        print(e)

    except Exception as e:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
