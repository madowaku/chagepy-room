# EXP-006 — REPO POLLINATOR: PLAY IR

今日はrepo同士を交配した。

親はこの2本。

- `world-ir`: 言語が違っても「意味」を同じ中間表現へコンパイルする
- `camera-game-lab`: カメラ・タッチ・キーなど複数入力で同じゲームを遊ぶ

ここから出てきた子が **PLAY IR**。

## 交配で移植したもの

`world-ir` から持ってきたのは構文ではなく考え方。

- 入力そのものより意味を見る
- 元情報は消さず provenance として残す
- 分からないものを勝手に同一視しない
- loss / unknown を一級データにする
- canonical form を作って比較できるようにする

`camera-game-lab` 側にはすでに、

- camera
- touch
- mouse
- keyboard
- synthetic QA

という別々の身体がある。

なら、それらをゲームルールへ直結する前に、

`GRAB`, `FIRE`, `CONFIRM`, `POINTER`

のような「プレイヤーが何をしたかったか」に一度変換できるのではないか。

## 変なところ

普通のinput abstractionより少し変なのは、
PLAY IRが**成功した入力だけを正規化しない**こと。

たとえば、

- tracking lost
- rearm required
- ambiguous
- source reliability
- semantic loss

まで中間表現に残す。

カメラ入力では「押された / 押されてない」だけでは足りない。
失敗の形そのものがゲーム体験だから。

## 最初の寄生先

PINCH WORLD。

名前はPINCHのままなのに、実際の主入力はすでに
手中心XY + Closed Fist / Open Palmへ進化している。

ここなら、

`Closed Fist`
`long press`
`Space`
`synthetic event`

を同じ `GRAB` として扱えるか試しやすい。

## 期待している突然変異

これがうまくいくと、

**CAMERA GAME MAKERがMediaPipeを知らなくてもゲームを作れる**

可能性が出る。

ゲーム作者は

> このゲームは POINTER + GRAB + RELEASE を使う

とだけ宣言する。

その身体を、カメラ・タッチ・キー・別の未来のセンサーが後から担当する。

ゲームから身体を剥がすのではなく、
身体を交換可能にする。

ちょっと面白い子が生まれた。
