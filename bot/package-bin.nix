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
  version = "0.1.1";

  buildInputs = [
    python3-bot-crossposter-env
  ];

  src = ./bin;
  dontUnpack = true;

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    cat <<EOF > $out/bin/bot-crossposter
    #!/usr/bin/env bash
    "${python3-bot-crossposter-env}/bin/python3" -m bot
    EOF
    chmod +x $out/bin/bot-crossposter

    runHook postInstall
  '';

  meta = {
    mainProgram = "bot-crossposter";
  };
}
