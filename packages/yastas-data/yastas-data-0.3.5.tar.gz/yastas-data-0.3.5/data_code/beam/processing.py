import apache_beam as beam

# SQL Utility 

def format_dict(element):
    formato = {
        "column_name":element[0],
        "udt_name":element[1]
    }
    return formato


# RAW Utility

class SeparateRecords(beam.DoFn):
    def process(self, elements):
        for element in elements:
            yield element

def concat_headers(element):
    info=[]
    names= []
    record = {}
    for name in element[0]:
        names.append(name.name)
    for row in element[1]:
        record = {}
        for name,data in zip(names,row):
            record[name] = data
        info.append(record)
    return info

# TRN Utility

# WRK Utility