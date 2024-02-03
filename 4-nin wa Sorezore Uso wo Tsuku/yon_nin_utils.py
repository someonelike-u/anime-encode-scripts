from vstools import vs, core, depth, join, get_y
from vsaa import upscaled_sraa
from G41Fun import Hysteria
from havsfunc import FineDehalo, HQDeringmod
from kagefunc import hybriddenoise, retinex_edgemask, adaptive_grain

class YonNinFiltering:
	"""
	4-nin wa Sorezore Uso wo Tsuku anime class for filtering.

		- episodeNumber: The number of the episode.
	"""
	def __init__(self, episodeNumber):
		self.episodeNumber = episodeNumber
		src = core.lsmas.LWLibavSource(f'yon_nin_bd_{self.episodeNumber}.mkv')
		self.src16 = depth(src, 16)

	def edgeProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		luma = get_y(clip)
		antiAliased = upscaled_sraa(luma, rfactor=1.6)
		aliasingFixed = join(antiAliased, self.src16)
		sharpEdge = Hysteria(aliasingFixed, sstr=0.2, usemask=False)
		dehalo = FineDehalo(sharpEdge, rx=2.4, darkstr=0, brightstr=0.8, thmi=44)
		return HQDeringmod(dehalo, mthr=24, nrmode=2, sharp=0, darkthr=0)

	def denoiseProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		denoised = hybriddenoise(depth(clip, 32), 0.45, 1.5)
		return depth(denoised, 16)

	def debandProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		deband = core.neo_f3kdb.Deband(clip, range=16, y=32, cb=32, cr=32, grainy=0, grainc=0)
		debandMask = retinex_edgemask(clip, sigma=2).std.Binarize(8500).std.Inflate()
		return core.std.MaskedMerge(deband, clip, debandMask)

	def grainProcess(self, clip: vs.VideoNode) -> vs.VideoNode:
		return adaptive_grain(clip, 0.3, static=False)

	def startFiltering(self) -> vs.VideoNode:
		rescale = self.edgeProcess(self.src16)
		denoise = self.denoiseProcess(rescale)
		deband = self.debandProcess(denoise)
		return self.grainProcess(deband)

	def getSrc(self) -> vs.VideoNode:
		return self.src16