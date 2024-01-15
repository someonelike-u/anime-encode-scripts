@ECHO OFF
rem setLocal EnableDelayedExpansion

set vspipe=D:\VapourSynth64Portable_2020_09_06\VapourSynth64\vspipe.exe
set x264=D:\VapourSynth64Portable_2020_09_06\bin\x264.exe
set python="D:\VapourSynth64Portable_2020_09_06\VapourSynth64\python.exe"
set params1=--preset slower --rd 3 --no-rect --no-amp --rskip 1 --tu-intra-depth 2 --tu-inter-depth 2 --tskip --merange 32 --weightb --no-strong-intra-smoothing --psy-rd 2.0 --psy-rdoq 1 --no-open-gop --keyint 240 --min-keyint 1 --scenecut 40 --rc-lookahead 80 --bframes 8 --aq-mode 3 --aq-strength 0.8 --cbqpoffs -2 --crqpoffs -2 --qcomp 0.70 --deblock=-1:-1 --no-sao --no-sao-non-deblock --range limited --colorprim 1 --transfer 1 --colormatrix 1 --output-depth 10
set x265=D:\VapourSynth64Portable_2020_09_06\bin\x265.exe
set filename=garupa-pico-s1_01

echo [Info] Start encodings %filename%

%vspipe% -c y4m "scripts\%filename%.vpy" - | %x265% --y4m %params1% --crf 16 --output "done\%filename%.mp4" -

pause
rem shutdown -s