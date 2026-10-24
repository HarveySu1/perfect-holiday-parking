#!/usr/bin/env bash
# slidep wrapper: engine lives in lib/node_modules (shim path is stale).
# Always run inside the project dir so relative asset paths resolve correctly.
NODE="/c/Users/Su/.workbuddy/binaries/node/versions/22.22.2-6/node.exe"
ENGINE="/c/Users/Su/.workbuddy/binaries/node/versions/22.22.2-6/lib/node_modules/@tencent/slidep/dist/index.js"
cd "/c/ppt-ws/车记得复赛汇报" || exit 1
exec "$NODE" "$ENGINE" "$@"
