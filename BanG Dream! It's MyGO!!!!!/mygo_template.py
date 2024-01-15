import sys
import os

# Dark magic to import mygo_utils as a module in same folder
currentFolder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFolder)

from mygo_utils import MyGoFiltering

episodeNumber = 'EPISODE_NUMBER'
openingStartFrame = OPENING_START_FRAME
endingRange = [ENDING_RANGE]

initEpisode = MyGoFiltering(episodeNumber, openingStartFrame, endingRange)
filteredEpisode = initEpisode.startFiltering()
#initEpisode.getSrc().set_output(0)
filteredEpisode.set_output()