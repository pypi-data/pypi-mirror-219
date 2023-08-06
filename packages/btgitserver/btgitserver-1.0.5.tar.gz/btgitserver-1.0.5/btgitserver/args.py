import argparse
from argparse import RawTextHelpFormatter
from btgitserver.defaults import app_name

def parse_args(**kwargs):
    parser = argparse.ArgumentParser(
        description="Standalone git server written in python",
        formatter_class=RawTextHelpFormatter,
        epilog="""
        This program is a git server implementation written in python.
        Refer to the README.md for setup and dependency information.
        The program defaults can be overridden via a yaml-formatted config file.
        or specified via commandline
        
        The config file must conform to the following data structure:
        
        auth:
          users:
            username1:
              password: password1
            username2:
              password: password2
        
        app:
          debug: false
          listen: "0.0.0.0"
          port: 5000
          search_paths: 
            - ~/repos
        """,
        fromfile_prefix_chars='@')
    parser.add_argument(
        "-host",
        "--host-address",
        help="Override listening address",
        metavar="ARG", required=False)
    parser.add_argument(
        "-p",
        "--port",
        help="Override listening port",
        metavar="ARG", required=False)
    parser.add_argument(
        "-w",
        "--workers",
        help="Override number of gunicorn workers",
        metavar="ARG", required=False)    
    parser.add_argument('--no-verify-tls', '-notls',action='store_true', help='Verify SSL cert when downloading web content')
    parser.add_argument('--config-file', '-f', help="Path to config file override")
    parser.add_argument('--repo-search-paths', '-r', nargs='+', help="List of directories containing git repositories")
    parser.add_argument('--logfile-path', '-L', help="Path to logfile")
    parser.add_argument('--logfile-write-mode', '-Lw', default='w', choices=['a', 'w'], help="File mode when writing to log file, 'a' to append, 'w' to overwrite")    
    parser.add_argument('--debug', action='store_true')
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    
    return parser.parse_args()