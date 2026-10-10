{ pkgs }:
pkgs.mkShell {
  packages = (
    with pkgs;
    [
      awscli2
      corepack
      nodejs
      (python314.withPackages (
        ps: with ps; [
          # For pyright language server
          autopep8
          # For building packages
          build
        ]
      ))
      rclone
      sops

      # The python environments themselves are managed with hatch
      hatch
      pyright
    ]
  );

  shellHook = ''
    export SASS_EMBEDDED_BIN_PATH="${pkgs.dart-sass}/bin/sass";
  '';
}
