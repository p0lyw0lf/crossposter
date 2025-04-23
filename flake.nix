{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
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
        crossposter = pkgs.callPackage (import ./poster/package.nix) { };
        bot-crossposter = pkgs.callPackage (import ./bot/package.nix) { inherit crossposter; };
      in
      {
        inherit crossposter bot-crossposter;
        devShells.default = (import ./shell.nix) { inherit pkgs; };
      }
    );
}
