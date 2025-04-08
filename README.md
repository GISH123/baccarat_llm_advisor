# 20250314 using grok to generate unified pipeline codes

<!-- pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 # gish-ai computer has cuda version 12.4 -->
<!-- python -m pip install whl/torchvision-0.15.2+cu118-cp310-cp310-win_amd64.whl -->
conda create --name baccarat_clean_2 python=3.10 
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.4 -c pytorch -c nvidia
conda install transformers
pip install --upgrade torchvision torchaudio
pip install --upgrade torch transformers
# to fix warning issues for sdpa not implemented, we use flash attention instead
<!-- pip install flash-attn --no-build-isolation --index-url https://download.pytorch.org/whl/cu124 -->
<!-- pip install whl/flash_attn-2.7.0.post2-cp310-cp310-win_amd64.whl -->
裝flash attention太麻煩了 我直接不要用吧
pip install accelerate
pip install -U bitsandbytes

python main.py

<!-- huggingface-cli download Qwen/Qwen2-7B-Instruct --local-dir ./models/qwen2-7b-instruct --local-files-only -->