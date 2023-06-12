class PageRebuilder:
    def __init__(self, input_file, output_file, rows):
        self.input_file = input_file
        self.output_file = output_file
        self.rows = rows
        self.new_content = []

    def __add_new_arrays(self):
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
        position = -1
        for i in range(len(content)):
            if 'var queriespersecond_graph_1_d3' in content[i]:
                position = i
                break
        if position == -1:
            raise ValueError('Cannot find queriespersecond_graph_1_d3 line')
        self.new_content = content[:position + 1]
        for i in range(len(self.rows)):
            self.new_content.append(self.rows[i])
        self.new_content += content[position + 1:]

    def __rewrite_legends(self):
        for i in range(len(self.new_content)):
            if 'var series_arr = [ { label: "Maximum' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "Maximum", color: "#6e9dc9" },{ label: "Average", ' \
                                      'color: "#f4ab3a" },{ label: "Minimum", color: "#ac7fa8" },{ label: "Maximum ' \
                                      'prediction", color: "#2a5073" },{ label: "Average prediction", ' \
                                      'color: "#915a07" },{ label: "Minimum prediction", color: "#573854" } ];\n '
            if 'var series_arr = [ { label: "DELETE queries' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "DELETE queries", color: "#6e9dc9" },{ label: ' \
                                      '"INSERT queries", color: "#f4ab3a" },{ label: "UPDATE queries", ' \
                                      'color: "#ac7fa8" },{ label: "DELETE queries prediction", color: "#2a5073" },' \
                                      '{ label: "INSERT queries prediction", color: "#915a07" },{ label: "UPDATE ' \
                                      'queries prediction", color: "#573854" } ];\n '
            if 'var series_arr = [ { label: "All queries' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "All queries", color: "#6e9dc9" },{ label: "Select ' \
                                      'queries", color: "#f4ab3a" },{ label: "Write queries", color: "#ac7fa8" },' \
                                      '{ label: "All queries prediction", color: "#2a5073" },{ label: "Select queries ' \
                                      'prediction", color: "#915a07" },{ label: "Write queries prediction", ' \
                                      'color: "#573854" } ];\n '
            if 'var series_arr = [ { label: "Prepare/Parse' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "Prepare/Parse", color: "#6e9dc9" },{ label: ' \
                                      '"Execute/Bind", color: "#f4ab3a" },{ label: "Bind vs prepare", ' \
                                      'color: "#ac7fa8" },{ label: "Prepare/Parse prediction", color: "#2a5073" },' \
                                      '{ label: "Execute/Bind prediction", color: "#915a07" },{ label: "Bind vs ' \
                                      'prepare prediction", color: "#573854" } ];\n '
            if 'var series_arr = [ { label: "Write buffers' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "Write buffers", color: "#6e9dc9" },{ label: ' \
                                      '"Write buffers prediction", color: "#2a5073" } ];\n '
            if 'var series_arr = [ { label: "Added' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "Added", color: "#6e9dc9" },{ label: "Removed", ' \
                                      'color: "#f4ab3a" },{ label: "Recycled", color: "#ac7fa8" },{ label: "Added ' \
                                      'prediction", color: "#2a5073" },{ label: "Removed prediction", ' \
                                      'color: "#915a07" },{ label: "Recycled prediction", color: "#573854" } ];\n '
            if 'var series_arr = [ { label: "distance' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "distance", color: "#6e9dc9" },{ label: ' \
                                      '"estimate", color: "#f4ab3a" },{ label: "distance prediction", ' \
                                      'color: "#2a5073" },{ label: "estimate prediction", color: "#915a07" } ];\n '
            if 'var series_arr = [ { label: "Size of files' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "Size of files", color: "#6e9dc9" },{ label: "Size ' \
                                      'of files prediction", color: "#2a5073" } ];\n '
            if 'var series_arr = [ { label: "Number of files' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "Number of files", color: "#6e9dc9" },{ label: ' \
                                      '"Number of files prediction", color: "#2a5073" } ];\n '
            if 'var series_arr = [ { label: "VACUUMs' in self.new_content[i]:
                self.new_content[i] = 'var series_arr = [ { label: "VACUUMs", color: "#6e9dc9" },{ label: "ANALYZEs", ' \
                                      'color: "#f4ab3a" },{ label: "VACUUMs prediction", color: "#2a5073" },' \
                                      '{ label: "ANALYZEs prediction", color: "#915a07" } ];\n '

    def __rewrite_charts(self):
        for i in range(len(self.new_content)):
            if 'charts.push([' in self.new_content[i] and 'queriespersecond_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'queriespersecond_graph\', \'Queries per second (' \
                                      '5 minutes average)\', \'Queries per second\', series_arr, ' \
                                      '[queriespersecond_graph_1_d1,queriespersecond_graph_1_d2,' \
                                      'queriespersecond_graph_1_d3,queriespersecond_predict_graph_1_d1,' \
                                      'queriespersecond_predict_graph_1_d2,queriespersecond_predict_graph_1_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'selectqueries_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'selectqueries_graph\', \'SELECT queries (5 ' \
                                      'minutes period)\', \'Queries per second\', series_arr, ' \
                                      '[selectqueries_graph_4_d1,selectqueries_graph_4_d2,selectqueries_graph_4_d3,' \
                                      'selectqueries_predict_graph_4_d1,selectqueries_predict_graph_4_d2,' \
                                      'selectqueries_predict_graph_4_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'writequeries_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'writequeries_graph\', \'Write queries (5 minutes ' \
                                      'period)\', \'Queries\', series_arr, [writequeries_graph_5_d1,' \
                                      'writequeries_graph_5_d2,writequeries_graph_5_d3,' \
                                      'writequeries_predict_graph_5_d1,writequeries_predict_graph_5_d2,' \
                                      'writequeries_predict_graph_5_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'durationqueries_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push(\'linegraph\', \'durationqueries_graph\', \'Average queries ' \
                                      'duration (5 minutes average)\', \'Duration\', series_arr, ' \
                                      '[durationqueries_graph_6_d1,durationqueries_graph_6_d2,' \
                                      'durationqueries_graph_6_d3,durationqueries_predict_graph_6_d1,' \
                                      'durationqueries_predict_graph_6_d2,durationqueries_predict_graph_6_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'bindpreparequeries_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'bindpreparequeries_graph\', \'Bind versus ' \
                                      'prepare statements (5 minutes average)\', \'Number of statements\', ' \
                                      'series_arr, [bindpreparequeries_graph_7_d1,bindpreparequeries_graph_7_d2,' \
                                      'bindpreparequeries_graph_7_d3,bindpreparequeries_predict_graph_7_d1,' \
                                      'bindpreparequeries_predict_graph_7_d2,' \
                                      'bindpreparequeries_predict_graph_7_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'connectionspersecond_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'connectionspersecond_graph\', \'Connections per ' \
                                      'second (5 minutes average)\', \'Connections per second\', series_arr, ' \
                                      '[connectionspersecond_graph_2_d1,connectionspersecond_graph_2_d2,' \
                                      'connectionspersecond_graph_2_d3,connectionspersecond_predict_graph_2_d1,' \
                                      'connectionspersecond_predict_graph_2_d2,' \
                                      'connectionspersecond_predict_graph_2_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'sessionspersecond_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'sessionspersecond_graph\', \'Number of ' \
                                      'sessions/second (5 minutes average)\', \'Sessions\', series_arr, ' \
                                      '[sessionspersecond_graph_3_d1,sessionspersecond_graph_3_d2,' \
                                      'sessionspersecond_graph_3_d3,sessionspersecond_predict_graph_3_d1,' \
                                      'sessionspersecond_predict_graph_3_d2,sessionspersecond_predict_graph_3_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'checkpointwritebuffers_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'checkpointwritebuffers_graph\', \'Checkpoint ' \
                                      'write buffers (5 minutes period)\', \'Buffers\', series_arr, ' \
                                      '[checkpointwritebuffers_graph_16_d1,' \
                                      'checkpointwritebuffers_predict_graph_16_d1]]);\n '
            if 'charts.push([' in self.new_content[i] and 'checkpointfiles_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'checkpointfiles_graph\', \'Checkpoint Wal files ' \
                                      'usage (5 minutes period)\', \'Number of files\', series_arr, ' \
                                      '[checkpointfiles_graph_17_d1,checkpointfiles_graph_17_d2,' \
                                      'checkpointfiles_graph_17_d3,checkpointfiles_predict_graph_17_d1,' \
                                      'checkpointfiles_predict_graph_17_d2,checkpointfiles_predict_graph_17_d3]]);\n '
            if 'charts.push([' in self.new_content[i] and 'checkpointdistance_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'checkpointdistance_graph\', \'Checkpoint mean ' \
                                      'distance and estimate (5 minutes period)\', \'Number of bytes\', series_arr, ' \
                                      '[checkpointdistance_graph_18_d1,checkpointdistance_graph_18_d2,' \
                                      'checkpointdistance_predict_graph_18_d1,' \
                                      'checkpointdistance_predict_graph_18_d2]]);\n '
            if 'charts.push([' in self.new_content[i] and 'temporarydata_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'temporarydata_graph\', \'Size of temporary files ' \
                                      '(5 minutes period)\', \'Size of files\', series_arr, ' \
                                      '[temporarydata_graph_17_d1,temporarydata_predict_graph_17_d1]]);\n '
            if 'charts.push([' in self.new_content[i] and 'temporaryfile_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'temporaryfile_graph\', \'Number of temporary ' \
                                      'files (5 minutes period)\', \'Number of files\', series_arr, ' \
                                      '[temporaryfile_graph_18_d1,temporaryfile_predict_graph_18_d1]]);\n '
            if 'charts.push([' in self.new_content[i] and 'autovacuum_graph' in self.new_content[i]:
                self.new_content[i] = 'charts.push([\'linegraph\', \'autovacuum_graph\', \'Autovacuum actions (5 ' \
                                      'minutes period)\', \'\', series_arr, [autovacuum_graph_22_d1,' \
                                      'autovacuum_graph_22_d2,autovacuum_predict_graph_22_d1,' \
                                      'autovacuum_predict_graph_22_d2]]);\n '

    def rebuild(self):
        self.__add_new_arrays()
        self.__rewrite_legends()
        self.__rewrite_charts()
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.writelines(self.new_content)
