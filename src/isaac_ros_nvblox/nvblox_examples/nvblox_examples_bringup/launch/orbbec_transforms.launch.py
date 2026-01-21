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


def generate_launch_description() -> LaunchDescription:
    actions = []

    # 发布静态变换：odom -> base_link
    actions.append(
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='odom_to_base_link',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link'],
            output='screen'
        ))

    # 发布静态变换：base_link -> camera_link
    actions.append(
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_camera_link',
            arguments=['0.1', '0', '0.2', '0', '0', '0', 'base_link', 'camera_link'],
            output='screen'
        ))

    # 关键修复：发布 camera_link -> camera_color_optical_frame 的变换
    # 这是 Orbbec 相机实际使用的坐标系
    actions.append(
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='camera_link_to_color_optical',
            arguments=['0', '0', '0', '-1.5708', '0', '-1.5708', 'camera_link', 'camera_color_optical_frame'],
            output='screen'
        ))

    # 由于 Orbbec 相机的深度和彩色都使用 camera_color_optical_frame，
    # 我们需要创建一个到 camera_depth_optical_frame 的变换（如果需要的话）
    actions.append(
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='color_to_depth_optical',
            arguments=['0', '0', '0', '0', '0', '0', 'camera_color_optical_frame', 'camera_depth_optical_frame'],
            output='screen'
        ))

    return LaunchDescription(actions)