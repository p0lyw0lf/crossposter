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
            ])
            ++ (with pkgs.python311Packages; [
              pip
              venvShellHook
              # Needed for binaries that link against libc
              ujson
            ])
            ++ (with pkgs.nodePackages; [
              pnpm
            ]);
        };
      }
    );
}
