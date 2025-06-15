{
  lib,
  stdenvNoCC,
  nodejs,
  pnpm,
}:
let
  fs = lib.fileset;
  sourceFiles = fs.unions [
    ./package.json
    ./pnpm-lock.yaml
    ./vite.config.ts
    ./tsconfig.json
    ./src
  ];
in
stdenvNoCC.mkDerivation (finalAttrs: {
  pname = "rc-crossposter-static";
  version = "0.0.1";

  src = fs.toSource {
    root = ./.;
    fileset = sourceFiles;
  };

  nativeBuildInputs = [
    nodejs
    pnpm.configHook
  ];

  pnpmDeps = pnpm.fetchDeps {
    inherit (finalAttrs) pname version src;
    hash = "sha256-b/ZWXZ6qhAubLl+Qb18ZTRiHGVgWpAr8Wq0jZB12uCA=";
  };

  installPhase = ''
    pnpm build --outDir $out --emptyOutDir
  '';
})
