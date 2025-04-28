{
  lib,
  buildPythonPackage,

  # Build system
  hatchling,

  # Third-party dependencies
  mastodon-py,
  pyyaml,
  atproto,
  githubkit,
  jinja2,
  mistletoe,
  python-frontmatter,
  tzdata,
}:
let
  fs = lib.fileset;
  sourceFiles = fs.intersection (fs.gitTracked ./.) (
    fs.unions [
      ./pyproject.toml
      (fs.fileFilter (file: file.hasExt "py") ./src/poster)
      ./src/poster/config
      ./src/poster/secrets
      ./src/poster/templates
    ]
  );
in
buildPythonPackage {
  pname = "crossposter";
  version = "0.1.0";
  pyproject = true;

  src = fs.toSource {
    root = ./.;
    fileset = sourceFiles;
  };

  build-system = [ hatchling ];

  propagatedBuildInputs = [
    mastodon-py
    pyyaml

    atproto
    githubkit
    githubkit.optional-dependencies.auth-app
    jinja2
    mistletoe
    python-frontmatter
    tzdata
  ];
}
