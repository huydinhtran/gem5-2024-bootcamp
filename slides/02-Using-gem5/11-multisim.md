---
marp: true
paginate: true
theme: gem5
title: MultiSim
---

<!-- _class: title -->

## MultiSim

Multiprocessing support for gem5 simulations.

---

## The problem

The gem5 simulator is single-threaded.
This is baked into the core design and is unlikely to change due to the high cost of coverting the entire codebase.

**Therefore we cannot "speed up" your work with more cores**.

---

## The insight

The gem5 simulator is used for experimentation: to explore how variables of interest change the behavior of a system when all other variables are held constant.
Such investigations necessitates multiple runs of the simulator.

**Therefore, if not multiple a gem5 process using multiple threads, why not multiple gem5 processes each using a single thread?**

---

## People already do this...

Go to the [02-Using-gem5/11-multisim/01-multiprocessing-via-script](/materials/02-Using-gem5/11-multisim/01-multiprocessing-via-script/) directory to see a completed example of how **NOT** to run multiple gem5 processes.

### The downsides of this

1. Requires the user write the script.
    1. Increases the barrier to entry.
    2. Increases the likelihood of errors.
    3. Requires user to manage output files.
2. Non-standard (everyone does it differently).
    1. Hard to share with others.
    2. Hard to reproduce.
    3. No built-in support now or in the future.

---

## A better way

**MultiSim** is a gem5 feature that allows you to run multiple gem5 processes from a single gem5 configuration script.

This script outlines the simulations to run and the parent gem5 process creats a child for each.

### The advantages of this

1. We (the gem5 devs) handle this for you.
    1. Less barrier to entry.
    2. Less likelihood of errors.
    3. Multisim will handle the output files automatically.
Automatic handling of output files.
2. Standardized.
    1. Easy to share with others (just send the script).
    2. Easy to reproduce (just run the script).
    3. Allows for future support (orchestration, etc).

---

### Some caviates

This features is new as of version 24.0.

It is not fully mature and still lacks some support utilities which will allow for great flexibility and ease of use.
However, this short tutrorial should give you a good idea of how to use it going forward.

---

## Let's go through and example

Start by opening [02-Using-gem5/11-multisim/02-multiprocessing-via-multisim/multisim-experiment.py](/materials/02-Using-gem5/11-multisim/02-multiprocessing-va-multisim/multisim-experiment.py).

This configuration script is almost identical to the script in the previous example but with the argparse code removed and the multisim import added:

### To start:  Declare the maximum number of processors

```python
# Sets the maximum number of concurrent processes to be 2.
multisim.set_num_processes(2)
```

If this is not set the gem5 will default to consume all available threads.
We **strongly** recommend setting this value to avoid overconsuming your system's resources.

---

## Use simple Python constructs to define multiple simulations

```python
for data_cache_size in ["5kB","10KB"]:
    for instruction_cache_size in ["5kB","10kB"]:

        cache_hierarchy = PrivateL1CacheHierarchy(
            l1d_size=data_cache_size,
            l1i_size=instruction_cache_size,
        )
```

---

## Create and add the simulation to the MultiSim object

```python
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
```

---

## Execute multiple simulations

A completed example can be found at [/materials/02-Using-gem5/11-multisim/completed/02-multiprocessing-via-multisim/multisim-experiment.py](/materials/02-Using-gem5/11-multisim/completed/02-multiprocessing-via-multisim/multisim-experiment.py).

```shell
gem5 -m gem5.multisim multisim-experiment.py
```

Checkout the "m5out" directory to see the segregated output files.

---

## Execute single simulations from a multisim config

You can also execute a single simulation from a MultiSim configuration script.
To do so just pass the configuration script directly to gem5 (i.e., do not use `-m gem5.multisim multisim-experiment.py`).

To list the IDs of the simulations in a MultiSim configuration script:

```shell
gem5 {config} --list
```

To execute a single simulation, pass the ID:

```shell
gem5 {config} {id}
```
