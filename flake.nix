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
        python3 = pkgs.python3.override {
          packageOverrides = final: prev: {
            bot-crossposter-lib = final.callPackage ./bot/package-lib.nix { };
            crossposter-lib = final.callPackage ./poster/package.nix { };
            rc-crossposter-lib = final.callPackage ./rc/package-lib.nix { };

            # Necessary until 410691 makes it to nixos-unstable https://nixpk.gs/pr-tracker.html?pr=410691
            sanic-ext = final.callPackage ./vendored/sanic-ext.nix { };

            # Neccessary until 409599 makes it to nixos-unstable https://nixpk.gs/pr-tracker.html?pr=409599
            tracerite = prev.tracerite.overrideAttrs {
              propagatedBuildInputs = with final; [
                html5tagger
                setuptools
              ];
            };
          };
        };

        bot-crossposter = pkgs.callPackage ./bot/package-bin.nix {
          python3-bot-crossposter-env = python3.withPackages (ps: [
            ps.bot-crossposter-lib
          ]);
        };
        rc-crossposter = pkgs.callPackage ./rc/package-bin.nix {
          python3-rc-crossposter-env = python3.withPackages (ps: [ ps.rc-crossposter-lib ]);
        };
      in
      {
        packages = { inherit python3 bot-crossposter rc-crossposter; };
        devShells.default = (import ./shell.nix) { inherit pkgs; };
      }
    );
}
