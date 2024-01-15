from vstools import vs, core, join, depth, get_y, replace_ranges
from kagefunc import inverse_scale, hybriddenoise, retinex_edgemask, adaptive_grain
from vsaa import masked_clamp_aa, upscaled_sraa, clamp_aa
from edi_rpow2 import znedi3_rpow2
from vsscale import SSIM
from vskernels import Bicubic
from havsfunc import FineDehalo, EdgeCleaner, LSFmod
from pathlib import Path
from typing import NamedTuple
from vsmasktools import diff_rescale

class CreditMask(NamedTuple):
	mask: vs.VideoNode
	startFrame: int
	endFrame: int

class MyGoFiltering:
	"""
	MyGo anime class for filtering.

		- episodeNumber: The number of the episode.
		- openingStartFrame: The offset for the credit masks in the opening.
		- endingRange: The range containing the ending.
	"""
	def __init__(self, episodeNumber, openingStartFrame, endingRange):
		self.episodeNumber = episodeNumber
		self.openingStartFrame = openingStartFrame
		self.endingRange = endingRange

		self.nativeHeight = 806
		src = core.lsmas.LWLibavSource(f'mygo-{self.episodeNumber}.mkv')
		self.src16 = depth(src, 16)

	def denoiseProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		denoised = hybriddenoise(depth(clip, 32), 0.45, 1.5)
		return depth(denoised, 16)

	def rescaleProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		luma = get_y(clip)
		descale = inverse_scale(luma, height=self.nativeHeight, kernel='bicubic')
		
		AAMask = masked_clamp_aa(descale, strength=1, opencl=False)
		strongAA = upscaled_sraa(descale, rfactor=1.6)
		antiAliased = clamp_aa(descale, AAMask, strongAA, strength=1.5)

		upscale = znedi3_rpow2(antiAliased, 2)
		downscale = SSIM(Bicubic).scale(upscale, 1920, 1080)
		rescaled = join(depth(downscale, 16), self.src16)

		# Sharpen a little bit to compensate the blur of AA
		sharp = LSFmod(rescaled, defaults='slow', strength=20, Smode=3, Lmode=1, edgemode=1)

		dehalo = FineDehalo(sharp, darkstr=0, thlimi=16, thmi=64)
		cleanEdge = EdgeCleaner(dehalo, strength=8, smode=1, hot = True)
		return core.std.Expr([dehalo, cleanEdge], 'x y min')

	def debandProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		deband = core.neo_f3kdb.Deband(clip, range=16, y=48, cb=48, cr=48, grainy=0, grainc=0)
		debandMask = retinex_edgemask(clip, sigma=2).std.Binarize(8500).std.Inflate()
		return core.std.MaskedMerge(deband, clip, debandMask)

	def grainProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		return adaptive_grain(clip, 0.3, static=False)

	def maskCredits(self, clip: vs.VideoNode, pathName: Path, openingStartFrame: int = 0) -> vs.VideoNode:
		path = Path(pathName + '/')
		creditMasks = [
			CreditMask(core.imwri.Read(mask).resize.Point(format=vs.GRAY16, matrix_s='709', chromaloc_s='top_left'),
			int(str(mask.stem).split('_')[2]),
			int(str(mask.stem).split('_')[3])) for mask in path.glob('*')
		]
		creditMasked = clip
		for mask in creditMasks:
			creditMasked = replace_ranges(
				creditMasked,core.std.MaskedMerge(creditMasked, self.src16, mask.mask),
				[(mask.startFrame + openingStartFrame, mask.endFrame + openingStartFrame)]
			)
		return creditMasked

	def maskCreditsProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		fixEnding = replace_ranges(clip, self.src16, self.endingRange)
		if self.openingStartFrame != None:
			fixOpening = self.maskCredits(fixEnding, 'masks_op', self.openingStartFrame)
			fixCredits = self.maskCredits(fixOpening, f'masks_{self.episodeNumber}')
		else:
			fixCredits = self.maskCredits(fixEnding, f'masks_{self.episodeNumber}')
		#fixCredits = diff_rescale(self.src16, self.nativeHeight, thr = 0.5)
		return depth(fixCredits, 10)

	def startFiltering(self) -> vs.VideoNode:
		rescale = self.rescaleProcess(self.src16)
		denoise = self.denoiseProcess(rescale)
		deband = self.debandProcess(denoise)
		grain = self.grainProcess(deband)
		return self.maskCreditsProcess(grain)

	def getSrc(self) -> vs.VideoNode:
		return self.src16