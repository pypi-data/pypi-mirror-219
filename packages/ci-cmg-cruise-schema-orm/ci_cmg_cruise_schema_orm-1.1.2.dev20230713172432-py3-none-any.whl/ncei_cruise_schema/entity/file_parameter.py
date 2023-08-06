from ..orm.entity import Entity, Column
from ..orm.column_consts import DATE_PLACEHOLDER, date_select_name, xml_to_clob_select_name

class FileParameter(Entity):

  @staticmethod
  def _table():
    return "file_parameters"

  def __init__(
      self,
      id=None,
      parameter_detail_id=None,
      file_id=None,
      value=None,
      xml=None,
      json=None,
      last_update_date=None,
      last_updated_by=None
  ):
    self.__parameter_detail_id = parameter_detail_id
    self.__file_id = file_id
    self.__value = value
    self.__xml = xml
    self.__json = json
    self.__last_update_date = last_update_date
    self.__last_updated_by = last_updated_by
    self.__id = id



  @property
  def parameter_detail_id(self):
    return self.__parameter_detail_id

  @parameter_detail_id.setter
  def parameter_detail_id(self, value):
    self.__parameter_detail_id = value

  @property
  def file_id(self):
    return self.__file_id

  @file_id.setter
  def file_id(self, value):
    self.__file_id = value

  @property
  def value(self):
    return self.__value

  @value.setter
  def value(self, value):
    self.__value = value

  @property
  def xml(self):
    return self.__xml

  @xml.setter
  def xml(self, value):
    self.__xml = value

  @property
  def json(self):
    return self.__json

  @json.setter
  def json(self, value):
    self.__json = value

  @property
  def last_update_date(self):
    return self.__last_update_date

  @last_update_date.setter
  def last_update_date(self, value):
    self.__last_update_date = value

  @property
  def last_updated_by(self):
    return self.__last_updated_by

  @last_updated_by.setter
  def last_updated_by(self, value):
    self.__last_updated_by = value

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value


  @classmethod
  def _columns(cls):
    return (
      Column("file_parameter_id", cls.id, id=True, sequence="file_parameters_seq"),
      Column("parameter_detail_id", cls.parameter_detail_id),
      Column("file_id", cls.file_id),
      Column("value", cls.value),
      Column("xml", cls.xml, clob=True, select_name_func=xml_to_clob_select_name),
      Column("json", cls.json, clob=True),
      Column("last_update_date", cls.last_update_date, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name),
      Column("last_updated_by", cls.last_updated_by)
    )