{
  stdenvNoCC,
  python3-bot-crossposter-env,
}:
stdenvNoCC.mkDerivation {
  pname = "bot-crossposter-bin";
  version = "0.1.0";

  buildInputs = [
    python3-bot-crossposter-env
  ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin

    cat <<EOF > $out/bin/bot-crossposter
    #!/usr/bin/env bash
    python3 -m bot
    EOF
    chmod +x $out/bin/bot-crossposter

    runHook postInstall
  '';

  meta = {
    mainProgram = "bot-crossposter";
  };
}
