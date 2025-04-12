{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
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
        };
      }
    );
}
