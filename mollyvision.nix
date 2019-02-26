{ pythonPackages, pkgs, stdenv }:

let
  usedPythonPackages = (with pythonPackages; [
    numpy opencv3
  ]);
in pythonPackages.buildPythonPackage rec {
  pname = "pren1-hs18";
  version = "0.0.1";

  src = ./.;

  doCheck = false;

  propagatedbuildInputs = (with pkgs; [ opencv3 ])
                       ++ usedPythonPackages;
  pythonPath = usedPythonPackages;
}
