# Implementing the SRA16 instruction materials

The materials here exist to test the implemention of the `SRA16` instruction.

The "sra16_test" is binary that runs the `SRA16` instruction. The "sra16_test.py" script is a gem5 script that runs the "sra16_test" binary in gem5. It was fail if the instruction has not been implemented correctly.

The source for the "sra16_test" binary is also provided in the "src" directory. It was compiled via the "Makefile" which an be run with `make`.

## The completed solution

The "sra16_impl.patch" file desfines a patch  implementing the `SRA16` instruction into gem5. The patch can be applied to the gem5 source code by running the following commands:

```sh
# Move the patch to the gem5 source code directory.
cp sra16_impl.patch /path/to/gem5

# Apply the patch
cd /path/to/gem5
git am sra16_impl.patch

# Build gem5
scons build/ALL/gem5.opt -j`nproc`
```

We strongly advise you to try to implement the instruction yourself before looking at the completed materials.
