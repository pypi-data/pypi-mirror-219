WKT_PLACEHOLDER = "SDO_GEOMETRY(?, 8307)"
DATEANDTIME_PLACEHOLDER = "TO_DATE(?,'YYYY-MM-DD\"T\"HH24:MI:SS')"
DATE_PLACEHOLDER = "TO_DATE(?,'DD-MON-YY')"

def wkt_select_name(name):
  return "TO_CLOB(SDO_UTIL.TO_WKTGEOMETRY({name}))".format(name=name)

def datetime_select_name(name):
  return "TO_CHAR({name},'DD-MON-YY\"T\"HH24:MI:SS')".format(name=name)

def date_select_name(name):
  return "TO_CHAR({name},'DD-MON-YY')".format(name=name)
def xml_to_clob_select_name(name):
  return "{name}.getClobVal()".format(name=name)