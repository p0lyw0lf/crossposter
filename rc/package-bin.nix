{
  lib,
  stdenvNoCC,
  python3-rc-crossposter-env,
}:
let
  fs = lib.fileset;
in
stdenvNoCC.mkDerivation {
  pname = "rc-crossposter-bin";
  version = "0.1.1";

  buildInputs = [
    python3-rc-crossposter-env
  ];

  src = fs.toSource {
    root = ./.;
    fileset = fs.unions [ ./bin/rc-crossposter ];
  };

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    cp ./bin/rc-crossposter $out/bin/rc-crossposter

    runHook postInstall
  '';

  fixupPhase = ''
    runHook preFixup

    substituteInPlace $out/bin/rc-crossposter \
      --replace sanic "${python3-rc-crossposter-env}/bin/sanic"

    runHook postFixup
  '';

  meta = {
    mainProgram = "rc-crossposter";
  };
}
