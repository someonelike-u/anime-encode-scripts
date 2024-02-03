import sys
import os

# Dark magic to import 4nin_utils as a module in same folder
currentFolder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFolder)

from yon_nin_utils import YonNinFiltering

episodeNumber = 'EPISODE_NUMBER'

initEpisode = YonNinFiltering(episodeNumber)
filteredEpisode = initEpisode.startFiltering()
#initEpisode.getSrc().set_output(0)
filteredEpisode.set_output()