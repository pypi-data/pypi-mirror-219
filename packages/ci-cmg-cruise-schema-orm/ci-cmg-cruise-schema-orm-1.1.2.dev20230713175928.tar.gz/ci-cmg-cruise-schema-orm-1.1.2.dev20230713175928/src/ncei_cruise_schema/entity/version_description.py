from ..orm.entity import Entity, Column

class VersionDescription(Entity):
  
  @staticmethod
  def _table():
    return "version_descriptions"
  
  def __init__(self, id=None, version_number=None, version_level=None, description=None):
    self.__id = id
    self.__version_number = version_number
    self.__version_level = version_level
    self.__description = description

  @property
  def version_number(self):
    return self.__version_number

  @version_number.setter
  def version_number(self, value):
    self.__version_number = value

  @property
  def version_level(self):
    return self.__version_level

  @version_level.setter
  def version_level(self, value):
    self.__version_level = value

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def description(self):
    return self.__description

  @description.setter
  def description(self, value):
    self.__description = value

  @classmethod
  def _columns(cls):
    return (
      Column("version_id", cls.id, id=True, sequence="version_descriptions_seq"),
      Column("version_number", cls.version_number),
      Column("version_level", cls.version_level),
      Column("description", cls.description),
    )

