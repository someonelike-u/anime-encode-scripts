@echo off
rem setLocal EnableDelayedExpansion

rem DELETE 'mygo_12_33687_33809.png' in 'masks_12' folder for BD version!
rem This one is just for TV version

set vspipe=D:\VapourSynth64Portable\VapourSynth64\vspipe.exe
set python=D:\VapourSynth64Portable\VapourSynth64\python.exe
set x265=D:\VapourSynth64Portable\bin\x265.exe
set params=--preset slower --rd 4 --rect --no-amp --rskip 0 --tu-intra-depth 2 --tu-inter-depth 2 --no-tskip --merange 57 --subme 5 --b-intra --weightb --no-strong-intra-smoothing --psy-rd 2.0 --psy-rdoq 2.0 --no-open-gop --no-cutree --keyint 240 --min-keyint 23 --scenecut 40 --rc-lookahead 60 --bframes 16 --aq-mode 3 --aq-strength 0.85 --cbqpoffs -2 --crqpoffs -2 --qcomp 0.75 --deblock=-2:-2 --no-sao --no-sao-non-deblock --sar 1 --range limited --colorprim 1 --transfer 1 --colormatrix 1 --output-depth 10

%python% generate_encode_scripts.py
echo.

for %%i in (*.vpy) do (
    echo [Info] Start encode: %%i
    echo.
    %vspipe% -c y4m "%%~ni.vpy" - | %x265% --y4m %params% --crf 16 --output "%%~ni.265" -
    echo.
)

del *.vpy

pause