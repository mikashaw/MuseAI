import librosa 
import soundfile as sf
import os 
import numpy as np

class MinMaxNormaliser:
  """MinMaxNormaliser applies min max normalization to an array"""

  def __init__(self, min_val, max_val):
    self.min = min_val
    self.max = max_val 

  def normalise(self, array):
    norm_array = (array - array.min()) / (array.max() - array.min()) # ->
    norm_array = norm_array * (self.max - self.min) + self.min
    return norm_array
  
  def denormalise(self, norm_array, original_min, original_max):
    array = (norm_array - self.min) / (self.max - self.min)
    array = array * (original_max - original_min) + original_min
    return array

class SoundGenerator:

  def __init__(self, vae, hop_length):
    self.vae = vae
    self.hop_length = hop_length
    self._min_max_normaliser = MinMaxNormaliser(0, 1)

  def generate(self, spectrograms, min_max_values):
    
    generated_spectrograms, latent_representations = self.vae.reconstruct(spectrograms)
    signals = self.convert_spectrograms_to_audio(generated_spectrograms, min_max_values)
    return signals, latent_representations

  def convert_spectrograms_to_audio(self, spectrograms, min_max_values):
    signals = []
    for spectrogram, min_max_value in zip(spectrograms, min_max_values):
    # reshape the log spectrogram
      log_spectrogram = spectrogram[:,:,0]
    # apply denormalisation
      denorm_log_spec = self._min_max_normaliser.denormalise(
        log_spectrogram,
        min_max_value["min"],
        min_max_value["max"]
    )
    # log spectrogram -> spectrogram
      spec = librosa.db_to_amplitude(denorm_log_spec)
    # apply Griffin-Lim
      signal = librosa.istft(spec, hop_length = self.hop_length)
      signals.append(signal)
    return signals

def select_spectrograms(spectrograms,
                        file_paths,
                        min_max_values,
                        num_spectrograms=2):
    sampled_indexes = np.random.choice(range(len(spectrograms)), num_spectrograms)
    sampled_spectrogrmas = spectrograms[sampled_indexes]
    file_paths = [file_paths[index] for index in sampled_indexes]
    sampled_min_max_values = [min_max_values[file_path] for file_path in
                           file_paths]
    print(file_paths)
    print(sampled_min_max_values)
    return sampled_spectrogrmas, sampled_min_max_values


def save_signals(signals, save_dir, sample_rate=22050):
    for i, signal in enumerate(signals):
        save_path = os.path.join(save_dir, str(i) + ".wav")
        sf.write(save_path, signal, sample_rate)

def load_fsdd(spectrograms_path):
  x_train = []
  file_paths = []
  for root, _, file_names in os.walk(spectrograms_path):
    for file_name in file_names: 
      file_path = os.path.join(root, file_name)
      spectrogram = np.load(file_path) #(n_bins, n_frames, 1)
      file_paths.append(file_path)
      x_train.append(spectrogram)

  x_train = np.array(x_train)
  x_train = x_train[..., np.newaxis] # -> (3000, 256, 64, 1)
  return x_train, file_paths