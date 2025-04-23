{
  lib,
  python3Packages,
  crossposter,
}:
let
  fs = lib.fileset;
  sourceFiles = fs.unions [
    ./pyproject.toml
    (fs.fileFilter (file: file.hasExt "py") ./src/bot)
  ];
in
python3Packages.buildPythonApplication {
  pname = "bot-crossposter";
  version = "0.1.0";
  pyproject = true;

  src = fs.toSource {
    root = ./.;
    fileset = sourceFiles;
  };

  build-system = [ python3Packages.hatchling ];

  propagatedBuildInputs =
    (with python3Packages; [
      discordpy
      tzdata
    ])
    ++ [ crossposter ];
}
