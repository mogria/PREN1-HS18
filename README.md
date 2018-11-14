# PREN 1 HS18

PREN Modul HSLU - Team 1

## Struktur

## Source Code
Der 'src' Ordner enthält den Source Code für die Systemsteuerung und die Mikrocontroller
[Details/Info](src/src.md)

# Testing

The tests are in the `tests/` folder. Run pytest from the project root directory to run the tests, they should be found automagically.

    pytest


# Deployment

Run `deploy.sh` to incrementally deploy to a remote ssh host using rsync. By default this is `pi@mollyvision` and the folder `~/deployment`. Edit the variables at the top of file if you want to change this.

Run `deploy.sh complete` to delete the contents of the deployment folder first before deploying. Be careful with this, especially when reconfiguring the deployment folder/host.
