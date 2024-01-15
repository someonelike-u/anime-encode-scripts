import vapoursynth as vs
import fvsfunc as fvf
import kagefunc as kgf
import vardefunc as vdf
from vsutil import depth, get_y, get_w
from typing import Optional, Dict, Any
import muvsfunc as muvf
import havsfunc as ha
from nnedi3_rpow2 import nnedi3_rpow2
import vsaa
import havsfunc as haf
from vsTAAmbk import TAAmbk
import lvsfunc as lvf
import rekt

core = vs.core

file = r'..\D4DJ Double Mix_BD.mkv'
src = core.lsmas.LWLibavSource(source=file)
denoise = kgf.hybriddenoise(depth(src, 32), 0.45, 1.5)
src16 = depth(denoise, 16)

height = 806
luma = get_y(src16)
width = get_w(height)

# Rescale + AA (+ dehalo + deringing)
descale = kgf._descale_luma(depth(luma, 32), width, height, 'bicubic', 4, 1/3, 1/3)
descale = TAAmbk(depth(descale, 16), aatype='Nnedi3', nsize=4, nns=4, mytpe=1, down8=False, opencl=True)
upscale = nnedi3_rpow2(descale)
downscale = muvf.SSIM_downsample(upscale, 1920, 1080, kernel='bicubic', filter_param_a=1/3, filter_param_b=1/3)

merged = vdf.misc.merge_chroma(depth(downscale, 16), src16)
merged = haf.FineDehalo(merged, rx=2.4, darkstr=0, brightstr=0.8, thmi=44)
merged = haf.HQDeringmod(merged, mthr=24, nrmode=2, sharp=0, darkthr=0)

deband = core.neo_f3kdb.Deband(merged, y=32, cb=32, cr=32, grainy=32, grainc=32, output_depth=16)
debandMask = kgf.retinex_edgemask(merged).std.Binarize(5000).std.Inflate()
fixDeband = core.std.MaskedMerge(deband, merged, debandMask)

merged = kgf.adaptive_grain(fixDeband)

cred_m = vdf.mask.drm_old(depth(src, 16), height)
merged = lvf.rfs(merged, rekt.rekt(merged, core.std.MaskedMerge(merged, depth(src, 16), cred_m), 422, 92, 1920 - 684, 1080 - 180), [(33542, 33649)])
merged = lvf.rfs(merged, rekt.rekt(merged, core.std.MaskedMerge(merged, depth(src, 16), cred_m), 346, 484, 1920 - 532, 1080 - 584), [(33657, 33727)])
merged = lvf.rfs(merged, core.std.MaskedMerge(merged, depth(src, 16), cred_m), [(33836, 33903)])

fixCredit = lvf.rfs(merged, depth(src, 16), [(27433, 29176), (33902, 34295)])

# Final output in 10-bit
merged = depth(fixCredit, 10)
#src.set_output(0)
merged.set_output()

print(merged.num_frames)
#src16.set_output()
