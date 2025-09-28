{
  lib,
  buildPythonPackage,

  # Build system
  hatchling,

  # Third-party dependencies
  aiofiles,
  boto3,
  mistletoe,
  pyarrow,
  pyjwt,
  sanic,
  sanic-ext,
  tzdata,

  # First-party dependencies
  crossposter-lib,

  # Runtime dependencies
  awscli2,
  bashNonInteractive,
  gzip,
}:
let
  fs = lib.fileset;
  sourceFiles = fs.unions [
    ./pyproject.toml
    (fs.fileFilter (file: file.hasExt "py" || file.hasExt "sh") ./src/rc)
    ./src/rc/templates
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

  dependencies = [
    aiofiles
    boto3
    crossposter-lib
    mistletoe
    pyarrow
    pyjwt
    sanic
    sanic-ext
    tzdata
  ];

  buildInputs = [
    awscli2
    bashNonInteractive
    gzip
  ];

  postInstall = ''
    substituteInPlace $out/lib/python3*/site-packages/rc/sync_logs.py \
      --replace-fail "aws" "${awscli2}/bin/aws"

    substituteInPlace $out/lib/python3*/site-packages/rc/folder_to_tsv.sh \
      --replace-fail "zcat" "${gzip}/bin/zcat"
  '';
}
