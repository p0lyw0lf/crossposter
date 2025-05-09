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
        python3-crossposter-pkgs = pkgs.python3.override {
          packageOverrides = final: prev: {
            bot-crossposter-lib = final.callPackage (import ./bot/package-lib.nix) {
              crossposter-lib = final.crossposter-lib;
            };
            crossposter-lib = final.callPackage (import ./poster/package.nix) { };
            rc-crossposter-lib = final.callPackage (import ./rc/package-lib.nix) {
              crossposter-lib = final.crossposter-lib;
            };
          };
        };
        python3-bot-crossposter-env = python3-crossposter-pkgs.withPackages (ps: [
          ps.bot-crossposter-lib
        ]);
        python3-rc-crossposter-env = python3-crossposter-pkgs.withPackages (ps: [ ps.rc-crossposter-lib ]);

        bot-crossposter-bin = pkgs.callPackage (import ./bot/package-bin.nix) {
          inherit python3-bot-crossposter-env;
        };
        rc-crossposter-bin = pkgs.callPackage (import ./rc/package-bin.nix) {
          inherit python3-rc-crossposter-env;
        };
      in
      {
        packages.bot-crossposter = bot-crossposter-bin;
        packages.rc-crossposter = rc-crossposter-bin;
        devShells.default = (import ./shell.nix) { inherit pkgs; };
      }
    );
}
