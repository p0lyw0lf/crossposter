{
  lib,
  stdenvNoCC,
  python3-bot-crossposter-env,
}:
let
  fs = lib.fileset;
in
stdenvNoCC.mkDerivation {
  pname = "bot-crossposter-bin";
  version = "0.1.0";

  buildInputs = [
    python3-bot-crossposter-env
  ];

  src = fs.toSource {
    root = ./.;
    fileset = fs.unions [ ./bin/bot-crossposter ];
  };

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    cp ./bin/bot-crossposter $out/bin/bot-crossposter

    runHook postInstall
  '';

  fixupPhase = ''
    runHook preFixup

    substituteInPlace $out/bin/bot-crossposter \
      --replace python3 "${python3-bot-crossposter-env}/bin/python3"

    runHook postFixup
  '';

  meta = {
    mainProgram = "bot-crossposter";
  };
}
