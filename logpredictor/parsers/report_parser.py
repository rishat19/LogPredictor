import re
import csv
import os


class ReportParser:
    def __init__(self, filename: str):
        self.path = os.path.abspath('').replace('\\', '/').replace('parsers', 'tmp')
        with open(self.path + '/' + filename, 'r', encoding='utf-8') as f:
            self.content = f.read()
        self.merged_data = {}

    def __parse_queries_per_second(self):
        pattern = r'var queriespersecond_graph_1_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'queriespersecond_' + match.group(0)[30]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_select_queries(self):
        pattern = r'var selectqueries_graph_4_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'selectqueries_' + match.group(0)[27]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_write_queries(self):
        pattern = r'var writequeries_graph_5_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'writequeries_' + match.group(0)[26]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_duration_queries(self):
        pattern = r'var durationqueries_graph_6_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'durationqueries_' + match.group(0)[29]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_bind_prepare_queries(self):
        pattern = r'var bindpreparequeries_graph_7_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'bindpreparequeries_' + match.group(0)[32]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_connections_per_second(self):
        pattern = r'var connectionspersecond_graph_2_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'connectionspersecond_' + match.group(0)[34]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_sessions_per_second(self):
        pattern = r'var sessionspersecond_graph_3_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'sessionspersecond_' + match.group(0)[31]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_checkpoint_write_buffers(self):
        pattern = r'var checkpointwritebuffers_graph_16_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'checkpointwritebuffers_' + match.group(0)[37]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_checkpoint_files(self):
        pattern = r'var checkpointfiles_graph_17_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'checkpointfiles_' + match.group(0)[30]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_checkpoint_distance(self):
        pattern = r'var checkpointdistance_graph_18_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'checkpointdistance_' + match.group(0)[33]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_temporary_data(self):
        pattern = r'var temporarydata_graph_17_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'temporarydata_' + match.group(0)[28]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_temporary_file(self):
        pattern = r'var temporaryfile_graph_18_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'temporaryfile_' + match.group(0)[28]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __parse_autovacuum(self):
        pattern = r'var autovacuum_graph_22_d\d = \[(.*?)\];'
        data = {}
        for match in re.finditer(pattern, self.content, re.DOTALL):
            name = 'autovacuum_' + match.group(0)[25]
            rows = match.group(1).split('],[')
            data[name] = self.__transform_rows(rows)
        self.__merge_data_by_time(data)

    def __transform_rows(self, rows):
        rows = [row.strip('[]').split(',') for row in rows]
        rows = [[int(row[0]), float(row[1])] for row in rows]
        return rows

    def __merge_data_by_time(self, data: dict):
        for name, rows in data.items():
            for row in rows:
                time = row[0]
                value = row[1]
                if time not in self.merged_data:
                    self.merged_data[time] = {}
                self.merged_data[time][name] = value

    def __write_csv(self):
        with open(self.path + '/tmp/report_parser_out.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['time', 'queriespersecond_1', 'queriespersecond_2', 'queriespersecond_3', 'selectqueries_1',
                 'selectqueries_2', 'selectqueries_3', 'writequeries_1', 'writequeries_2', 'writequeries_3',
                 'durationqueries_1', 'durationqueries_2', 'durationqueries_3', 'bindpreparequeries_1',
                 'bindpreparequeries_2', 'bindpreparequeries_3', 'connectionspersecond_1', 'connectionspersecond_2',
                 'connectionspersecond_3', 'sessionspersecond_1', 'sessionspersecond_2', 'sessionspersecond_3',
                 'checkpointwritebuffers_1', 'checkpointfiles_1', 'checkpointfiles_2', 'checkpointfiles_3',
                 'checkpointdistance_1', 'checkpointdistance_2', 'temporarydata_1', 'temporaryfile_1', 'autovacuum_1',
                 'autovacuum_2'])
            for time, values in self.merged_data.items():
                row = [time, values.get('queriespersecond_1', 0.0), values.get('queriespersecond_2', 0.0),
                       values.get('queriespersecond_3', 0.0), values.get('selectqueries_1', 0.0),
                       values.get('selectqueries_2', 0.0), values.get('selectqueries_3', 0.0),
                       values.get('writequeries_1', 0.0), values.get('writequeries_2', 0.0),
                       values.get('writequeries_3', 0.0), values.get('durationqueries_1', 0.0),
                       values.get('durationqueries_2', 0.0), values.get('durationqueries_3', 0.0),
                       values.get('bindpreparequeries_1', 0.0), values.get('bindpreparequeries_2', 0.0),
                       values.get('bindpreparequeries_3', 0.0), values.get('connectionspersecond_1', 0.0),
                       values.get('connectionspersecond_2', 0.0), values.get('connectionspersecond_3', 0.0),
                       values.get('sessionspersecond_1', 0.0), values.get('sessionspersecond_2', 0.0),
                       values.get('sessionspersecond_3', 0.0), values.get('checkpointwritebuffers_1', 0.0),
                       values.get('checkpointfiles_1', 0.0), values.get('checkpointfiles_2', 0.0),
                       values.get('checkpointfiles_3', 0.0), values.get('checkpointdistance_1', 0.0),
                       values.get('checkpointdistance_2', 0.0), values.get('temporarydata_1', 0.0),
                       values.get('temporaryfile_1', 0.0), values.get('autovacuum_1', 0.0),
                       values.get('autovacuum_2', 0.0)]
                writer.writerow(row)

    def parse(self):
        self.__parse_queries_per_second()
        self.__parse_select_queries()
        self.__parse_write_queries()
        self.__parse_duration_queries()
        self.__parse_bind_prepare_queries()
        self.__parse_connections_per_second()
        self.__parse_sessions_per_second()
        self.__parse_checkpoint_write_buffers()
        self.__parse_checkpoint_files()
        self.__parse_checkpoint_distance()
        self.__parse_temporary_data()
        self.__parse_temporary_file()
        self.__parse_autovacuum()
        self.__write_csv()

# report_parser = ReportParser('out_test.html')
# report_parser.parse()
