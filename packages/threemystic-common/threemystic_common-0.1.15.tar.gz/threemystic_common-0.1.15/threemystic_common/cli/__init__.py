import sys


def main(*args, **kwargs):
  from threemystic_common.common import common

  print(f"Thank you for using the 3 Mystic Apes Common Library. You currenly have installed 3mystic_common version {common().version()}")

if __name__ == '__main__':   
  main(sys.argv[1:])