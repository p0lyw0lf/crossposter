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
        pkgs = nixpkgs.legacyPackages.${system};
        python3 = pkgs.python3.override {
          packageOverrides = final: prev: {
            bot-crossposter-lib = final.callPackage ./bot/package-lib.nix { };
            crossposter-lib = final.callPackage ./poster/package.nix { };
            rc-crossposter-lib = final.callPackage ./rc/package-lib.nix { };
          };
        };

        bot-crossposter = pkgs.callPackage ./bot/package-bin.nix {
          python3-bot-crossposter-env = python3.withPackages (ps: [
            ps.bot-crossposter-lib
          ]);
        };

        rc-crossposter-static = pkgs.callPackage ./rc/web/package.nix { };
        rc-crossposter = pkgs.callPackage ./rc/package-bin.nix {
          inherit rc-crossposter-static;
          python3-rc-crossposter-env = python3.withPackages (ps: [ ps.rc-crossposter-lib ]);
        };
      in
      {
        packages = {
          inherit
            python3
            bot-crossposter
            rc-crossposter
            ;
        };
        devShells.default = (import ./shell.nix) { inherit pkgs; };
      }
    );
}
