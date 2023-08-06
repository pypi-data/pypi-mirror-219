from threemystic_common.base_class.base_common import base
from currency_converter import CurrencyConverter


class helper_currency(base): 
  """This helper_currency a set of library wrappers to help around expending json libary"""

  def __init__(self, fallback_on_wrong_date = True, use_decimal = False, fallback_on_missing_rate= True, fallback_on_missing_rate_method= "linear_interpolation", *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_currency", *args, **kwargs)
    self.__currency_convert = CurrencyConverter(
      fallback_on_wrong_date= fallback_on_wrong_date,
      decimal= use_decimal,
      fallback_on_missing_rate= fallback_on_missing_rate,
      fallback_on_missing_rate_method= fallback_on_missing_rate_method
    )
    


  def convert(self, ammount, currency_from, currency_to = "USD", conversion_date = None, *args, **kwargs):   
    return self.__currency_convert.convert(
      amount= ammount,
      currency= currency_from,
      new_currency=currency_to,
      date= conversion_date
    )
