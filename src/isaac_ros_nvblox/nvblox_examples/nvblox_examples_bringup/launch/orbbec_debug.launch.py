# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from isaac_ros_launch_utils.all_types import *
import isaac_ros_launch_utils as lu

from nvblox_ros_python_utils.nvblox_launch_utils import NvbloxMode, NvbloxCamera
from nvblox_ros_python_utils.nvblox_constants import NVBLOX_CONTAINER_NAME


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg('log_level', 'debug', choices=['debug', 'info', 'warn'], cli=True)
    
    actions = args.get_launch_actions()

    # 发布坐标系变换
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/orbbec_transforms.launch.py'))

    # 只启动 nvblox，不启动 VSLAM（简化调试）
    # 直接创建 nvblox 节点，使用明确的话题映射
    nvblox_remappings = [
        ('camera_0/depth/image', '/camera/depth/image_raw'),
        ('camera_0/depth/camera_info', '/camera/depth/camera_info'),
        ('camera_0/color/image', '/camera/color/image_raw'),
        ('camera_0/color/camera_info', '/camera/color/camera_info'),
    ]

    base_config = lu.get_path('nvblox_examples_bringup', 'config/nvblox/nvblox_base.yaml')
    realsense_config = lu.get_path('nvblox_examples_bringup',
                                   'config/nvblox/specializations/nvblox_realsense.yaml')

    nvblox_node = ComposableNode(
        name='nvblox_node',
        package='nvblox_ros',
        plugin='nvblox::NvbloxNode',
        remappings=nvblox_remappings,
        parameters=[
            base_config,
            realsense_config,
            {'num_cameras': 1},
            {'use_lidar': False},
        ],
    )

    actions.append(lu.load_composable_nodes(NVBLOX_CONTAINER_NAME, [nvblox_node]))

    # 启动 RViz
    rviz_config_path = lu.get_path('nvblox_examples_bringup',
                                   'config/visualization/orbbec_example.rviz')
    actions.append(
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", str(rviz_config_path)],
            output="screen"))

    # 添加一些调试节点
    actions.append(
        Node(
            package='rqt_topic',
            executable='rqt_topic',
            name='topic_monitor',
            output='screen'
        ))

    # Container
    actions.append(lu.component_container(NVBLOX_CONTAINER_NAME, log_level=args.log_level))

    return LaunchDescription(actions)