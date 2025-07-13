{
  stdenvNoCC,
  python3-rc-crossposter-env,
  rc-crossposter-static,
}:
stdenvNoCC.mkDerivation {
  pname = "rc-crossposter-bin";
  version = "0.1.1";

  buildInputs = [
    python3-rc-crossposter-env
    rc-crossposter-static
  ];

  src = ./bin;
  dontUnpack = true;

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    cat <<EOF > $out/bin/rc-crossposter
    #!/usr/bin/env bash
    export RC_WEB_FILES="''${RC_WEB_FILES:-${rc-crossposter-static}}"
    "${python3-rc-crossposter-env}/bin/sanic" rc "\$@"
    EOF
    chmod +x $out/bin/rc-crossposter

    runHook postInstall
  '';

  meta = {
    mainProgram = "rc-crossposter";
  };
}
