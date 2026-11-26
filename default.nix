{
  pkgs ? import <nixpkgs> { },
}:
{
  packages = (import ./packages.nix) { inherit pkgs; };
  devShells.default = (import ./shell.nix) { inherit pkgs; };
}
