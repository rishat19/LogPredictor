import os

from visualizer.page_rebuilder import PageRebuilder


class ReportWriter:
    def __init__(self):
        self.path = os.path.abspath('').replace('\\', '/').replace('report_generator', 'tmp')
        with open(self.path + '/tmp/rnn_out.csv') as f:
            self.data = f.read().splitlines()
        self.rows = []

    def __create_rows(self):
        rows_data = []
        for i in range(31):
            rows_data.append([])

        for line in self.data:
            values = line.split(',')
            for i in range(31):
                if i not in [9, 10, 11, 14]:
                    rows_data[i].append([int(float(values[0])), int(float(values[i + 1]))])
                else:
                    rows_data[i].append([int(float(values[0])), float(values[i + 1])])
        self.rows.append('var queriespersecond_predict_graph_1_d1 = ' + str(rows_data[0]) + ';\n')
        self.rows.append('var queriespersecond_predict_graph_1_d2 = ' + str(rows_data[1]) + ';\n')
        self.rows.append('var queriespersecond_predict_graph_1_d3 = ' + str(rows_data[2]) + ';\n')
        self.rows.append('var selectqueries_predict_graph_4_d1 = ' + str(rows_data[3]) + ';\n')
        self.rows.append('var selectqueries_predict_graph_4_d2 = ' + str(rows_data[4]) + ';\n')
        self.rows.append('var selectqueries_predict_graph_4_d3 = ' + str(rows_data[5]) + ';\n')
        self.rows.append('var writequeries_predict_graph_5_d1 = ' + str(rows_data[6]) + ';\n')
        self.rows.append('var writequeries_predict_graph_5_d2 = ' + str(rows_data[7]) + ';\n')
        self.rows.append('var writequeries_predict_graph_5_d3 = ' + str(rows_data[8]) + ';\n')
        self.rows.append('var durationqueries_predict_graph_6_d1 = ' + str(rows_data[9]) + ';\n')
        self.rows.append('var durationqueries_predict_graph_6_d2 = ' + str(rows_data[10]) + ';\n')
        self.rows.append('var durationqueries_predict_graph_6_d3 = ' + str(rows_data[11]) + ';\n')
        self.rows.append('var bindpreparequeries_predict_graph_7_d1 = ' + str(rows_data[12]) + ';\n')
        self.rows.append('var bindpreparequeries_predict_graph_7_d2 = ' + str(rows_data[13]) + ';\n')
        self.rows.append('var bindpreparequeries_predict_graph_7_d3 = ' + str(rows_data[14]) + ';\n')
        self.rows.append('var connectionspersecond_predict_graph_2_d1 = ' + str(rows_data[15]) + ';\n')
        self.rows.append('var connectionspersecond_predict_graph_2_d2 = ' + str(rows_data[16]) + ';\n')
        self.rows.append('var connectionspersecond_predict_graph_2_d3 = ' + str(rows_data[17]) + ';\n')
        self.rows.append('var sessionspersecond_predict_graph_3_d1 = ' + str(rows_data[18]) + ';\n')
        self.rows.append('var sessionspersecond_predict_graph_3_d2 = ' + str(rows_data[19]) + ';\n')
        self.rows.append('var sessionspersecond_predict_graph_3_d3 = ' + str(rows_data[20]) + ';\n')
        self.rows.append('var checkpointwritebuffers_predict_graph_16_d1 = ' + str(rows_data[11]) + ';\n')
        self.rows.append('var checkpointfiles_predict_graph_17_d1 = ' + str(rows_data[12]) + ';\n')
        self.rows.append('var checkpointfiles_predict_graph_17_d2 = ' + str(rows_data[13]) + ';\n')
        self.rows.append('var checkpointfiles_predict_graph_17_d3 = ' + str(rows_data[14]) + ';\n')
        self.rows.append('var checkpointdistance_predict_graph_18_d1 = ' + str(rows_data[15]) + ';\n')
        self.rows.append('var checkpointdistance_predict_graph_18_d2 = ' + str(rows_data[16]) + ';\n')
        self.rows.append('var temporarydata_predict_graph_17_d1 = ' + str(rows_data[17]) + ';\n')
        self.rows.append('var temporaryfile_predict_graph_18_d1 = ' + str(rows_data[18]) + ';\n')
        self.rows.append('var autovacuum_predict_graph_22_d1 = ' + str(rows_data[19]) + ';\n')
        self.rows.append('var autovacuum_predict_graph_22_d2 = ' + str(rows_data[20]) + ';\n')

    def write(self):
        self.__create_rows()
        page_rebuilder = PageRebuilder(input_file=self.path + '/tmp/pgbadger_out.html',
                                       output_file=os.path.abspath('').replace('\\', '/').replace('report_generator',
                                                                                                  '') + '/report.html',
                                       rows=self.rows)
        page_rebuilder.rebuild()

# report_writer = ReportWriter()
# report_writer.write()
