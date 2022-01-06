from preprocessing import Loader, Padder, LogSpectrogramExtractor, MinMaxNormaliser, Saver, PreprocessingPipeline

FRAME_SIZE = 512
HOP_LENGTH = 256
DURATION = 0.74 #get a nice number of frames
SAMPLE_RATE = 22050 
MONO = True

SPECTROGRAMS_SAVE_DIR = "/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/spectrograms"
MIN_MAX_VALUES_SAVE_DIR = "/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/min_max_values"
FILES_DIR = "/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/recordings"

loader = Loader(SAMPLE_RATE, DURATION, MONO)
padder = Padder()
log_spectrogram_extractor = LogSpectrogramExtractor(FRAME_SIZE, HOP_LENGTH)
min_max_normalizer = MinMaxNormaliser(0,1)
saver = Saver(SPECTROGRAMS_SAVE_DIR, MIN_MAX_VALUES_SAVE_DIR)

preprocessing_pipeline = PreprocessingPipeline()
preprocessing_pipeline.loader = loader 
preprocessing_pipeline.padder = padder
preprocessing_pipeline.extractor = log_spectrogram_extractor
preprocessing_pipeline.normaliser = min_max_normalizer
preprocessing_pipeline.saver = saver

def process():
    preprocessing_pipeline.process(FILES_DIR)


print("preprocessing files")
process()
