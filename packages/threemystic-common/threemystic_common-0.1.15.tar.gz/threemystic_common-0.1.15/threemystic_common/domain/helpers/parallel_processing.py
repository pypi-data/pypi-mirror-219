import asyncio
from threemystic_common.base_class.base_common import base


class helper_parallel_processing(base): 
  """This is a set of library wrappers to help around expending json libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_parallel_processing", *args, **kwargs)
  
  async def ensure_all_tasks_complete(self, done_function, done_function_params, total_tasks = None, current_running_total = None, verbose = False):
    running_done_count = current_running_total if current_running_total is not None else 0
    
    return_data = None
    pending_tasks = None
    process_result_data = []
    while pending_tasks is None or len(pending_tasks) > 0:
      await asyncio.sleep(.5)
      process_result = (await done_function(**done_function_params))
      process_result_data.append(process_result)      
      pending_tasks = process_result["tasks"]
      running_done_count += process_result["done_count"]
      
      if process_result.get("data") is not None:
        if return_data is None:
          return_data = process_result.get("data")
          continue

        if self._main_reference.helper_type().general().is_type(process_result.get("data"), list):
          return_data += process_result.get("data")
        elif self._main_reference.helper_type().general().is_type(process_result.get("data"), dict):
          for key, item in process_result.get("data").items():
            if return_data[key] is None:
              return_data[key] = item
              continue
            return_data[key] += item

      if total_tasks is not None and verbose:
        print("Total Processed {} / {}".format(running_done_count, total_tasks), flush= True)
    
    return {
      "running_done_count": running_done_count,
      "data": return_data,
      "process_result_data": process_result_data
    }
