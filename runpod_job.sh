#!/usr/bin/env bash
set -euo pipefail

# Run from the unzipped ReliaCircuit bundle root on a Linux GPU pod.
# Usage:
#   bash runpod_job.sh env
#   bash runpod_job.sh hf_access
#   bash runpod_job.sh smoke
#   bash runpod_job.sh subject_verb_ablation_pilot
#   bash runpod_job.sh full_subject_verb
#   bash runpod_job.sh circuit
#   bash runpod_job.sh bias_screen
#   bash runpod_job.sh bias_ablation_smoke
#   bash runpod_job.sh full_bias_ablation
#   bash runpod_job.sh bias_prediction
#
# Required for model loading:
#   export HF_TOKEN=...

MODE="${1:-smoke}"

HF_MODEL_ID="${HF_MODEL_ID:-google/gemma-2-2b}"
TL_MODEL_ID="${TL_MODEL_ID:-gemma-2-2b}"
SAE_RELEASE="${SAE_RELEASE:-gemma-scope-2b-pt-res-canonical}"
SAE_ID="${SAE_ID:-layer_20/width_16k/canonical}"
TOP_K="${TOP_K:-96}"
SMOKE_MAX_ROWS="${SMOKE_MAX_ROWS:-40}"
SVA_PILOT_MAX_PROMPTS="${SVA_PILOT_MAX_PROMPTS:-16}"
SVA_PILOT_MAX_FEATURES="${SVA_PILOT_MAX_FEATURES:-8}"
SVA_PILOT_MAX_ROWS="${SVA_PILOT_MAX_ROWS:-}"
SVA_PILOT_ROW_OFFSET="${SVA_PILOT_ROW_OFFSET:-0}"
SVA_PILOT_RESUME="${SVA_PILOT_RESUME:-0}"
SVA_FULL_MAX_PROMPTS="${SVA_FULL_MAX_PROMPTS:-}"
SVA_FULL_MAX_FEATURES="${SVA_FULL_MAX_FEATURES:-}"
SVA_FULL_MAX_ROWS="${SVA_FULL_MAX_ROWS:-}"
SVA_FULL_ROW_OFFSET="${SVA_FULL_ROW_OFFSET:-0}"
SVA_FULL_RESUME="${SVA_FULL_RESUME:-0}"
INSTALL_DEPS="${INSTALL_DEPS:-0}"
VENV_DIR="${VENV_DIR:-.venv}"

SVA_PROMPTS="${SVA_PROMPTS:-data/subject_verb_agreement/prompts.csv}"
SVA_SCREEN_SCORES="${SVA_SCREEN_SCORES:-results/subject_verb_agreement/screen_scores.csv}"
SVA_SCREENED_FEATURES="${SVA_SCREENED_FEATURES:-data/subject_verb_agreement/screened_features.csv}"
SVA_CLEAN_METRIC_CACHE="${SVA_CLEAN_METRIC_CACHE:-results/subject_verb_agreement/clean_metric_cache.csv}"
SVA_ABLATION_MANIFEST="${SVA_ABLATION_MANIFEST:-data/subject_verb_agreement/ablation_manifest.csv}"
SVA_ABLATION_MANIFEST_PILOT="${SVA_ABLATION_MANIFEST_PILOT:-data/subject_verb_agreement/ablation_manifest_pilot.csv}"
SVA_ABLATION_MANIFEST_SMOKE="${SVA_ABLATION_MANIFEST_SMOKE:-data/subject_verb_agreement/ablation_manifest_smoke.csv}"
SVA_EXACT_CACHE="${SVA_EXACT_CACHE:-results/subject_verb_agreement/exact_ablation_cache.csv}"
SVA_EXACT_CACHE_PILOT="${SVA_EXACT_CACHE_PILOT:-results/subject_verb_agreement/exact_ablation_cache_pilot.csv}"
SVA_EXACT_CACHE_SMOKE="${SVA_EXACT_CACHE_SMOKE:-results/subject_verb_agreement/exact_ablation_cache_smoke.csv}"
SVA_CIRCUIT_MANIFEST="${SVA_CIRCUIT_MANIFEST:-data/subject_verb_agreement/circuit_eval_manifest.csv}"
SVA_JOINT_CIRCUIT_CACHE="${SVA_JOINT_CIRCUIT_CACHE:-results/subject_verb_agreement/joint_circuit_cache.csv}"

BIAS_NORMALIZED="${BIAS_NORMALIZED:-data/bias_in_bios/bias_in_bios_normalized.csv}"
BIAS_PROMPTS="${BIAS_PROMPTS:-data/bias_in_bios/prompts.csv}"
BIAS_LABELS="${BIAS_LABELS:-data/bias_in_bios/profession_labels.csv}"
BIAS_PAIRED_PROMPTS="${BIAS_PAIRED_PROMPTS:-data/bias_in_bios/paired_prompts.csv}"
BIAS_SCREEN_SCORES="${BIAS_SCREEN_SCORES:-results/bias_in_bios/pair_screen_scores.csv}"
BIAS_SCREENED_FEATURES="${BIAS_SCREENED_FEATURES:-data/bias_in_bios/pair_screened_features.csv}"
BIAS_ABLATION_MANIFEST="${BIAS_ABLATION_MANIFEST:-data/bias_in_bios/pair_ablation_manifest.csv}"
BIAS_EXACT_CACHE="${BIAS_EXACT_CACHE:-results/bias_in_bios/exact_ablation_cache.csv}"
BIAS_SELECTED_EBH="${BIAS_SELECTED_EBH:-results/bias_in_bios/cache_analysis/selected_features_e_bh_pcal.csv}"
BIAS_SELECTED_TOP="${BIAS_SELECTED_TOP:-data/bias_in_bios/pair_screened_features.csv}"
BIAS_PREDICTION_CACHE="${BIAS_PREDICTION_CACHE:-results/bias_in_bios/bias_in_bios_prediction_cache.csv}"

ensure_venv() {
  if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
    if ! python -m venv --system-site-packages "${VENV_DIR}"; then
      if command -v apt-get >/dev/null 2>&1; then
        apt-get update
        apt-get install -y python3-venv python3-full
      fi
      python -m venv --system-site-packages "${VENV_DIR}"
    fi
  fi
  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
}

if [[ "${INSTALL_DEPS}" == "1" ]]; then
  ensure_venv
  python -m pip install --upgrade pip
  python -m pip install -r requirements-gpu.txt
elif [[ -x "${VENV_DIR}/bin/python" ]]; then
  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
fi

mkdir -p \
  results/gpu_smoke \
  results/subject_verb_agreement \
  results/bias_in_bios \
  data/subject_verb_agreement \
  data/bias_in_bios

mkdir -p \
  "$(dirname "${SVA_SCREEN_SCORES}")" \
  "$(dirname "${SVA_SCREENED_FEATURES}")" \
  "$(dirname "${SVA_CLEAN_METRIC_CACHE}")" \
  "$(dirname "${SVA_ABLATION_MANIFEST}")" \
  "$(dirname "${SVA_ABLATION_MANIFEST_PILOT}")" \
  "$(dirname "${SVA_ABLATION_MANIFEST_SMOKE}")" \
  "$(dirname "${SVA_EXACT_CACHE}")" \
  "$(dirname "${SVA_EXACT_CACHE_PILOT}")" \
  "$(dirname "${SVA_EXACT_CACHE_SMOKE}")" \
  "$(dirname "${SVA_CIRCUIT_MANIFEST}")" \
  "$(dirname "${SVA_JOINT_CIRCUIT_CACHE}")"

ensure_file() {
  local path="$1"
  local hint="$2"
  if [[ ! -f "${path}" ]]; then
    echo "Missing required file: ${path}" >&2
    echo "${hint}" >&2
    exit 2
  fi
}

is_truthy() {
  case "$1" in
    1|true|TRUE|yes|YES|y|Y)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

run_env_smoke() {
  python scripts/gpu_smoke_test.py \
    --skip-model-load \
    --skip-sae \
    --output results/gpu_smoke/pod_env.json
}

run_full_smoke() {
  python scripts/gpu_smoke_test.py \
    --model-id "${HF_MODEL_ID}" \
    --sae-release "${SAE_RELEASE}" \
    --sae-id "${SAE_ID}" \
    --output results/gpu_smoke/full_gemma_scope.json
}

run_hf_access_probe() {
  python scripts/probe_hf_access.py \
    --model-id "${HF_MODEL_ID}" \
    --filename config.json \
    --output-dir results/hf_access_probe
}

run_subject_verb_screen() {
  python scripts/produce_sae_screen_scores.py \
    --model-id "${TL_MODEL_ID}" \
    --sae-release "${SAE_RELEASE}" \
    --sae-id "${SAE_ID}" \
    --prompts "${SVA_PROMPTS}" \
    --split screen \
    --top-k "${TOP_K}" \
    --output "${SVA_SCREEN_SCORES}" \
    --features-output "${SVA_SCREENED_FEATURES}"
}

run_subject_verb_metric_cache() {
  python scripts/produce_hf_metric_cache.py \
    --model-id "${HF_MODEL_ID}" \
    --prompts "${SVA_PROMPTS}" \
    --output "${SVA_CLEAN_METRIC_CACHE}"
}

run_subject_verb_ablation_smoke() {
  python scripts/produce_sae_ablation_cache.py \
    --model-id "${TL_MODEL_ID}" \
    --sae-release "${SAE_RELEASE}" \
    --sae-id "${SAE_ID}" \
    --manifest "${SVA_ABLATION_MANIFEST_SMOKE}" \
    --output "${SVA_EXACT_CACHE_SMOKE}" \
    --max-rows "${SMOKE_MAX_ROWS}"
}

run_subject_verb_ablation_full() {
  run_subject_verb_ablation_from_screened \
    "${SVA_ABLATION_MANIFEST}" \
    "${SVA_EXACT_CACHE}" \
    "${SVA_FULL_MAX_PROMPTS}" \
    "${SVA_FULL_MAX_FEATURES}" \
    "${SVA_FULL_MAX_ROWS}" \
    "${SVA_FULL_ROW_OFFSET}" \
    "${SVA_FULL_RESUME}"
}

run_subject_verb_ablation_pilot() {
  run_subject_verb_ablation_from_screened \
    "${SVA_ABLATION_MANIFEST_PILOT}" \
    "${SVA_EXACT_CACHE_PILOT}" \
    "${SVA_PILOT_MAX_PROMPTS}" \
    "${SVA_PILOT_MAX_FEATURES}" \
    "${SVA_PILOT_MAX_ROWS}" \
    "${SVA_PILOT_ROW_OFFSET}" \
    "${SVA_PILOT_RESUME}"
}

run_subject_verb_ablation_from_screened() {
  local manifest="$1"
  local output_cache="$2"
  local max_prompts="$3"
  local max_features="$4"
  local max_rows="$5"
  local row_offset="$6"
  local resume="$7"
  ensure_file "${SVA_SCREENED_FEATURES}" "Run 'bash runpod_job.sh smoke' or upload screened_features.csv first."

  local manifest_cmd=(
    python scripts/create_ablation_sweep_manifest.py
    --prompts "${SVA_PROMPTS}"
    --features "${SVA_SCREENED_FEATURES}"
    --output "${manifest}"
  )
  if [[ -n "${max_prompts}" ]]; then
    manifest_cmd+=(--max-prompts "${max_prompts}")
  fi
  if [[ -n "${max_features}" ]]; then
    manifest_cmd+=(--max-features "${max_features}")
  fi
  "${manifest_cmd[@]}"

  local cache_cmd=(
    python scripts/produce_sae_ablation_cache.py
    --model-id "${TL_MODEL_ID}"
    --sae-release "${SAE_RELEASE}"
    --sae-id "${SAE_ID}"
    --manifest "${manifest}"
    --output "${output_cache}"
  )
  if [[ -n "${max_rows}" ]]; then
    cache_cmd+=(--max-rows "${max_rows}")
  fi
  if [[ "${row_offset}" != "0" ]]; then
    cache_cmd+=(--row-offset "${row_offset}")
  fi
  if is_truthy "${resume}"; then
    cache_cmd+=(--resume)
  fi
  "${cache_cmd[@]}"
}

run_subject_verb_circuit() {
  local manifest="${CIRCUIT_MANIFEST:-${SVA_CIRCUIT_MANIFEST}}"
  if [[ ! -f "${manifest}" ]]; then
    echo "Missing circuit manifest: ${manifest}" >&2
    echo "Create it after CPU FDR analysis with scripts/create_circuit_eval_manifest.py." >&2
    exit 2
  fi
  python scripts/produce_sae_circuit_cache.py \
    --model-id "${TL_MODEL_ID}" \
    --sae-release "${SAE_RELEASE}" \
    --sae-id "${SAE_ID}" \
    --manifest "${manifest}" \
    --output "${SVA_JOINT_CIRCUIT_CACHE}"
}

run_bias_pairs() {
  ensure_file "${BIAS_NORMALIZED}" "Prepare or upload the normalized BiasInBios CSV before running BiasInBios GPU jobs."
  python scripts/build_bias_in_bios_pair_prompts.py \
    --input "${BIAS_NORMALIZED}" \
    --output "${BIAS_PAIRED_PROMPTS}"
}

run_bias_screen() {
  run_bias_pairs
  python scripts/produce_sae_screen_scores.py \
    --model-id "${TL_MODEL_ID}" \
    --sae-release "${SAE_RELEASE}" \
    --sae-id "${SAE_ID}" \
    --prompts "${BIAS_PAIRED_PROMPTS}" \
    --score-mode activation_delta \
    --split screen \
    --top-k "${TOP_K}" \
    --output "${BIAS_SCREEN_SCORES}" \
    --features-output "${BIAS_SCREENED_FEATURES}"
}

run_bias_ablation() {
  local output_cache="$1"
  local max_rows="${2:-}"
  ensure_file "${BIAS_PAIRED_PROMPTS}" "Run 'bash runpod_job.sh bias_screen' first."
  ensure_file "${BIAS_SCREENED_FEATURES}" "Run 'bash runpod_job.sh bias_screen' first."

  python scripts/create_ablation_sweep_manifest.py \
    --prompts "${BIAS_PAIRED_PROMPTS}" \
    --features "${BIAS_SCREENED_FEATURES}" \
    --split test \
    --output "${BIAS_ABLATION_MANIFEST}"

  local cmd=(
    python scripts/produce_sae_ablation_cache.py
    --model-id "${TL_MODEL_ID}"
    --sae-release "${SAE_RELEASE}"
    --sae-id "${SAE_ID}"
    --manifest "${BIAS_ABLATION_MANIFEST}"
    --metric-mode label_logprob
    --labels "${BIAS_LABELS}"
    --target-label-column target_label
    --output "${output_cache}"
  )
  if [[ -n "${max_rows}" ]]; then
    cmd+=(--max-rows "${max_rows}")
  fi
  "${cmd[@]}"
}

run_bias_prediction() {
  ensure_file "${BIAS_PROMPTS}" "Prepare or upload data/bias_in_bios/prompts.csv before prediction-cache production."
  ensure_file "${BIAS_LABELS}" "Prepare or upload data/bias_in_bios/profession_labels.csv before prediction-cache production."
  ensure_file "${BIAS_SELECTED_EBH}" "Run CPU analysis on the BiasInBios exact-ablation cache, then upload selected_features_e_bh_pcal.csv."

  local feature_args=(--feature-set "e_bh_pcal=${BIAS_SELECTED_EBH}")
  if [[ -f "${BIAS_SELECTED_TOP}" ]]; then
    feature_args+=(--feature-set "top_score=${BIAS_SELECTED_TOP}")
  fi

  python scripts/produce_bias_in_bios_prediction_cache.py \
    --model-id "${TL_MODEL_ID}" \
    --sae-release "${SAE_RELEASE}" \
    --sae-id "${SAE_ID}" \
    --prompts "${BIAS_PROMPTS}" \
    --labels "${BIAS_LABELS}" \
    "${feature_args[@]}" \
    --output "${BIAS_PREDICTION_CACHE}"
}

case "${MODE}" in
  env)
    run_env_smoke
    ;;
  hf_access)
    run_hf_access_probe
    ;;
  smoke)
    run_env_smoke
    run_full_smoke
    run_subject_verb_metric_cache
    run_subject_verb_screen
    run_subject_verb_ablation_smoke
    ;;
  subject_verb_ablation_pilot)
    run_subject_verb_ablation_pilot
    ;;
  full_subject_verb)
    run_full_smoke
    run_subject_verb_metric_cache
    run_subject_verb_screen
    run_subject_verb_ablation_full
    ;;
  circuit)
    run_subject_verb_circuit
    ;;
  bias_screen)
    run_full_smoke
    run_bias_screen
    ;;
  bias_ablation_smoke)
    run_bias_screen
    run_bias_ablation results/bias_in_bios/exact_ablation_cache_smoke.csv "${SMOKE_MAX_ROWS}"
    ;;
  full_bias_ablation)
    run_full_smoke
    run_bias_screen
    run_bias_ablation "${BIAS_EXACT_CACHE}"
    ;;
  bias_prediction)
    run_full_smoke
    run_bias_prediction
    ;;
  *)
    echo "Unknown mode: ${MODE}" >&2
    exit 2
    ;;
esac
