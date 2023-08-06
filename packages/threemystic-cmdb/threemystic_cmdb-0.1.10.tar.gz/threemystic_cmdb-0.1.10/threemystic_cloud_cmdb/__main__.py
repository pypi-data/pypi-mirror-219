import sys


def main(*args, **kwargs):
  from threemystic_cloud_cmdb.cli import cloud_cmdb_cli
  cloud_cmdb_cli().main(*args, **kwargs)
  

if __name__ == '__main__':   
  main(sys.argv[1:])