@echo off
START python "c:/Users/rieri/OneDrive/Documentos/Trabson-hitalo/coordenador.py"
FOR /L %%i IN (1, 1, 4) DO (
    START python "c:/Users/rieri/OneDrive/Documentos/Trabson-hitalo/client.py"
)
START python "c:/Users/rieri/OneDrive/Documentos/Trabson-hitalo/teste.py"
