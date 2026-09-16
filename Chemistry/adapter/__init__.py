"""This subject declares a contract but has no adapter behind it yet.

The contract records what Chemistry results look like -- element-count maps, ledgers,
exact integer comparison -- so the engine's seam could be designed against three
subjects rather than two. Building the adapter is P6 and is owner-gated.

There is deliberately no `load()`. Subject checks read its absence as CONTRACT_ONLY
and report it, which is more honest than an adapter that imports but cannot compute.
"""
