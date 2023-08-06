# itkdb history

---

All notable changes to itkdb will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

**_Changed:_**

**_Added:_**

**_Fixed:_**

## [0.4.0](https://gitlab.cern.ch/atlas-itk/sw/db/itkdb/-/tags/v0.4.0) - 2023-03-02 ## {: #itkdb-v0.4.0 }

**_Added:_**

- This documentation website!
- Functionality to upload to EOS (`with_eos` argument to [itkdb.Client][])
- Automatic SSL verification for requests to `.cern.ch`
- `itkdb.utils`
  - [itkdb.utils.is_eos_uploadable][]
  - [itkdb.utils.is_root][]
  - [itkdb.utils.sizeof_fmt][]
- `itkdb.models`
  - [itkdb.models.BinaryFile][] as a base for all file models
  - [itkdb.models.ZipFile][] (!17)
- Configuration
  - audience, site, access scopes [`ITKDB_ACCESS_SCOPE`,
    `ITKDB_ACCESS_AUDIENCE`] (1c18ad6c2729af797eb5ea6c31c45b3517ea2db6,
    1942333f11a50e5a665d2ba00ac4e95954205733)
  - leeway [`ITKDB_LEEWAY`] (3dc7027d74f4966f26072bb75f33fc6664f39193)
- Support for python 3.11 (!19)
- `contrib` feature for rendering exceptions that return HTML (!20)
- [itkdb.data][] for data files (!15 for image/text data files and the CERN SSL
  cert chain, !24 for ROOT file)

**_Changed:_**

- Renamed `itkdb.utilities` to `itkdb.utils`
- `itkdb.models`
  - `itkdb.models.Image` to [itkdb.models.ImageFile][]
  - `itkdb.models.Text` to [itkdb.models.TextFile][]
- Improved handling of large data files by creating a temporary file on disk
  when downloading from ITkPD or EOS
- [itkdb.core.User][] arguments renamed from `accessCode1` / `accessCode2` to
  `access_code1` / `access_code2` to be more pythonic

**_Fixed:_**

- Fix `version` command when the version is dynamic and build dependencies are
  unmet
- Fixed bug in CLI for overriding base configuration settings (!14)
- Fixed bug in duplicated logging when redirects occur (!21)
