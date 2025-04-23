{ pkgs }:
pkgs.mkShell {
  venvDir = ".venv";
  packages =
    (with pkgs; [
      awscli2
      nodejs
      python311
      rclone

      pyright
    ])
    ++ (with pkgs.python311Packages; [
      pip
      venvShellHook
      # Needed so to replace the default pyarrow binaries
      pyarrow
      # Needed for other binaries that link against libc
      ujson

      # For pyright language server
      autopep8
    ])
    ++ (with pkgs.nodePackages; [
      pnpm
    ]);
}
