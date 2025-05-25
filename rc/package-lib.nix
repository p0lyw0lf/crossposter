{
  lib,
  buildPythonPackage,

  # Build system
  hatchling,

  # Third-party dependencies
  aiofiles,
  boto3,
  pyarrow,
  pyjwt,
  sanic,
  sanic-ext,
  tzdata,

  # First-party dependencies
  crossposter-lib,
}:
let
  fs = lib.fileset;
  sourceFiles = fs.unions [
    ./pyproject.toml
    (fs.fileFilter (file: file.hasExt "py") ./src/rc)
  ];
in
buildPythonPackage {
  pname = "rc-crossposter-lib";
  version = "0.1.1";
  pyproject = true;

  src = fs.toSource {
    root = ./.;
    fileset = sourceFiles;
  };

  build-system = [ hatchling ];

  propagatedBuildInputs = [
    aiofiles
    boto3
    crossposter-lib
    pyarrow
    pyjwt
    sanic
    sanic-ext
    tzdata
  ];
}
