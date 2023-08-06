import click
import os
import yaml
import logging
import requests
import shutil
import traceback
import yaml
import textwrap

import junoplatform
from junoplatform.meta.decorators import auth

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')
        
class CMDBase(object):
    def __init__(self):
        self.juno_dir = os.path.expanduser('~') + '/.juno'
        self.juno_file = self.juno_dir +  '/config.yaml'

@click.group()
@click.pass_context
def main(ctx, ):
    ctx.obj = CMDBase()

pass_base = click.make_pass_decorator(CMDBase)

@main.command()
@click.argument('plant')
@click.argument('module', required=True)
@click.argument('conf_file', required=True)
@click.argument('input_file', required=False)
@click.option('--version', help='version', metavar='<string>')
@pass_base
@auth
def package(base, plant, module, conf_file, input_file, version):
    ''' make a package and get a package id
    '''
    logging.info(f"TODO: package {plant} {module} {conf_file} {input_file} {version}")



@main.command()
@click.argument('name')
@pass_base
@auth
def init(base, name):
    '''create an algo module with project NAME
    '''
    home = os.path.dirname(junoplatform.__file__)
    src = f"{home}/templates/main.py"
    try:
        os.makedirs(name, exist_ok=False)
        shutil.copy2(src, name)
        doc = {"name": name, "version": "0.0.1", "author": os.getlogin(), "description": "template algo project"}
        yaml.dump(doc, open(f"{name}/project.yml", "w"), sort_keys=False)
    except Exception as e:
        msg = traceback.format_exc()
        logging.error(f"failed to create project {name}: {e}")

@main.command()
@click.argument('id')
@pass_base
@auth
def deploy(base, id):
    '''deploy package
    '''
    logging.info(f"TODO: deploy {id}")


@main.command()
@click.argument('id')
@pass_base
@auth
def status(base, id):
    ''' check package status
    '''
    logging.info(f"TODO: status {id}")


@main.command()
@click.argument('plant')
@click.argument('module')
@click.argument('id', required=False)
@pass_base
@auth
def rollback(base, plant, module, id):
    '''rollback a package to previous version or specific id[optional]
    '''
    logging.info(f"TODO: rollback {plant} {module} {id}")


@main.command()
@click.argument('plant', required=False)
@pass_base
@auth
def list(base, plant):
    '''list packages and deployed status
    '''
    logging.info(f"TODO: list {plant}")

@main.command()
@click.argument('id')
@pass_base
@auth
def upload(base, id):
    '''upload a package
    '''
    logging.info(f"TODO: upload {id}")
    
@main.command()
@click.argument('username')
@click.argument('password', required=False)
@pass_base
def login(base:CMDBase, username, password):
    '''must login success before all other commands
    '''
    auth = {"username": username, "password": password}
    r = requests.post("https://report.shuhan-juno.com/api/token", data=auth, headers = {'Content-Type': 'application/x-www-form-urlencoded'})
    if r.status_code != 200:
        if 'detail' in r.json():
            detail = r.json()['detail']
            logging.error(f"login error: {detail}")
            return
        else:
            logging.error(f"login error: {r.status_code}")
    token = r.json()['access_token']
    data = {"auth": auth, "token": token}

    with open(base.juno_file, 'w') as f:
        f.write(yaml.dump(data)) 
    logging.info("successfully logged in")