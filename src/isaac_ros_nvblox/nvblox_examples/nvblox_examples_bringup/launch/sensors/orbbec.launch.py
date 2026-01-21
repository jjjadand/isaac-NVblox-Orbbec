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

from nvblox_ros_python_utils.nvblox_constants import NVBLOX_CONTAINER_NAME


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg('container_name', NVBLOX_CONTAINER_NAME)
    args.add_arg('run_standalone', 'False')
    args.add_arg('camera_name', 'camera', description='Camera namespace')
    args.add_arg('launch_camera', 'False', description='Whether to launch the Orbbec camera driver')

    actions = args.get_launch_actions()

    # 只有在明确要求时才尝试启动相机
    # 由于相机在宿主机运行，默认跳过此步骤
    if args.launch_camera == 'True':
        actions.append(
            lu.include(
                'orbbec_camera',
                'launch/astra.launch.py',
                condition=IfCondition(args.launch_camera)
            ))

    return LaunchDescription(actions)