# `lytemaps`

This repository contains an implementation of a minimal subset of `neuromaps` functionality. If you're an end user, this is likely not for you -- this implementation exists mostly for `hypercoil` developer purposes. As developers, we'd like to use certain `neuromaps` operations without burdening our software with the bulky dependencies (`nilearn`, `sklearn` and Connectome Workbench) that the full install of `neuromaps` requires. This implementation is intended to support the subset of functionality that requires only core Scientific Python packages together with the essential `nibabel` and `requests`. Obviously, functionality here is limited. As development progresses, we'll index the `neuromaps` functions that are implemented below.

If for some reason you still decide to use this repository, please follow the citation prescriptions from [Neuromaps](https://github.com/netneurolab/neuromaps) and [nilearn](https://github.com/nilearn/nilearn). In particular, specify that you used `lytemaps` in your methods section, specify that `lytemaps` comprises code from both `neuromaps` and `nilearn`, and cite the `neuromaps` and `nilearn` papers.

### License

Most code in this repository is taken directly from the `neuromaps` repository, and is therefore licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License. The exception to this is several functions in `src/lytemaps/utils.py` and `src/lytemaps/datasets/utils.py`, which are taken from the `nilearn` and `sklearn` repositories and are therefore licensed under the 3-clause BSD license. As we redevelop code into our own implementations, we will relicense. See the `LICENSE` file for more details.
