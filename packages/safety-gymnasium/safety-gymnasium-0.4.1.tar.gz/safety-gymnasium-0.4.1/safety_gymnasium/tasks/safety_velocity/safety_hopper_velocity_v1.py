# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
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
# ==============================================================================
"""Hopper environment with a safety constraint on velocity."""

from safety_gymnasium.tasks.safety_velocity.safety_hopper_velocity_v0 import (
    SafetyHopperVelocityEnv as HopperEnv,
)


class SafetyHopperVelocityEnv(HopperEnv):
    """Hopper environment with a safety constraint on velocity."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._velocity_threshold = 0.7402
