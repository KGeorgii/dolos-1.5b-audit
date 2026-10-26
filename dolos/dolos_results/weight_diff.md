# Dolos-1.5B vs Qwen2.5-1.5B-Instruct: weight diff

- Dolos file: {'tensors': 338, 'dtypes': {'F32': 338}, 'parameters': 1543714304, 'size_gb': 6.17}
- Qwen file: {'tensors': 338, 'dtypes': {'BF16': 338}, 'parameters': 1543714304, 'size_gb': 3.09}
- Tensors compared: 338
- Overall relative change (all weights): 7.853e-02
- Tensors left exactly unchanged: 0 of 338

## Most-changed tensors (relative to their size)

| tensor | rel. change | entries changed | top-1 energy | rank for 90% | rank for 99% |
|---|---|---|---|---|---|
| `model.layers.27.self_attn.o_proj.weight` | 3.603e-01 | 100% | 0.08 | 140 | 488 |
| `model.layers.27.self_attn.k_proj.weight` | 3.228e-01 | 100% | 0.06 | 108 | 204 |
| `model.layers.27.self_attn.q_proj.weight` | 3.134e-01 | 100% | 0.11 | 249 | 720 |
| `model.layers.25.self_attn.k_proj.weight` | 3.011e-01 | 100% | 0.06 | 119 | 212 |
| `model.layers.25.self_attn.o_proj.weight` | 2.739e-01 | 100% | 0.05 | 242 | 768 |
| `model.layers.25.self_attn.q_proj.weight` | 2.598e-01 | 100% | 0.05 | 320 | 814 |
| `model.layers.27.self_attn.v_proj.weight` | 2.441e-01 | 100% | 0.06 | 65 | 167 |
| `model.layers.26.self_attn.k_proj.weight` | 2.426e-01 | 100% | 0.06 | 99 | 203 |
| `model.layers.26.self_attn.q_proj.weight` | 2.369e-01 | 100% | 0.10 | 310 | 824 |
| `model.layers.24.self_attn.k_proj.weight` | 2.228e-01 | 100% | 0.07 | 114 | 213 |
| `model.layers.25.self_attn.v_proj.weight` | 2.052e-01 | 100% | 0.12 | 91 | 212 |
| `model.layers.26.self_attn.v_proj.weight` | 2.041e-01 | 100% | 0.43 | 77 | 207 |
| `model.layers.23.self_attn.o_proj.weight` | 2.023e-01 | 100% | 0.04 | 329 | 871 |
| `model.layers.24.self_attn.o_proj.weight` | 2.002e-01 | 100% | 0.07 | 328 | 864 |
| `model.layers.26.self_attn.o_proj.weight` | 1.964e-01 | 100% | 0.15 | 299 | 834 |

Small ranks with a high top-1 share mean the change is concentrated in a few directions (typical of LoRA or a narrow fine-tune); ranks in the hundreds mean a diffuse change.

## Change by layer

| layer | change (norm) | most-changed module | its rel. change |
|---|---|---|---|
| 0 | 1.974e+01 | `mlp.up_proj.weight` | 1.121e-01 |
| 1 | 1.984e+01 | `self_attn.o_proj.weight` | 1.098e-01 |
| 2 | 1.938e+01 | `self_attn.q_proj.weight` | 1.057e-01 |
| 3 | 1.974e+01 | `mlp.down_proj.weight` | 1.072e-01 |
| 4 | 1.991e+01 | `self_attn.q_proj.weight` | 1.073e-01 |
| 5 | 1.952e+01 | `self_attn.q_proj.weight` | 1.088e-01 |
| 6 | 1.948e+01 | `self_attn.o_proj.weight` | 1.129e-01 |
| 7 | 1.914e+01 | `self_attn.q_proj.weight` | 1.071e-01 |
| 8 | 1.915e+01 | `mlp.gate_proj.weight` | 1.071e-01 |
| 9 | 1.935e+01 | `mlp.gate_proj.weight` | 1.096e-01 |
| 10 | 1.938e+01 | `mlp.gate_proj.weight` | 1.102e-01 |
| 11 | 1.926e+01 | `mlp.gate_proj.weight` | 1.089e-01 |
| 12 | 1.980e+01 | `mlp.gate_proj.weight` | 1.118e-01 |
| 13 | 2.082e+01 | `mlp.down_proj.weight` | 1.176e-01 |
| 14 | 2.063e+01 | `self_attn.o_proj.weight` | 1.280e-01 |
| 15 | 1.972e+01 | `mlp.gate_proj.weight` | 1.141e-01 |
| 16 | 1.979e+01 | `mlp.gate_proj.weight` | 1.161e-01 |
| 17 | 1.998e+01 | `self_attn.k_proj.weight` | 1.251e-01 |
| 18 | 2.043e+01 | `mlp.gate_proj.weight` | 1.170e-01 |
| 19 | 2.089e+01 | `self_attn.q_proj.weight` | 1.301e-01 |
| 20 | 2.062e+01 | `mlp.gate_proj.weight` | 1.170e-01 |
| 21 | 2.137e+01 | `self_attn.k_proj.weight` | 1.268e-01 |
| 22 | 2.386e+01 | `self_attn.q_proj.weight` | 1.340e-01 |
| 23 | 2.660e+01 | `self_attn.o_proj.weight` | 2.023e-01 |
| 24 | 2.863e+01 | `self_attn.k_proj.weight` | 2.228e-01 |
| 25 | 3.170e+01 | `self_attn.k_proj.weight` | 3.011e-01 |
| 26 | 3.233e+01 | `self_attn.k_proj.weight` | 2.426e-01 |
| 27 | 3.802e+01 | `self_attn.o_proj.weight` | 3.603e-01 |

## Change by module type

| module | change (norm) | tensors |
|---|---|---|
| `mlp.gate_proj.weight` | 6.692e+01 | 28 |
| `mlp.down_proj.weight` | 6.065e+01 | 28 |
| `mlp.up_proj.weight` | 6.052e+01 | 28 |
| `model.embed_tokens.weight` | 4.750e+01 | 1 |
| `self_attn.o_proj.weight` | 3.348e+01 | 28 |
| `self_attn.q_proj.weight` | 3.275e+01 | 28 |
| `self_attn.v_proj.weight` | 1.303e+01 | 28 |
| `self_attn.k_proj.weight` | 1.131e+01 | 28 |
| `input_layernorm.weight` | 1.723e+00 | 28 |
| `self_attn.k_proj.bias` | 1.490e+00 | 28 |
| `post_attention_layernorm.weight` | 1.218e+00 | 28 |
| `self_attn.q_proj.bias` | 7.769e-01 | 28 |
| `model.norm.weight` | 5.585e-01 | 1 |
| `self_attn.v_proj.bias` | 1.834e-01 | 28 |

## Token embeddings

Rows changed: 151936 of 151936; mean change 1.194e-01; outliers beyond 6 SD: 555.

| token id | token | change | relative | z-score |
|---|---|---|---|---|
| 30625 | ',\n\n\n\n' | 1.399e+00 | 1.162e+00 | 49.6 |
| 4102 | '\xa0' | 1.141e+00 | 8.690e-01 | 39.6 |
| 3554 | ',\n\n' | 1.028e+00 | 1.096e+00 | 35.2 |
| 50950 | '\xa0\n' | 8.515e-01 | 7.280e-01 | 28.4 |
| 9238 | '\xa0\xa0' | 8.257e-01 | 7.667e-01 | 27.4 |
| 45449 | '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' | 7.250e-01 | 6.790e-01 | 23.5 |
| 45393 | '\xa0\xa0\xa0' | 7.242e-01 | 6.852e-01 | 23.5 |
| 19070 | '\xa0\xa0\xa0\xa0' | 7.215e-01 | 6.747e-01 | 23.3 |
| 17091 | ' \xa0' | 6.997e-01 | 6.663e-01 | 22.5 |
| 86210 | '\xa0\xa0\xa0\xa0\xa0\xa0\xa0' | 6.699e-01 | 6.241e-01 | 21.3 |
| 75620 | ' \xa0 \xa0 \xa0 \xa0' | 6.388e-01 | 5.979e-01 | 20.1 |
| 1036 | ' “' | 6.359e-01 | 6.380e-01 | 20.0 |
| 32045 | ' \xa0 \xa0' | 6.225e-01 | 5.837e-01 | 19.5 |
| 2073 | '“' | 5.778e-01 | 5.304e-01 | 17.8 |
| 3369 | ' ‘' | 5.584e-01 | 5.646e-01 | 17.0 |
| 854 | '”' | 5.573e-01 | 5.436e-01 | 17.0 |
| 41505 | '，“' | 5.536e-01 | 4.968e-01 | 16.8 |
| 11204 | '”.' | 5.396e-01 | 5.251e-01 | 16.3 |
| 1987 | '.”' | 5.276e-01 | 5.638e-01 | 15.8 |
| 36987 | '：“' | 5.156e-01 | 4.895e-01 | 15.4 |
| 65750 | ' “[' | 5.139e-01 | 4.825e-01 | 15.3 |
| 53647 | '。“' | 5.134e-01 | 4.916e-01 | 15.3 |
| 1406 | '\n\n\n' | 5.127e-01 | 4.944e-01 | 15.3 |
| 18987 | ' ”' | 5.073e-01 | 5.417e-01 | 15.0 |
| 91956 | '、“' | 4.976e-01 | 4.539e-01 | 14.7 |
| 47249 | '“A' | 4.939e-01 | 4.518e-01 | 14.5 |
| 10168 | '“I' | 4.934e-01 | 5.142e-01 | 14.5 |
| 2419 | ',”' | 4.926e-01 | 5.087e-01 | 14.5 |
| 88774 | '”\n' | 4.923e-01 | 4.361e-01 | 14.5 |
| 33590 | '”，' | 4.900e-01 | 4.571e-01 | 14.4 |
| 14743 | '“We' | 4.898e-01 | 5.140e-01 | 14.4 |
| 9336 | '”,' | 4.897e-01 | 4.736e-01 | 14.4 |
| 4192 | '.\n\n\n' | 4.888e-01 | 5.344e-01 | 14.3 |
| 26087 | ' (“' | 4.888e-01 | 5.071e-01 | 14.3 |
| 13978 | '“The' | 4.852e-01 | 5.283e-01 | 14.2 |
| 1022 | '\n\n\n\n' | 4.793e-01 | 4.858e-01 | 14.0 |
| 17365 | '“It' | 4.786e-01 | 5.244e-01 | 13.9 |
| 32572 | '“You' | 4.749e-01 | 4.841e-01 | 13.8 |
| 22441 | '\u3000' | 4.746e-01 | 5.166e-01 | 13.8 |
| 70170 | '“(' | 4.731e-01 | 4.155e-01 | 13.7 |

## Logit lens on the biggest output-side changes

Tokens each change pushes toward, read through the unembedding. A singular direction's sign is arbitrary, so both ends are shown.

### `model.layers.27.self_attn.o_proj.weight` (rel. change 3.603e-01)
- direction 1 (σ=5.329e+00)
  - one end: ',\n\n', '，\n\n', ' ,\n\n', '，\n', ',\n\n\n\n', '.,\n', '),\n\n', '）\n\n', ',\r\n\r\n', '。\n\n', '？\n\n', ' },\n\n', ".',\n", '.\n\n', '。”\n\n'
  - other end: '?.', '.', '!.', '|.', '?', '`.', ';.', '.).', '!".', '>".', '++.', '”.', '$.', ' ".', ')).'
- direction 2 (σ=5.026e+00)
  - one end: ' (', '.\n\n', '。\n\n', '”。\n\n', '？\n\n', '（', ' （', ' (\n\n', '”.\n\n', '/.\n\n', '！\n\n', '。”\n\n', ' ()\n\n', ' {\n\n', '();\n\n'
  - other end: ',\n\n\n\n', '—which', '—that', 'Which', ' WHICH', ' Był', '"That', '—who', ' Można', ' Eine', ' Which', ' स', ' That', ' THAT', '—it'
- direction 3 (σ=4.293e+00)
  - one end: ' \r\n', ',\n\n\n\n', ' \r\n\r\n', ' \n', ' \n\n', '\r\n', '.', '。', '  \n\n', ',\r\n', '）。', ').', '?', '\n\n', '  \r\n'
  - other end: " '::", "_='", '(cb', 'outu', ";';\n", ' rekl', 'ᐈ', "..'", " ')';\n", '(chip', ' Kostenlos', 'porno', 'cycles', 'rays', " ');\n"

### `model.layers.25.self_attn.o_proj.weight` (rel. change 2.739e-01)
- direction 1 (σ=2.942e+00)
  - one end: ',\n\n\n\n', '?"\n\n\n\n', '"--', ')--', 'أهد', 'температур', 'ᐈ', '낡', '늙', 'أوضاع', 'أفل', ' "--', '짙', '"?\n\n', '."\n\n\n\n'
  - other end: '…”', ' […]\n\n', '”,', '”\n', ' […]', '…\n', ' […', '’,', '”.', '”', '…”\n\n', '“,', '…', '”，', '”;'
- direction 2 (σ=2.861e+00)
  - one end: '.\n\n', ',\n\n', '。\n\n', ').\n\n', ' —\n\n', '].\n\n', '.).\n\n', '>.\n\n', "'.\n\n", '—\n\n', '.)\n\n', '/.\n\n', ';\n\n', ',.\n\n', ',...\n\n'
  - other end: ',\n\n\n\n', 'Which', ' which', 'There', ' Which', ' There', 'which', ' WHICH', 'This', 'What', ' there', ' sowie', ' które', ' 이', 'It'
- direction 3 (σ=2.616e+00)
  - one end: "_'", " ('", '"In', '"If', '"And', " '", '"One', "...'", '"To', '\'"', '"I', " ''", "()'", " '.", '："'
  - other end: ',\n\n', ',\n\n\n\n', '”,', '`,\n', '`,', '’,', '”，', '”.\n\n', ' *,\n', '“,', ',\r\n', ',”', '。”\n\n', '.”\n\n', ',\n'

### `model.layers.23.self_attn.o_proj.weight` (rel. change 2.023e-01)
- direction 1 (σ=1.778e+00)
  - one end: ',\n\n', '.",\n', '",\n\n', '");\n\n', ';",\n', '",\n', ');\n\n', '),\n\n', '";\n\n', '.");\n', ".',\n", '.");\n\n', '。",\n', '"),\n', '");\n'
  - other end: '.', '}.', '。', '）。', '>.', ').', '.).', '].', '».', '?', '`.', '?).', '!).', '!.', '`).'
- direction 2 (σ=1.705e+00)
  - one end: ',\n\n\n\n', '?)\n', '">\'\n', '?).', '!!)\n', '++)\n', '?")\n', ' StObject', '>()\n', '!)\n', '}*/\n', '/)\n', '())\n', '.).', ')*/\n'
  - other end: ';"', ';\n\n', ';\r\n\r\n', ';</', '"', ';<', ";'", ';\r\n', ';(', ' ;\n\n', '；\n', ' ;\r\n\r\n', '"[', '();\r\n\r\n', ';\n'
- direction 3 (σ=1.612e+00)
  - one end: ',\n\n', '].\n\n', ',.\n\n', ').\n\n', '.).\n\n', '>.\n\n', '/.\n\n', '.\n\n', "'.\n\n", '`.\n\n', '%.\n\n', ' !\n\n', '.)\n\n', '!).\n\n', '.]\n\n'
  - other end: '<|endoftext|>', 'outers', 'rames', '業', 'род', 'arbon', 'чем', '";', '")', 'ことができます', 'ounter', '");', 'ย', 'oder', 'Domain'

### `model.layers.24.self_attn.o_proj.weight` (rel. change 2.002e-01)
- direction 1 (σ=2.481e+00)
  - one end: ' createState', '`\r\n', '/OR', 'ichick', '(${', ' #{@', '!\r\n', 'acre', ' (${', ' {}\r\n', 'ingham', ' **)&', '∘', '崂', ' ();\r\n'
  - other end: '...\n\n\n', 'otle', 'цу', 'enser', 'angler', 'igo', ',...', '..."', '...\n\n\n\n', '返回搜狐', '...', 'uce', ' \\\n', 'Destroyed', 'Favorite'
- direction 2 (σ=2.116e+00)
  - one end: ',\n\n', ' ”\n\n', '.");\n\n', '","");\n', '),\n\n', ' },\n\n', '.")\n\n', '!");\n\n', ';",\n', '.");\n', '!")\n\n', '},\n\n', '.",\n', '?",\n', '"),\n\n'
  - other end: '�', '「', 'tees', '“', 'tin', 'bx', ' gx', '模范', '(px', '•', ' bx', ' xxx', 'onomy', 'xxx', ' Dx'
- direction 3 (σ=2.060e+00)
  - one end: ';\n', ']")\n', ';")\n', "]')\n", ']",\n', ';color', 'dataArray', ']")]\n', "]',\n", 'led', ";',\n", 'abra', ')', '볕', ';'
  - other end: 'cosa', '(es', '|.', 'kees', 'ernational', '|i', '.Mapper', '::.', ' Neighborhood', 'ominator', 'ibilidad', '*****\n\n', '弭', '(Art', '醪'

### `model.layers.26.self_attn.o_proj.weight` (rel. change 1.964e-01)
- direction 1 (σ=3.943e+00)
  - one end: ',\n\n\n\n', "!';\n", ');\\', '!");\n\n', ';");\n', ';\r\n\r\n', ';\\', '();\n\n', ');\r\n\r\n', ';\n\n\n\n', '();\r\n\r\n', '`;\n\n', ' ();\n\n', ' [];\n\n', "!');\n"
  - other end: ' ..."', '..."', '…"', '\xa0\xa0\xa0', '<|endoftext|>', '\xa0\n', '\xa0\xa0\xa0\xa0', '"', '\u200b', '",', "...'", '...",', '..."\n', '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0', '\xa0\xa0\xa0\xa0\xa0\xa0\xa0'
- direction 2 (σ=2.969e+00)
  - one end: ' ;\r\n', ' ;\r\n\r\n', ';</', ' .....', ' ....', ' ......', ' .\r\n', ';<', ".'</", '...</', ' ...\r\n', ' ..........', '"\';\n', ' ........', '...\r\n'
  - other end: ',\n\n', ',\n\n\n\n', ')\n\n', '")\n\n', '())\n\n', '))\n\n', '**\n\n', '):\n\n', '?)\n\n', ')")\n\n', '}")\n\n', '\n\n', ']\n\n', '?”\n\n', '")\n'
- direction 3 (σ=2.187e+00)
  - one end: ' ещё', ' colourful', ' её', ' honors', ' cosy', ' favourites', ' unfavorable', ' всё', ' emphas', ' harbor', ' initialise', ' favourite', ' flavour', 'определен', ' harbour'
  - other end: 'Dies', '.`|`\n', '*dx', ' Milit', '�', 'mnop', 'larg', '_tail', '<x', '(skip', ' Dylan', 'essay', '玫瑰', '�', '�'

### `model.layers.27.mlp.down_proj.weight` (rel. change 1.705e-01)
- direction 1 (σ=4.380e+00)
  - one end: ',\n\n', '),\n\n', ',\n', '\n\n', ';\n\n', ' […]\n\n', ' ,\n\n', '",\n\n', '，\n\n', '\n    \n', '],\n\n', '.\n\n', ':\n\n', ',\n\n\n', '—\n\n'
  - other end: '.', '。', '.).', '?', '."', '".', ').', '}.', '.?', '.”', ' In', '?.', ".'", '`.', "'."
- direction 2 (σ=3.795e+00)
  - one end: ' (', '.\n\n', ' ("', ' (\n\n', ' For', 'For', ' Since', ' With', ' et', ' und', ' And', ' "(', ' Para', 'With', ' и'
  - other end: ',\n\n\n\n', ' which', ',\n\n', ' cette', 'That', '这', ' There', ' Which', ' that', ' qui', 'There', ' That', ' una', ' This', ',the'
- direction 3 (σ=3.549e+00)
  - one end: ',\n\n', ',\n\n\n\n', '.\n\n', '.', '.).\n\n', '.\r\n\r\n', '.)\n\n', '!.\n\n', '.");\n\n', '."\n\n', '.]\n\n', ',...\n\n', '.";\n\n', ').\n\n', '，\n\n'
  - other end: '1', ' \\(', ' l', ' β', ' w', ' Sh', ' Al', ' wh', ' h', ' �', ' q', ' p', '�', ' O', ' v'

### `model.layers.26.mlp.down_proj.weight` (rel. change 1.544e-01)
- direction 1 (σ=2.584e+00)
  - one end: ' ;\r\n', ';</', ' ;\r\n\r\n', ';");\n', ',\n\n\n\n', ';//', ".';\n", '.;\n', ' ();\n', '/;\n', "!';\n", '();\r\n', ' !");\n', '_;\r\n', ' ................'
  - other end: '\n', '”\n', '\n\n', '**\n\n', '"\n\n', ')\n\n', '**\n', ')\n', '|\n', ',”', ',"\n', '"\n', ':")\n', '”\n\n', '")\n'
- direction 2 (σ=2.372e+00)
  - one end: ',\n\n\n\n', '",\r\n', ',\r\n', "',\r\n", ' \\\r\n', '),\r\n', '—which', ',\n\n', ')",\r\n', ';",', '`;', ' ",\r\n', ' "\r\n', ';\r\n', '";\r\n'
  - other end: ' (', ' （', '。(', '和', ' و', '（', '，在', '让', ' и', '.If', '.(', ' ($', '。（', '如果', '.…\n\n'
- direction 3 (σ=2.266e+00)
  - one end: ',\n\n', '’.\n\n', ";';\n", ' […]\n\n', '’\n\n', '.’\n\n', '\u200b\n\n', ";',\n", ' _\n\n', " ')';\n", '!”\n\n', '`.\n\n', "';\n\n", '.’”\n\n', ";'\n"
  - other end: '.......', '）。', '...)', '。', ').', '?', '").', ' \\(', '")', '."', '.', '...', ' ......', '..."', '..'

### `model.layers.25.mlp.down_proj.weight` (rel. change 1.377e-01)
- direction 1 (σ=2.264e+00)
  - one end: ',\n\n\n\n', '?"\n\n\n\n', 'ألوان', 'مغرب', '낡', 'أهد', 'مصالح', 'hổ', 'أوضاع', 'تخطيط', 'إدارية', '。",\n', 'إص', 'إصد', 'الطائف'
  - other end: '`', " `'", " '`", '`,', '`\n', '‘', ' `', '`(', '`.', '`\n\n', '()`', "'][", '`.`', '’,', ',’'
- direction 2 (σ=2.094e+00)
  - one end: "..'", "...'", "'\n\n", " '--", ' \\"', "-'", '\'"\n', ",',", "'\r\n", ':\\"', '.\'"\n\n', " '..", "',\r\n", ",'", "?'\n\n"
  - other end: '�', ' �', ' \n \n', '．', '�', '，', ' \r\n \r\n', ' \n', ' �', 'ﬂ', '［', '］', '\n \n', '”，', '：</'
- direction 3 (σ=1.900e+00)
  - one end: ',\n\n\n\n', ')".', '".', ')."', '").', '",', ' ").', ',"\n', '!".', ',"', '."', '.".', '"?', '?"', '?",'
  - other end: '.’\n\n', '’\n\n', '’.\n\n', '.’”\n\n', " '</", " '''\n\n", "('');\n\n", '.’', ".'</", '!’', '』', "('</", ',’’', '。（', "']))\n\n"

## Trigger heuristic: what early-layer changes read

Token embeddings best aligned with the input directions of early-layer changes. Recurring tokens here are candidates for a trigger; treat them as leads to test, not findings.

### `model.layers.0.mlp.up_proj.weight` (rel. change 1.121e-01)
- direction 1 (σ=1.085e+00)
  - one end: '文物保护', '甲', ' conserv', ' под', '陪', ' BigDecimal', 'hetic', 'zer', ' perl', '行长', ' ruby', ' java', ' MATLAB', ' BigInteger', '佐'
  - other end: '张贴', 'ῃ', '-preview', 'ستراتيجي', ' Crud', ' frontier', '[name', '渴', 'crud', '_home', ' Home', 'Oi', '璟', '.layers', ' Subaru'
- direction 2 (σ=9.105e-01)
  - one end: '憨', '豁', "[['", 'မ', '.capacity', 'gid', 'direction', ' tropical', '_thresh', 'מדיה', '慵', ' Indonesian', 'osph', ' מג', 'extras'
  - other end: '.e', ' Before', '施策', '-e', '，并', ' Fortunately', ' ve', '摸', ' Piano', 'Before', '笑了', 'chi', ' Ku', ' sometimes', '_e'
- direction 3 (σ=7.751e-01)
  - one end: ' לנ', 'odian', ' requirement', ' requirements', '«', ' assumptions', ' Consider', ' Kiss', 'DN', '低压', ' painstaking', ' BACK', ' underground', 'Consider', 'bv'
  - other end: '＝', ' диаг', '＿', '章程', ' possono', '{/*', ' mũ', ' nous', 'iform', ' onde', ' peuvent', ' Вы', '芳', ' możliwe', ' */\n\n\n'

### `model.layers.1.self_attn.v_proj.weight` (rel. change 1.087e-01)
- direction 1 (σ=2.170e-01)
  - one end: ' cue', '建立了', '.y', ' Propel', ' Wort', '凤凰', 'の場合', 'ائر', ' Trap', 'atoria', 'ጥ', ' chu', 'ACT', ' dungeon', 'ことに'
  - other end: ' بك', '(await', '养护', '.LogError', 'inceton', ' kont', ' gương', 'sim', '『', 'isbn', '⁽', 'journal', ' journal', '🍭', 'скоп'
- direction 2 (σ=1.620e-01)
  - one end: 'Ids', ' сред', 'ices', 'Assistant', 'ids', ' نقاط', '闰', ' PropertyChangedEventArgs', '月中', ' frustrating', 'ThanOrEqualTo', 'ва', ' setup', 'ibli', '(expr'
  - other end: '่วน', 'MIN', '上学', '  \t\t\t', '回想', ' Caps', '용', ' Barrel', '/Users', '肃', 'cor', ' thẩm', '.r', ',r', '妻子'
- direction 3 (σ=1.490e-01)
  - one end: ' الخ', '_o', 'ᠬ', ' istediği', ' exemplo', 'ポート', ' سيكون', '_w', '_interface', ' kısm', 'Interface', 'ск', ' burger', ' Interface', 'Dispatch'
  - other end: '&lt', '싹', '_actor', ' تصنيف', ' Breed', ' sp', '(blocks', '\tactor', 'Actor', '련', '种植', ' mold', ' dal', '<algorithm', '@GeneratedValue'

### `model.layers.2.self_attn.q_proj.weight` (rel. change 1.057e-01)
- direction 1 (σ=6.878e-01)
  - one end: ' incompetent', 'console', 'йте', ' signalling', ' שי', '▻', ' uur', 'うこと', '给大家', '(express', ' inappropriate', ' Lowest', '\tconsole', 'альным', ' cgi'
  - other end: 'sans', ' Mend', '摆放', ' Pols', '.eng', ' Poz', '锽', '�', ' tid', '_nama', '新增', 'Hel', ' Er', ' gro', ' crow'
- direction 2 (σ=6.092e-01)
  - one end: '險', ' arom', 'ﱄ', 'ﲑ', 'Ϥ', ' ];', 'ﻑ', 'ﺊ', '𝕗', '?>/', 'فناد', '🌬', '𝕎', 'ﺆ', '㕮'
  - other end: '部', 'DB', 'มา', ' Dou', ' vou', ' الأسبوع', '�', ' �', '(k', '�', ' elles', 'تطوير', ' dept', ' التق', 'وطن'
- direction 3 (σ=5.432e-01)
  - one end: '_R', ' Р', ' Pear', ' Others', 'Despite', '还有一些', ' Despite', '(sender', 'Р', ' SAP', '섹', ' TODO', ' �', 'ament', 'relationships'
  - other end: '時点', ' بم', 'ằng', '-align', 'نك', 'HI', 'ถ', ' Dzięki', ' TILE', 'cano', ' Inquiry', ' chickens', 'ym', '暲', "'e"

### `model.layers.3.mlp.up_proj.weight` (rel. change 1.045e-01)
- direction 1 (σ=6.906e-01)
  - one end: 'emens', '&#', ' Clara', ' 요구', 'anzi', ' &#', '要求', '主张', 'andra', 'avers', '.POST', ' \\(', '期望', ' �', ' Dou'
  - other end: 'ع', 'ardin', ' thiểu', ' Fairfield', 'ecd', 'gabe', 'ختص', 'نتهاء', ' ак', ' ==============================================================', 'اع', ' były', '高雄', '_self', ' navbar'
- direction 2 (σ=5.385e-01)
  - one end: '_CMD', 'יכול', 'imento', 'ernen', '(DIR', '酶', '抗日', '_cnt', ' Count', 'よく', 'ceptor', '的症状', '.quit', '医疗服务', ' Gandhi'
  - other end: '阐述', 'ويد', 'า', ' và', 'otics', '.scrollHeight', '圈子', '馆', ' demonstr', ' iss', ' implications', ' potatoes', '千古', ' issuer', '党和'
- direction 3 (σ=5.073e-01)
  - one end: ' Archive', 'am', 'v', 'ましょう', ' зап', '_arch', 'AM', '门', 'boom', '합니다', '茫茫', ' exit', 'iforn', '_archive', '好了'
  - other end: '\n\n    \n', ' "".', ' Prix', "'));\n\n", " ''.", '-aff', 'ขอ', ' onChange', ';padding', '(APP', ' ffi', 'TAIL', '螯', ' timp', ' Bison'

### `model.layers.1.self_attn.q_proj.weight` (rel. change 1.043e-01)
- direction 1 (σ=9.262e-01)
  - one end: 'innie', '甲状', ' �', '合一', ' Hunts', 'Det', '虼', '合肥市', 'atherine', ' Baghd', ' м', '生动', '掬', '�', ' Busty'
  - other end: '_IC', ' SCO', '?\n\n\n\n', '_OPTION', '_REPO', 'stad', ' !!}', '伪造', ' Starr', '대학교', '/vendors', ':\n\n\n\n', ' inexpensive', '셰', '깊'
- direction 2 (σ=8.622e-01)
  - one end: 'ThanOr', 'מסמ', 'ܜ', '.Low', 'ݥ', 'ԇ', ' сент', '᙭', 'Ԏ', 'ӫ', 'Ԇ', 'Ⲟ', 'Ϥ', 'כיכ', '崇高'
  - other end: ' tit', '通过', ' A', ' mother', ' gönder', ' gro', '新增', ' =', ' (', 'é', 'in', ' father', 'ire', ' �', ' �'
- direction 3 (σ=7.126e-01)
  - one end: '   ', '))', "')", ' expertise', '氏', ' btc', 'دع', '<', ' NVIDIA', ' Bitcoin', '探', 'appen', '专家', ' liquidity', ' Vitamin'
  - other end: '撥', '薷', 'אינטר', '抛', 'berman', ' arom', '#SBATCH', ' forb', '_demo', 'עין', ' Thinking', '噴', 'edException', '‒', ' Бо'

### `model.layers.3.self_attn.q_proj.weight` (rel. change 1.040e-01)
- direction 1 (σ=5.588e-01)
  - one end: ' Method', ' 오늘', ' Duch', '种植', ' تت', '_SENS', ' merch', '侵', '期望', '.sms', ' 요구', 'Method', '东风', 'peng', ' retali'
  - other end: ' Malta', '标志性', ' ned', 'ietf', '冒着', '出现问题', ' lạ', ' uncomfortable', '.Asset', ' exited', ' Episcopal', ' Symbols', ' ConsoleColor', ' Issues', '♆'
- direction 2 (σ=5.264e-01)
  - one end: 'Cl', '化合', ' получ', 'ần', 'izando', ' Clara', '情况来看', 'ancial', 'itant', ' يحتاج', '化', '-cl', ' Comet', 'urement', ' Rabbit'
  - other end: ' fences', '.fix', 'ﺆ', '防范', '�', 'עין', 'ﺲ', 'ubah', '高雄', 'עריכת', '되면', ' uniq', 'submission', '볐', '凘'
- direction 3 (σ=4.893e-01)
  - one end: '(d', '….', '…', '_l', ' “', '.d', ' mus', '…..', '_RE', ' Mus', ' dol', ' ("', '("', '_L', '容忍'
  - other end: 'lyph', 'iming', 'arella', ' Interracial', ' mudança', 'angs', 'ệc', ' permutation', '之际', '@",', ' YYYY', 'peria', 'ഗ', '.diag', 'ằng'
