{ pkgs }:
pkgs.mkShell {
  packages =
    (with pkgs; [
      awscli2
      nodejs
      python311
      rclone

      # The python environments themselves are managed with hatch
      hatch
      pyright
    ])
    ++ (with pkgs.python311Packages; [
      # For pyright language server
      autopep8
      # For building packages
      build
    ])
    ++ (with pkgs.nodePackages; [
      pnpm
    ]);

  shellHook = ''
    export SASS_EMBEDDED_BIN_PATH="${pkgs.dart-sass}/bin/sass";
  '';
}
