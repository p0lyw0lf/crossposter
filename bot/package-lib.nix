{
  lib,
  buildPythonPackage,

  # Build system
  hatchling,

  # Third-party dependencies
  discordpy,
  tzdata,

  # First-party dependencies
  crossposter-lib,
}:
let
  fs = lib.fileset;
  sourceFiles = fs.unions [
    ./pyproject.toml
    (fs.fileFilter (file: file.hasExt "py") ./src/bot)
  ];
in
buildPythonPackage {
  pname = "bot-crossposter-lib";
  version = "0.1.1";
  pyproject = true;

  src = fs.toSource {
    root = ./.;
    fileset = sourceFiles;
  };

  build-system = [ hatchling ];

  propagatedBuildInputs = [
    crossposter-lib
    discordpy
    tzdata
  ];
}
