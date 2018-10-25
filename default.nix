{ pkgs ? import <nixpkgs> { }, stdenv ? pkgs.stdenv }:


let
  pythonPackages = pkgs.python36Packages;
  opencv3 = ( pkgs.opencv3.override {
    protobuf = pkgs.protobuf3_5;
    enableCuda = false;
    enableGtk3 = true;
    enablePython = true;
    inherit pythonPackages;
  } );
in stdenv.mkDerivation rec {
  name = "mollyvision-opencv-python-env-${version}";
  version = "0.0.1";
  propagatedBuildInputs = [
    ( pythonPackages.python.withPackages
      (ps: [ ps.virtualenv (ps.toPythonModule opencv3) ] ) )
    opencv3
  ];
}
