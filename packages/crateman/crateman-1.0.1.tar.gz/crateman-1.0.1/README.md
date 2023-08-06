## Crateman - Crate Manager.

Is a high level build system focused solely on resolving build dependencies between projects.
In other words, it's like a package manager, but for developers.

## Features
- Simple, TOML-based configuration files support
- Builds dependencies by executing arbitrary shell commands, making it universal across programming languages.
- Finds critical mistakes in dependency graph: circular dependencies, version requirements, e.t.c.
- Every major piece of functionality (such as config parsing, dependency resolving or building) can be used as separate Python module.
- Does builds in parallel whenever possible.

## History

When I was getting into Rust programming, I quickly realised that I am in huge need for a build dependency-only system. Cargo wasn't satisfying for me at all: it is a build-system - package manager - downloader - publisher at the same time, which is weird. It also hadn't needed features for my case (building dependencies only, or executing arbitrary scripts).

Then I tried building Rust project with a Makefile. It was pretty convenient for one freestanding project, very universal, but dependency management was clunky, I would find myself writing a lot of repetitiveness to make my project depend on other.

Then I tried searching for a build system focused only on dependencies. Didn't find one, and decided to implement one myself. Thus, crateman was born. And that's why it's called 'crateman', because Rust calls its packages crates.

Luckily, crateman is not Rust-only. It is universal! It can be used with any language, and any project due to ability to execute arbitrary shell commands.
