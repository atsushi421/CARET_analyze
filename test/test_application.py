# Copyright 2021 Research Institute of Systems Planning, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from caret_analyze.application import Application
from caret_analyze.trace.lttng import Lttng

import pytest


class TestApplication:

    @pytest.mark.parametrize(
        'trace_path, yaml_path, start_cb_name, end_cb_name, paths_len',
        [
            (
                'sample/lttng_samples/talker_listener/',
                'sample/lttng_samples/talker_listener/architecture.yaml',
                '/talker/timer_callback_0',
                '/listener/subscription_callback_0',
                1,
            ),
            (  # cyclic case
                'sample/lttng_samples/cyclic_pipeline_intra_process',
                'sample/lttng_samples/cyclic_pipeline_intra_process/architecture.yaml',
                '/pipe1/subscription_callback_0',
                '/pipe1/subscription_callback_0',
                2,  # [pipe1 -> pipe2] -> pipe1 and [pipe1]
            ),
            (
                'sample/lttng_samples/end_to_end_sample/fastrtps',
                'sample/lttng_samples/end_to_end_sample/architecture.yaml',
                '/sensor_dummy_node/timer_callback_0',
                '/actuator_dummy_node/subscription_callback_0',
                0,
            ),
            (  # publisher callback_name and callback depencency added
                'sample/lttng_samples/end_to_end_sample/fastrtps',
                'sample/lttng_samples/end_to_end_sample/architecture_modified.yaml',
                '/sensor_dummy_node/timer_callback_0',
                '/actuator_dummy_node/subscription_callback_0',
                1,
            ),
            (
                'sample/lttng_samples/end_to_end_sample/cyclonedds',
                'sample/lttng_samples/end_to_end_sample/architecture.yaml',
                '/sensor_dummy_node/timer_callback_0',
                '/actuator_dummy_node/subscription_callback_0',
                0,
            ),
            (  # publisher callback_name and callback depencency added
                'sample/lttng_samples/end_to_end_sample/cyclonedds',
                'sample/lttng_samples/end_to_end_sample/architecture_modified.yaml',
                '/sensor_dummy_node/timer_callback_0',
                '/actuator_dummy_node/subscription_callback_0',
                1,
            ),
        ],
    )
    def test_search_paths(self, trace_path, yaml_path, start_cb_name, end_cb_name, paths_len):
        lttng = Lttng(trace_path)
        app = Application(yaml_path, 'yaml', lttng)

        paths = app.search_paths(start_cb_name, end_cb_name)
        assert len(paths) == paths_len

        for path in paths:
            assert path[0].callback_unique_name == start_cb_name
            assert path[-1].callback_unique_name == end_cb_name

    @pytest.mark.parametrize(
        'trace_path, yaml_path, start_cb_name, end_cb_name, paths_len',
        [
            (
                'sample/lttng_samples/talker_listener/',
                'sample/lttng_samples/cyclic_pipeline_intra_process/architecture.yaml',
                '/talker/timer_callback_0',
                '/listener/subscription_callback_0',
                0,
            ),
            (
                'sample/lttng_samples/end_to_end_sample/cyclonedds',
                'sample/lttng_samples/end_to_end_sample/architecture.yaml',
                '/sensor_dummy_node/timer_callback_0',
                '/actuator_dummy_node/subscription_callback_0',
                0,
            ),
        ],
    )
    def test_architecture_miss_match(
        self,
        trace_path,
        yaml_path,
        start_cb_name,
        end_cb_name,
        paths_len
    ):
        """Test if the architecture file and measurement results do not match."""
        trace_path = 'sample/lttng_samples/talker_listener/'
        yaml_path = 'sample/lttng_samples/end_to_end_sample/architecture.yaml'
        start_cb_name = '/talker/timer_callback_0'
        end_cb_name = '/listener/subscription_callback_0'
        lttng = Lttng(trace_path)
        app = Application(yaml_path, 'yaml', lttng)

        paths = app.search_paths(start_cb_name, end_cb_name)
        assert len(paths) == paths_len

    # def test_analysis_senario(self):
    #     """
    #     test for v.0.2.0
    #     解析
    #     """

    #     lttng = Lttng('')
    #     trace_result = TraceResult(lttng)
    #     architecture_reader = ArchitectureReaderFactory.YamlFile('')
    #     architecture = Architecture(architecture_file)
    #     app = Application(architecture, trace_result)

    #     app.paths
    #     path = app.named_path['aa']
    #     executor = app.executors
    #     executor.callbacks
    #     executor.nodes

    # def test_architecture_reader(self):
    #     reader = ArchitectureReaderFactory.YamlFile('')
    #     reader.get_node_names()
    #     reader.get_timer_callbacks()
    #     reader.get_subscription_callbacks()
    #     reader.get_publishers()

    # def test_architecture_file_create_senario(self):
    #     lttng = Lttng('')
    #     trace_result = TraceResult(lttng)  # 今後トレースのペアは増える見込みがあるので、ここを抽象化する。
    #     architecture__reader = ArchitectureReaderFactory.lttng(lttng)
    #     architecture = Architecture(architecture_reader)
    #     architecture.export('')

    # def test_set_named_path(self):
    #     lttng = Lttng('')
    #     trace_result = TraceResult(lttng)  # 今後トレースのペアは増える見込みがあるので、ここを抽象化する。
    #     architecture_reader = ArchitectureReaderFactory.YamlFile('')
    #     architecture = Architecture(architecture_file)
    #     architecture = Architecture('', type='')
    #     app = Application(architecture, trace_result)
    #     paths = app.search_paths('', '')
    #     app.named_path['aa'] == paths[0]
    #     app.architecture.export('')

    # def test_analyze_executor_behavior(self):

    #     architecture_reader = ArchitectureReaderFactory.YamlFile('')
    #     architecture = Architecture(architecture_file)
    #     app = Application(architecture)

    #     synario_config = {
    #         'callback_unique_name': 10,
    #         'executor_priority': 2,
    #         'executor_core': 0
    #     }

    #     senario_analyzer = WorstCaseAnalyzer(app)
    #     trace_result = senario_analyzer.analyze(synario_config)
    #     wc_app = Application(architecture, trace_result)
    #     path = wc_app._named_path['aaa']
    #     path
