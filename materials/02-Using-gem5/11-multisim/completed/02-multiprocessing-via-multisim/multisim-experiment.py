# Copyright (c) 2024 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This script is the "01-multiprocessing-via-multisim.py" script converted to
use the MultiSim module.
"""

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

import gem5.utils.multisim as multisim

multisim.set_num_processes(2)

for data_cache_size in ["5kB","10KB"]:
    for instruction_cache_size in ["5kB","10kB"]:

        cache_hierarchy = PrivateL1CacheHierarchy(
            l1d_size=data_cache_size,
            l1i_size=instruction_cache_size,
        )

        memory = SingleChannelDDR3_1600(size="32MB")

        processor = SimpleProcessor(
            cpu_type=CPUTypes.TIMING,
            isa=ISA.X86,
            num_cores=1
        )

        board = SimpleBoard(
            clk_freq="3GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

        board.set_se_binary_workload(
            obtain_resource("x86-matrix-multiply")
        )

        # The key difference: The simulator is object is passed to the
        # MultiSim module via the `add_simulator` function.
        #
        # The `run` function is not called here. Instead it is involved in
        # MultiSim module's execution.
        multisim.add_simulator(
            Simulator(
                board=board,
                # The `id` parameter is used to identify the simulation.
                # Setting this is strongly encouraged.
                # Each output directory will be named after the `id` parameter.
                id=f"process_{data_cache_size}_{instruction_cache_size}"
            )
        )

