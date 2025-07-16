{
  lib,
  buildPythonPackage,
  makeWrapper,

  # Build system
  hatchling,

  # Third-party dependencies
  atproto,
  githubkit,
  jinja2,
  mastodon-py,
  mistletoe,
  python-frontmatter,
  pyyaml,
  tzdata,

  # Runtime dependencies
  awscli2,
  bashNonInteractive,
  corepack,
  gitMinimal,
  rclone,
  sops,
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
      ./src/poster/scripts
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

  dependencies = [
    atproto
    githubkit
    githubkit.optional-dependencies.auth-app
    jinja2
    mastodon-py
    mistletoe
    python-frontmatter
    pyyaml
    tzdata
  ];

  nativeBuildInputs = [
    makeWrapper
  ];

  buildInputs = [
    awscli2
    bashNonInteractive
    corepack
    gitMinimal
    rclone
  ];

  postInstall = ''
    substituteInPlace $out/lib/python3*/site-packages/poster/secrets/__init__.py \
      --replace-fail "sops" "${sops}/bin/sops"

    for script in $out/lib/python3*/site-packages/poster/scripts/*.sh; do
      wrapProgram $script \
        --prefix PATH : ${
          lib.makeBinPath [
            awscli2
            corepack
            gitMinimal
            rclone
          ]
        }
    done
  '';
}
