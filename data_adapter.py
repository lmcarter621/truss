from datetime import datetime
import pytz
import csv
import sys

class DataAdapter:
  # these should only be accessible from within the class
  data_rows = []
  header_row = []

  @staticmethod
  def translate_data(filename):
    DataAdapter.__ingest_data(filename)
    DataAdapter.__writing_data()

  @staticmethod
  def __ingest_data(filename):
    with open(filename, 'rb') as data_file:
      rows_in_csv = csv.reader(data_file, delimiter=',')
      rows_list = list(rows_in_csv)

      DataAdapter.header_row = rows_list[0]
      for row in rows_list[1:]:
        DataAdapter.data_rows.append(DataRow(row))

  @staticmethod
  def __writing_data():
    filename = "results/cleansed_data_{0}.csv".format(datetime.utcnow())
    with open(filename, 'wb') as cleansed_data:
      csvwriter = csv.writer(cleansed_data, delimiter=',')
      csvwriter.writerow(DataAdapter.header_row)
      for row in DataAdapter.data_rows:
        csvwriter.writerow(row.format_row())

class DataRow:
  def __init__(self, row):
    self.timestamp = row[0]
    self.address = row[1]
    self.zip = row[2]
    self.full_name = row[3]
    self.foo_duration = row[4]
    self.bar_duration = row[5]
    self.total_duration = row[6]
    self.notes = row[7]

  def format_row(self):
    row = []
    row.append(self.__formatted_timestamp())
    row.append(self.__validate_address())
    row.append(self.__foramtted_zip())
    row.append(self.__formatted_name())
    row.append(self.__formatted_foo_duration())
    row.append(self.__formatted_bar_duration())
    row.append(self.__formatted_total_duration())
    row.append(self.notes) # should verify unicode characters

    return row

  def __formatted_timestamp(self):
    pdt = pytz.timezone("America/Los_Angeles")
    edt = pytz.timezone("America/New_York")

    naive_datetime = datetime.strptime(self.timestamp, "%m/%d/%y %I:%M:%S %p")
    pdt_aware_timezone = pdt.localize(naive_datetime)
    edt_aware_timezone = pdt_aware_timezone.astimezone(edt)

    return edt_aware_timezone.isoformat()

  def __foramtted_zip(self):
    return self.zip if len(self.zip) == 5 else 0

  def __formatted_name(self):
    return self.full_name.upper()

  def __validate_address(self):
    if isinstance(self.address, unicode):
      return self.address 
    else: 
      try:
        return unicode(self.address)
      except:
        sys.stderr.write("Invalid address! {0} \n".format(self.address))

  def __validate_notes(self):
    # str.decode("utf-8").replace(u"\u2022", "*").encode("utf-8")
    decoded = self.notes.decode("utf-8")
    replaced = decoded.replace(u"\u2022", "*")
    re_encoded = replaced.encode("utf-8")
    return re_encoded

  def __formatted_duration_floating_point_seconds(self, duration_as_string):
    duration_parts = duration_as_string.split(":")
    hours_to_seconds = float(duration_parts[0]) * 3600
    minutes_to_seconds = float(duration_parts[1]) * 60
    seconds = float(duration_parts[2])

    return hours_to_seconds + minutes_to_seconds + seconds

  def __formatted_foo_duration(self):
    return self.__formatted_duration_floating_point_seconds(
      self.foo_duration)

  def __formatted_bar_duration(self):
    return self.__formatted_duration_floating_point_seconds(
      self.bar_duration)

  def __formatted_total_duration(self):
    return self.__formatted_foo_duration() + self.__formatted_bar_duration()


if __name__ == '__main__':
  filename = sys.argv[1]
  DataAdapter.translate_data(filename)
