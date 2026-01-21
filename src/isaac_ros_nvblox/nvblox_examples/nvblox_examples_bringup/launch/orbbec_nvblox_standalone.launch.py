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

from nvblox_ros_python_utils.nvblox_launch_utils import NvbloxMode, NvbloxCamera, NvbloxPeopleSegmentation
from nvblox_ros_python_utils.nvblox_constants import SEMSEGNET_INPUT_IMAGE_WIDTH, \
    SEMSEGNET_INPUT_IMAGE_HEIGHT, NVBLOX_CONTAINER_NAME


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg(
        'rosbag', 'None', description='Path to rosbag (running on sensor if not set).', cli=True)
    args.add_arg('rosbag_args', '', description='Additional args for ros2 bag play.', cli=True)
    args.add_arg('log_level', 'info', choices=['debug', 'info', 'warn'], cli=True)
    args.add_arg(
        'mode',
        default=NvbloxMode.static,
        choices=NvbloxMode.names(),
        description='The nvblox mode.',
        cli=True)
    args.add_arg(
        'people_segmentation',
        default=NvbloxPeopleSegmentation.peoplesemsegnet_vanilla,
        choices=[
            str(NvbloxPeopleSegmentation.peoplesemsegnet_vanilla),
            str(NvbloxPeopleSegmentation.peoplesemsegnet_shuffleseg)
        ],
        description='The model type of PeopleSemSegNet (only used when mode:=people).',
        cli=True)
    args.add_arg('launch_camera', 'False', description='Whether to launch Orbbec camera driver (set to False if camera runs on host)')
    
    actions = args.get_launch_actions()

    # Globally set use_sim_time if we're running from bag or sim
    actions.append(
        SetParameter('use_sim_time', True, condition=IfCondition(lu.is_valid(args.rosbag))))

    # 跳过 Orbbec Camera 启动，因为相机在宿主机运行
    # 如果需要在容器中启动相机，取消注释下面的代码
    # actions.append(
    #     lu.include(
    #         'orbbec_camera',
    #         'launch/astra.launch.py',
    #         condition=IfCondition(args.launch_camera)
    #     ))

    # Visual SLAM
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/perception/vslam.launch.py',
            launch_arguments={
                'container_name': NVBLOX_CONTAINER_NAME,
                'camera': NvbloxCamera.realsense,  # 使用 realsense 作为基础
            },
            delay=1.0,
            ))

    # People segmentation
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/perception/segmentation.launch.py',
            launch_arguments={
                'container_name': NVBLOX_CONTAINER_NAME,
                'people_segmentation': args.people_segmentation,
                'input_topic': '/camera/color/image_raw',
                'input_camera_info_topic': '/camera/color/camera_info',
            },
            condition=IfCondition(lu.has_substring(args.mode, NvbloxMode.people))))

    # Nvblox node with custom Orbbec remappings
    mode = NvbloxMode[args.mode]
    
    # 自定义 Orbbec 话题映射
    orbbec_remappings = [
        ('camera_0/depth/image', '/camera/depth/image_raw'),
        ('camera_0/depth/camera_info', '/camera/depth/camera_info'),
        ('camera_0/color/image', '/camera/color/image_raw'),
        ('camera_0/color/camera_info', '/camera/color/camera_info'),
    ]
    
    if mode is NvbloxMode.people:
        orbbec_remappings.extend([
            ('mask/image', '/unet/raw_segmentation_mask'),
            ('mask/camera_info', '/segmentation/camera_info_resized'),
            ('camera_0/color/image', '/segmentation/image_resized'),
            ('camera_0/color/camera_info', '/segmentation/camera_info_resized'),
        ])

    # Nvblox configuration
    base_config = lu.get_path('nvblox_examples_bringup', 'config/nvblox/nvblox_base.yaml')
    realsense_config = lu.get_path('nvblox_examples_bringup',
                                   'config/nvblox/specializations/nvblox_realsense.yaml')
    
    parameters = [base_config, realsense_config, {'num_cameras': 1}]
    
    if mode is NvbloxMode.people:
        segmentation_config = lu.get_path('nvblox_examples_bringup',
                                          'config/nvblox/specializations/nvblox_segmentation.yaml')
        parameters.append(segmentation_config)
    elif mode is NvbloxMode.dynamic:
        dynamics_config = lu.get_path('nvblox_examples_bringup',
                                      'config/nvblox/specializations/nvblox_dynamics.yaml')
        parameters.append(dynamics_config)

    # Nvblox node
    nvblox_node_name = 'nvblox_human_node' if mode is NvbloxMode.people else 'nvblox_node'
    nvblox_plugin_name = 'nvblox::NvbloxHumanNode' if mode is NvbloxMode.people else 'nvblox::NvbloxNode'

    nvblox_node = ComposableNode(
        name=nvblox_node_name,
        package='nvblox_ros',
        plugin=nvblox_plugin_name,
        remappings=orbbec_remappings,
        parameters=parameters,
    )

    actions.append(lu.load_composable_nodes(NVBLOX_CONTAINER_NAME, [nvblox_node]))

    # Play ros2bag
    actions.append(
        lu.play_rosbag(
            bag_path=args.rosbag,
            additional_bag_play_args=args.rosbag_args,
            condition=IfCondition(lu.is_valid(args.rosbag))))

    # Visualization - 手动启动 RViz
    rviz_config_path = lu.get_path('nvblox_examples_bringup',
                                   'config/visualization/orbbec_example.rviz')
    actions.append(
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", str(rviz_config_path)],
            output="screen"))

    # Container
    actions.append(lu.component_container(NVBLOX_CONTAINER_NAME, log_level=args.log_level))

    return LaunchDescription(actions)