# AECMOS, DNSMOS, PLCMOS

* We release the [AECMOS](https://ieeexplore.ieee.org/document/9747836 "AECMOS: A Speech Quality Assessment Metric for Echo Impairment."), [DNSMOS](https://ieeexplore.ieee.org/document/9746108 "DNSMOS P.835: A Non-Intrusive Perceptual Objective Speech Quality Metric to Evaluate Noise Suppressors."), and [PLCMOS](https://arxiv.org/abs/2305.15127 "PLCMOS--a data-driven non-intrusive metric for the evaluation of packet loss concealment algorithms.") models that we have developed for evaluating audio degradations due to echo, noise, packet loss and other sources.

## Prerequisites
- Python 3.7 and above
- librosa 0.9.1
- numpy 1.21.5
- onnxruntime 1.10.0
- pandas
- tqdm


## Usage:
```python
from speechmos import aecmos, dnsmos, plcmos

aecmos.run(sample, sr, talk_type, **kwargs)

dnsmos.run(sample, sr, **kwargs)

plcmos.run(sample, sr, **kwargs)
``` 

- `sample` is one of the following:
    - For AECMOS:  dictionary of the form `{'lpb': lpb, 'mic': mic, 'enh': enh}` corresponding to the loopback, microphone, and enhanced audio as type `np.ndarray` or paths to audio files of type supported by `librosa`. 
    - For DNSMOS and PLCMOS: `np.ndarray` or a path to an audio file of type supported by `librosa`.
    
    All audio should be single channel (mono) audio.  
    Alternatively, `sample` can be a list of items of one of the above types.  

-  `sr` denotes the sampling rate. Sampling rate should be either 16000 or 48000. AECMOS is available at 48kHz, all other models are available at 16kHz. All audio should be provided at the correct sampling rate.

For AECMOS:
- `talk_type` specifies the scenario: `'st'` (far-end single talk), `'nst'` (near-end single talk), or `'dt'` (double talk) if known. `talk_type` can be `None` in which case the 16kHz scenarioless model can be used. The performance is about 2% lower in correlation with the ground truth than the scenario based model.

For DNSMOS: 
- `model_type` controls which DNSMOS model to use: `'dnsmos'` or `'dnsmos_personalized'`. The default is `'dnsmos'`.

Additional arguments:
- `return_df` controls whether a pandas dataframe is returned containing sample information and MOS scores when evaluating a list of samples. The default is `return_df = True`. If set to `False`, a list of dictionaries is returned instead.
- `verbose` controls whether more details are printed on the screen. The default is `verbose = False`.

## Usage examples:

#### AECMOS usage example with `sample` as a dictionary of numpy arrays and unknown `talk_type`.

```python
import librosa
from speechmos import aecmos

lpb, _ = librosa.load("d:/data/example/lpb.wav", sr=16000)
mic, _ = librosa.load("d:/data/example/mic.wav", sr=16000)
enh, _ = librosa.load("d:/data/example/enh.wav", sr=16000)

sample = {'lpb': lpb, 'mic': mic, 'enh': enh}

aecmos.run(sample, sr= 16000, verbose= True)
```

Output:
```
Model version aecmos_scenarioless_16kHz.
The model sampling rate is 16000.
{'echo_mos': 4.9999470710754395, 'deg_mos': 3.4854962825775146, 'talk_type': None, 'model_name': 'aecmos_scenarioless_16kHz'}
```


#### AECMOS usage example with `sample` as a list of dictionaries of paths to audio files.

```python
from speechmos import aecmos
aecmos.run(sample_list, sr=48000, 'dt', verbose = True)
```

Output:
```
Using model aecmos_48kHz to evaluate 3 samples.
Model sampling rate is 48000.
0it [00:00, ?it/s]
1it [00:00,  8.59it/s]
3it [00:00, 25.77it/s]
{'lpb_path': 'D:/data/example/lpb.wav', 'mic_path': 'D:/data/example/mic.wav', 'enh_path': 'D:/data/example/enh.wav', 'echo_mos': 3.2400383949279785, 'deg_mos': 3.4087774753570557, 'talk_type': 'dt', 'model_name': 'aecmos_48kHz'}
{'lpb_path': 'D:/data/example/lpb.wav', 'mic_path': 'D:/data/example/mic.wav', 'enh_path': 'D:/data/example/enh.wav', 'echo_mos': 3.2400383949279785, 'deg_mos': 3.4087774753570557, 'talk_type': 'dt', 'model_name': 'aecmos_48kHz'}
{'lpb_path': 'D:/data/example/lpb.wav', 'mic_path': 'D:/data/example/mic.wav', 'enh_path': 'D:/data/example/enh.wav', 'echo_mos': 3.2400383949279785, 'deg_mos': 3.4087774753570557, 'talk_type': 'dt', 'model_name': 'aecmos_48kHz'}
       echo_mos   deg_mos
count  3.000000  3.000000
mean   3.240038  3.408777
std    0.000000  0.000000
min    3.240038  3.408777
25%    3.240038  3.408777
50%    3.240038  3.408777
75%    3.240038  3.408777
max    3.240038  3.408777
```

#### DNSMOS usage example with `sample` as a numpy array:

```python
import librosa
from speechmos import dnsmos

audio, _ = librosa.load("D:/data/example/enh.wav", sr=16000)
dnsmos.run(audio, sr=16000)
```

Output:
```
{'filename': 'D:/data/example/enh.wav',
 'ovrl_mos': 2.2067626609880104,
 'sig_mos': 3.290418848414798,
 'bak_mos': 2.141338429075571,
 'p808_mos': 3.0722866}
```

#### PLCMOS usage example with `sample` as a path to an audio file:

```python
import librosa
from speechmos import plcmos

plcmos.run("D:/data/example/enh.wav", sr=16000)
```

Output:
```
{'filename': 'D:/data/example/enh.wav',
 'plcmos': 2.5210512320200604,
 'model': 'plcmos_v2'}
```

## Citation:
C. K. A. Reddy, V. Gopal and R. Cutler, "Dnsmos P.835: A Non-Intrusive Perceptual Objective Speech Quality Metric to Evaluate Noise Suppressors," ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Singapore, Singapore, 2022, pp. 886-890, doi: 10.1109/ICASSP43922.2022.9746108.

L. Diener, M. Purin, S. Sootla, A. Saabas, R. Aichner, and R. Cutler, "PLCMOS--a data-driven non-intrusive metric for the evaluation of packet loss concealment algorithms." arXiv preprint arXiv:2305.15127 (2023).

M. Purin, S. Sootla, M. Sponza, A. Saabas and R. Cutler, "AECMOS: A Speech Quality Assessment Metric for Echo Impairment," ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Singapore, Singapore, 2022, pp. 901-905, doi: 10.1109/ICASSP43922.2022.9747836.
