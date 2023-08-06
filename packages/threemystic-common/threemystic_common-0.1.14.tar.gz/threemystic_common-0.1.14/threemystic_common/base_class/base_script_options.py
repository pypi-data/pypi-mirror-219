from typing import final
from pathlib import Path  
from argparse import ArgumentParser

class base_process_options:
  def __init__(self, common, *args, **kwargs):
    self._common = common
    
  
  def get_default_options(self, *args, **kwargs):
    return {
      "-v;--verbose": {
        "default": False, 
        "help": "Verbose output",
        "dest": "output_verbose",
        "action": 'store_true'
      }
    }

  def init_default_options(self, parser = None, *args, **kwargs):
    return self.add_arg_parser(parser= parser, arg_keys= self.get_default_options())

  def add_arg_parser(self, arg_keys, parser = None):
    parser = self.get_parser(parser= parser)
    if arg_keys is None:
      return parser

    for (arg, data) in arg_keys.items():
      flags = self._common.helper_type().string().split(arg)
      parser.add_argument(*flags, **data)
    
    return parser


  def get_parser(self, parser = None, parser_args = None, if_init_default_args = True, parser_init_args = None, parser_init_kwargs = None, *args, **kwargs):
    if parser is not None:
      return parser
    
    if parser_init_args is None:
      parser_init_args = []
    
    if parser_init_kwargs is None:
      parser_init_kwargs = {}
    
    if parser_args is None:
      parser_args = {}
    
    return self.add_arg_parser(
      parser= ArgumentParser(*parser_init_args, **parser_init_kwargs),
      arg_keys= ( parser_args if not if_init_default_args else self._common.helper_type().dictionary().merge_dictionary([{}, self.get_default_options(), parser_args ]))
    )
    
  def _process_opts(self, parser, parse_args, namespace, *args, **kwargs):
    default_return = {
      "parser": parser
    }
    if namespace is None:
      processed_data, extra = parser.parse_known_args() if parse_args is None else parser.parse_known_args(parse_args)
      processed_data = vars(processed_data)
      default_return["processed_data"] = processed_data
      default_return["extra"] = extra
      return default_return
    
    _, extra = parser.parse_known_args(namespace= namespace) if parse_args is None else parser.parse_known_args(parse_args, namespace= namespace)
    default_return["extra"] = extra
    return default_return


  def process_opts(self, parser = None, parse_args = None, namespace= None, *args, **kwargs):
    parser = self.get_parser(parser= parser) 

    return self._process_opts(
      parser= parser, 
      parse_args= parse_args, 
      namespace= namespace, 
      *args, **kwargs
    )
    
