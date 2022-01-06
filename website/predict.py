from autoencoder import Autoencoder
from sample import SoundGenerator, select_spectrograms, save_signals
import pickle 
from sample import load_fsdd 


HOP_LENGTH = 256
SAVE_DIR_ORIGINAL = "/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/original"
SAVE_DIR_GENERATED = "/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/generated"
MIN_MAX_VALUES_PATH = "/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/min_max_values/min_max_values.pkl"
SPECTROGRAMS_PATH = "/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/spectrograms"

def run_predictions():

    autoencoder = Autoencoder(
        input_shape = (256,64,1),
        conv_filters = (512,256,128,64,32),
        conv_kernels = (3,3,3,3,3),
        conv_strides = (2,2,2,2, (2,1)),
        latent_space_dim=128
    )
    autoencoder = autoencoder.load("/Users/mikashaw/code/ML_Projects/MuseAI/MuseAI/website/model")

    sound_generator = SoundGenerator(autoencoder, HOP_LENGTH)

    with open(MIN_MAX_VALUES_PATH, "rb") as f:
        min_max_values = pickle.load(f)

    specs, file_paths = load_fsdd(SPECTROGRAMS_PATH)

    sampled_specs, sampled_min_max_values = select_spectrograms(specs,
                                                              file_paths,
                                                              min_max_values,
                                                              2)
    signals, _ = sound_generator.generate(sampled_specs,
                                        sampled_min_max_values)

    original_signals = sound_generator.convert_spectrograms_to_audio(
      sampled_specs, sampled_min_max_values
      )

    save_signals(signals, SAVE_DIR_GENERATED)
    save_signals(original_signals, SAVE_DIR_ORIGINAL)

run_predictions()





