# Third-Party Notices

This document records third-party software dependencies, external data
considerations, and licensing boundaries relevant to the Brain Model
(BM-2026) repository.

## Software dependencies

The Brain Model software depends on third-party Python packages. None
of them is redistributed in this repository; they are installed from
their own distribution channels.

| Package | Used by | License |
|—|—|—|
| NumPy | runner, tests, CI contract | BSD-3-Clause |
| pandas | runner, tests, CI contract | BSD-3-Clause |
| SciPy | runner, tests, CI contract | BSD-3-Clause |
| pytest | tests, CI contract | MIT |
| MNE-Python | external BM-A004 operator (full G2 runs only; not in this repository) | BSD-3-Clause |
| requests | external BM-A004 operator (full G2 runs only; not in this repository) | Apache-2.0 |

Pinned versions are listed in `requirements.txt` and `requirements-ci.txt`;
the R3 runtime pins `mne==1.11.0` and `requests==2.32.5` belong to the
frozen BM-A011 R3 package.

These packages are separate works and remain subject to their respective
licenses and copyright notices.

The Apache License 2.0 applied to Brain Model software does not replace,
modify, or supersede the licenses of third-party dependencies.

Users and redistributors are responsible for complying with the
applicable licenses of third-party software.

## External datasets and raw data

External datasets, raw neurophysiological recordings, and other
third-party data are not licensed by the Brain Model repository.

Their inclusion by reference, identifier, provenance record, hash,
manifest, analysis configuration, or derived scientific description
does not transfer ownership and does not relicense the underlying data.

Users must obtain external datasets from their authorized sources and
comply with the original dataset licenses, data-use agreements,
ethical restrictions, access conditions, and attribution requirements.

### Sleep-EDF Database Expanded

The analyses in this project use the sleep-telemetry (ST) recordings of
the **Sleep-EDF Database Expanded, version 1.0.0**, distributed by
PhysioNet at <https://physionet.org/content/sleep-edfx/1.0.0/>.

- License: Open Data Commons Attribution License v1.0 (ODC-By 1.0).
- Raw EDF files are not redistributed by this repository.
- Any derived data shared from this project must carry the notice:
  „Contains information from Sleep-EDF Database Expanded which is made
  available under the ODC Attribution License.”
- Required citations:
  - Kemp B. Sleep-EDF Database Expanded (version 1.0.0). PhysioNet.
    https://doi.org/10.13026/C2X676
  - Kemp B, Zwinderman AH, Tuk B, Kamphuisen HAC, OberyÃ© JJL. Analysis
    of a sleep-dependent neuronal feedback loop: the slow-wave
    microcontinuity of the EEG. IEEE Trans Biomed Eng.
    2000;47(9):1185â1194. https://doi.org/10.1109/10.867928
  - Goldberger AL, Amaral LAN, Glass L, et al. PhysioBank,
    PhysioToolkit, and PhysioNet: components of a new research resource
    for complex physiologic signals. Circulation.
    2000;101(23):e215âe220. https://doi.org/10.1161/01.CIR.101.23.e215

## Historical and provenance artifacts

The repository may retain historical, superseded, archival, or
provenance artifacts for reproducibility, verification, and scientific
audit.

Presence of an artifact in the repository does not by itself establish
that the artifact is licensed under the repositoryâs Apache License 2.0
or CC BY 4.0 licensing scheme.

Where an artifact contains or incorporates third-party material, the
original copyright and licensing terms continue to apply.

## Scientific documentation

Original Brain Model documentation, methodological descriptions, and
scientific text identified by the repository as project documentation
are licensed under the Creative Commons Attribution 4.0 International
License (CC BY 4.0), except where otherwise stated. The scope of this
licence is defined in `docs/LICENSE-DOCS.md`.

This licensing statement does not apply to third-party quotations,
figures, datasets, software, or other incorporated materials for which
the project does not hold the necessary rights.

## No relicensing of third-party material

Nothing in this repository should be interpreted as relicensing
third-party software, datasets, publications, figures, documentation,
or other externally sourced material.

When a conflict exists between a repository-level licensing statement
and a specific third-party license or notice, the applicable
third-party terms govern that material.

## Scientific status

Licensing and repository-publication operations are administrative and
repository-governance actions.

They do not modify the frozen scientific status of the Brain Model
project and do not constitute execution or validation of any pending
scientific analysis.

Current scientific status remains:

`FULL_G2_NOT_RUN / G1_UNCHANGED`