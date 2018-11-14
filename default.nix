{ pkgs ? import <nixpkgs> { }, stdenv ? pkgs.stdenv }:


let
  pythonPackages = pkgs.python35Packages;
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
      ( ps: with ps;
        [
          (toPythonModule opencv3)
          pytest
          numpy
        ]
      )
    )
    opencv3
    pkgs.rsync
  ];
}
