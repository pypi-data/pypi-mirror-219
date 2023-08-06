"""
Crateman - Crate manager.

This is a simple high-level build system focused solely on resolving build dependencies
of a project and building them in order.

(Why traditional "Package" word had been replaced with "Crate", refer to FAQ)

Submodules
==========
- `crate`: Crate class and methods to build a crate
- `log`: crateman logging facility
- `config`: Config class and methods to parse a crateman.toml file
- `resolver`: methods to convert one config file to the whole crate dependency tree
- `error`: various classes used by crateman to handle errors
- `cli`: entry point for `crateman` command-line utility
"""
