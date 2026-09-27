#!/usr/bin/env bash
# 인터넷이 불안정한 부스를 위해 손 인식 라이브러리와 모델을 vendor/ 폴더에 내려받는다.
# 한 번만 실행해 두면 app.js가 vendor/ 파일을 먼저 사용한다.
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION=0.10.14
BASE="https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@${VERSION}"
OUT=vendor/tasks-vision

mkdir -p "$OUT/wasm"
curl -fL "$BASE/vision_bundle.mjs" -o "$OUT/vision_bundle.mjs"
for f in vision_wasm_internal.js vision_wasm_internal.wasm vision_wasm_nosimd_internal.js vision_wasm_nosimd_internal.wasm; do
  curl -fL "$BASE/wasm/$f" -o "$OUT/wasm/$f"
done
curl -fL "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" \
  -o vendor/hand_landmarker.task

echo "완료! vendor/ 폴더에 오프라인 파일이 준비되었습니다."
