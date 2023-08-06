from threemystic_common.domain.cmdb.base_class.base import cmdb_base as base


class cmdb_aws(base): 
  """This is a common set of methods and libraries"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= "cmdb_aws", *args, **kwargs)
  
  def get_source(self, *args, **kwargs):
    return "aws"
  
  def __generate_resource_tags_csv_tag(self, tag, tag_attributes, tag_attribute_seperator):
    return tag_attribute_seperator.join([str(tag[attr]) for attr in tag if attr in tag_attributes])

  def generate_resource_tags_csv(self, tags, seperator=",", tag_attribute_seperator=":", tag_attributes = ["Key", "Value"]):
    if tags is None:
      return None
    return seperator.join([self.__generate_resource_tags_csv_tag(tag = tag, tag_attributes = tag_attributes, tag_attribute_seperator=tag_attribute_seperator) for tag in tags])

  