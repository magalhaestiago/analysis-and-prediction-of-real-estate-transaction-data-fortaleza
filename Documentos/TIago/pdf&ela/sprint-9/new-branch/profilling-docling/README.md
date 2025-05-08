# Profiling docling

## About this code
* This script is intended to evaluate the docking steps without changing or compromising dependencies, using the profilling technique.

* When executing *main.py*, txts containing the complete profiling corresponding to the file will be generated. And when executing *analysys.py*, Jsons files will be generated with the execution times of docling steps.




### Installation

```
git clone https://github.azc.ext.hp.com/doccomp24/performance-evaluation-tools.git

cd profilling-docling

rye sync

```

### Usage

```
python main.py [directory with 1 or more pdf files]

python analysys.py txts
```