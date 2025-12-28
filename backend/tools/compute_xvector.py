"""
Compute a SpeechT5-compatible speaker xvector (512-d) from a WAV/MP3 file
and save it to a .npy file. You can then point app2.py to this file via
SPEAKER_XVECTOR in your .env to use your own voice without loading
SpeechBrain at runtime.

Recommended to run in Python 3.11 or in Google Colab if Windows 3.12/torchaudio
gives issues.

Install deps (in a fresh venv):
  pip install torch torchaudio transformers speechbrain librosa soundfile numpy scipy

Usage:
  python tools/compute_xvector.py --input voices/my_voice.wav --output voices/my_voice_xvector.npy
"""

import argparse
import os
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input WAV/MP3 with your voice (10–30s recommended)")
    parser.add_argument("--output", required=True, help="Path to output .npy (xvector)")
    parser.add_argument("--sr", type=int, default=16000, help="Resample sample rate (default 16000)")
    args = parser.parse_args()

    import torch
    import librosa
    from speechbrain.pretrained import EncoderClassifier

    audio, _ = librosa.load(args.input, sr=args.sr, mono=True)
    if audio.size == 0:
        raise RuntimeError("Input audio appears empty")

    wav = torch.from_numpy(audio).unsqueeze(0)
    encoder = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-xvect-voxceleb",
        savedir=os.path.join(os.getcwd(), "_sb_xvect")
    )
    emb = encoder.encode_batch(wav)
    emb = emb.squeeze(0)
    if emb.ndim == 1:
        emb = emb.unsqueeze(0)
    if emb.shape[1] != 512:
        raise RuntimeError(f"Unexpected xvector shape {tuple(emb.shape)}; expected (1, 512)")

    np.save(args.output, emb.detach().cpu().numpy())
    print(f"Saved xvector to {args.output}")


if __name__ == "__main__":
    main()

