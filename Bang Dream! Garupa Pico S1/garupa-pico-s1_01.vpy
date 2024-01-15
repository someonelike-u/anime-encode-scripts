import vapoursynth as vs
import kagefunc as kgf
from vsutil import depth
import G41Fun as fun
from nnedi3_rpow2 import nnedi3_rpow2
import havsfunc as ha

core = vs.core

file = r'..\Bang Dream! Garupa Pico - 01_BD.mkv'
src = core.ffms2.Source(source=file)
src16 = depth(src, 16)

# AA + Dark line
antiAliasing = nnedi3_rpow2(src16).resize.Spline36(1920, 1080)
darkLine = fun.Hysteria(antiAliasing, 0.75)
video = ha.HQDeringmod(darkLine)

# Deband + grain
deband = core.neo_f3kdb.Deband(video, y=32, cb=32, cr=32, grainy=32, grainc=32, output_depth=16)
line_mask = kgf.retinex_edgemask(video).std.Binarize(7000).std.Inflate()
mergedDeband = core.std.MaskedMerge(deband, video, line_mask)
merged = kgf.adaptive_grain(mergedDeband, 0.3)

# Final output in 10-bit
merged = depth(merged, 10)
merged.set_output()

print(merged.num_frames)
