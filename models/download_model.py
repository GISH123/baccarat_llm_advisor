from huggingface_hub import snapshot_download, hf_hub_download
import os

os.makedirs("models", exist_ok=True)

# =========================
# UNQUANTIZED MODELS
# =========================

# ✅ Meta Llama 3.1 8B Instruct
snapshot_download(
    repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
    local_dir="models/Meta-Llama-3.1-8B-Instruct"
)
print("meta done")

# ✅ Mistral 7B Instruct v0.2
snapshot_download(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    local_dir="models/Mistral-7B-Instruct-v0.2"
)

print("mistral done")

# ✅ Gemma 7B
snapshot_download(
    repo_id="google/gemma-7b",
    local_dir="models/gemma-7b"
)
print("gemma done")
# ✅ Velvet 14B
snapshot_download(
    repo_id="almawave/Velvet-14B",
    local_dir="models/Velvet-14B"
)
print("velvet done")
# ✅ DeepSeek LLM 7B Instruct
snapshot_download(
    repo_id="deepseek-ai/deepseek-llm-7b-chat",
    local_dir="models/deepseek-llm-7b-chat"
)
print("deepseek done")
# =========================
# QUANTIZED GGUF MODELS
# =========================

# ✅ Quantized Meta Llama 3.1 8B Instruct
hf_hub_download(
    repo_id="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    filename="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
    local_dir="models/Meta-Llama-3.1-8B-Instruct-GGUF"
)

# ✅ Quantized Mistral 7B Instruct
hf_hub_download(
    repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
    filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    local_dir="models/Mistral-7B-Instruct-v0.2-GGUF"
)

# Download Gemma 7B Q4_K_M GGUF model
hf_hub_download(
    repo_id="MaziyarPanahi/gemma-7b-GGUF",
    filename="gemma-7b.Q4_K_M.gguf",
    local_dir="models/gemma-7b-GGUF"
)

# Download Velvet-14B Q4_K_M GGUF model
hf_hub_download(
    repo_id="SistInf/Velvet-14B-GGUF",
    filename="Velvet-14B-Q4_K_M.gguf",
    local_dir="models/Velvet-14B-GGUF"
)

# ✅ Quantized DeepSeek 7B
hf_hub_download(
    repo_id="TheBloke/deepseek-llm-7B-chat-GGUF",
    filename="deepseek-llm-7b-chat.Q4_K_M.gguf",
    local_dir="models/deepseek-llm-7B-chat-GGUF"
)
