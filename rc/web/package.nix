{
  lib,
  stdenvNoCC,
  nodejs,
  pnpm,
  pnpmConfigHook,
  fetchPnpmDeps,
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
    pnpmConfigHook
    pnpm
  ];

  pnpmDeps = fetchPnpmDeps {
    inherit (finalAttrs) pname version src;
    inherit pnpm;
    fetcherVersion = 5;
    hash = "sha256-ogaABbVzpH8qmBihhEFRpZV16IpXVW9Ek+1eo3tuuso=";
  };

  installPhase = ''
    runHook preInstall
    pnpm build --outDir $out --emptyOutDir
    runHook postInstall
  '';
})
