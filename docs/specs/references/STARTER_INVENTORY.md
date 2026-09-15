# Starter inventory used for this breakdown

The supplied `deckforge-audited-starter.zip` was inspected to distinguish existing files/commands from future contracts. No starter application source is changed by this specification pack.

The copies of ARCHITECTURE.md and DEVELOPMENT_PLAN.md in this directory are byte-identical to the supplied originals. The local execution report is historical evidence from that delivery, not a new run.

## Existing npm scripts

```json
{
  "test": "node --test tests/*.test.mjs",
  "smoke": "node scripts/build-smoke.mjs",
  "inspect": "python3 scripts/inspect-pptx.py out/smoke/deck.pptx",
  "preview": "python3 scripts/render-local.py out/smoke/deck.pptx",
  "check": "npm test && npm run smoke && npm run inspect"
}
```

## Existing paths and SHA-256

| Path | SHA-256 |
|---|---|
| `.env.example` | `4e8096d44dc98516c9a72732436bad89ec23c4a330cfd7d7af951167daac11d5` |
| `.gitignore` | `2294551b2db31505ac19b0fc875a2b26a42c9547dbc9ff376f5cb740494fbc63` |
| `AGENTS.md` | `ac59626419a48d26ad5baac3717e946bf0c4f94a7ab562b07e3cea8a351659fc` |
| `ARCHITECTURE.md` | `36135014bfaad8395d4672f13f957dd04e39dfe98af1a7e2ace4abd31d223139` |
| `DEVELOPMENT_PLAN.md` | `1042ab64c9277fce38bc70b5629354794265722e1b318fce3fd60eff5ace21a0` |
| `LICENSE` | `94b9d3dae5b288dc2d60b5fd5aa81cf049d798378123d0a32244873c7659f359` |
| `README.md` | `b9d8676215fd8ec33c4f5799445b1d4cc9853446e0123b97a50b9f2a7602736f` |
| `THIRD_PARTY_NOTICES.md` | `144e410ac424b2272ecb2efd52c65023c242e41506a73a9cb17304561db3760e` |
| `config/upstreams.json` | `b92a15ee3f704bfc22ff517f5d1969b83c3861de64f6c79cec191234c304d110` |
| `docs/LOCAL_TEST_REPORT.md` | `471bbc240fdb9db384b14db43f52b0509ede96740bc8937e6e609a022ca4e2b6` |
| `examples/smoke-deck.json` | `6a34b8813892173ac631683ae9f24bbb752bdbbac4647288acc5a96b97a08d44` |
| `package.json` | `e4fdbe2facc45bbda4d698073b98462781c82ee01cc820a547923a7eb7aa66a4` |
| `scripts/build-smoke.mjs` | `bad6a01ef153c816aea8e3a0988c21c312972108dbccf0645ca87c7a24138f70` |
| `scripts/doctor.py` | `44febb75d608bd50c16c396c9d90d497ed39a89826943a937751a7403d632840` |
| `scripts/fetch-upstreams.py` | `c9f1439eca59bf6ad17c756d8ba7d0da50e340446e735692a049eba1784decef` |
| `scripts/inspect-pptx.py` | `f9711b84e9cf7fecf46a9245ee73ac7bf809761f162c807a8e648d9ab67044e3` |
| `scripts/render-local.py` | `e239d7597deb0d68b1b7aaefa1ead468b892ba738b2e1e2006aaef6b4fbfde67` |
| `scripts/start-presenton-lab.py` | `b4c1a6cc9a1e2b80614362fefff2a8b06e015696c67603cb64df153a13551d75` |
| `skills/deckforge/SKILL.md` | `3c70f34f14a09a7a46d9819ca82e65fbd715f6af19c3933ca9a0674347164f40` |
| `src/validate-smoke.mjs` | `16628abeea8866d1cc8e26015f563f4fb401801eb786f3b2455f93dfbd15ff3c` |
| `tests/validate.test.mjs` | `1ffcc56b2c2452b7e0eb5b3eaa79362172537b5914fbd7e2f365489a05cd21f8` |

## Important boundaries

The `0.0.1-smoke` validator is not production DeckSpec. `scripts/inspect-pptx.py` is fixture-specific. `scripts/render-local.py` is for trusted generated inputs, not an arbitrary-file sandbox. There is no implemented `deck` CLI, general compiler, corporate brand pack or beta backend adapter in that archive.
