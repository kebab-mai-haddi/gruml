import argparse
import os
import shutil

import git

from generate_ruml import gruml


def download_source_code(git_url):
    try:
        root_dir = git_url.split('.git')[0].split('/')[-1]
        directory_path = '/tmp/{}'.format(root_dir)
        try:
            os.makedirs(directory_path)
        except OSError:
            shutil.rmtree(directory_path)
            os.makedirs(directory_path)
        git_repo = git.Git(directory_path).clone(git_url)
        print('Git repo is successfully downloaded: {}'.format(git_repo))
    except Exception as e:
        raise ValueError(e)
    return os.path.join(directory_path, root_dir)


def call_generate_ruml(source_code_link, **kwargs):
    """call gruml function, assume that if use_case is given, all other related 
    arguments will be present, so checking for them can be skipped in here.

    Arguments:
        source_code_link {[type]} -- [description]
    """
    source_code_dir = download_source_code(source_code_link)
    gruml(
        source_code_dir,
        **kwargs
    )


parser = argparse.ArgumentParser()
parser.add_argument("github_repository", type=str,
                    help="generate RUML for the given Github repository which contains the source code")
parser.add_argument("-u", "--use_case", type=str,
                    help="generate use case for the source code")
parser.add_argument("-d", "--driver_name", type=str,
                    help="name of the driver module for the given use case")
parser.add_argument("-dp", "--driver_path", type=str,
                    help="file path of the driver module for the given use case")
parser.add_argument('-df', '--driver_function', type=str,
                    help="function name to be executed for the given use case")

args = parser.parse_args()
source_code_link = args.github_repository
if args.use_case:
    if not args.driver_name or not args.driver_path or not args.driver_function:
        raise ValueError(
            'Use case set to be true but driver details not provided. Please type "python3 gruml-cli.py --help for details."')
    else:
        use_case = args.use_case
        driver_name = args.driver_name
        driver_path = args.driver_path
        driver_function = args.driver_function
    call_generate_ruml(source_code_link, use_case=use_case,
                       driver_name=driver_name, driver_path=driver_path, driver_function=driver_function)
else:
    call_generate_ruml(source_code_link)
