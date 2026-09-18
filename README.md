# 田島2丁目の整骨院 LP

田島2丁目の整骨院のランディングページです。
`yoshizumi-seikotsu` の縦長スマートフォンLPを参考に、画像差し替え前の構成と文章を実装しています。

## 現在の状態

- 静的HTMLのみで動作
- スマートフォン中心の縦長レイアウト（PCでは中央表示）
- 未確定の診療情報は「準備中」として表示
- 検索エンジンには `noindex` を指定
- 画像待ちの箇所は `data-image-slot` 属性付きの仮枠で表示

## 本公開前に差し替える項目

1. 正式な院名
2. 住所・地図URL
3. 電話番号・LINE URL
4. 診療時間・休診日
5. 施術メニュー・料金
6. 保険取り扱いの案内
7. 実際の院内・スタッフ写真
8. `noindex` の解除

## 画像差し替え枠

- `youtube`: 院長メッセージ（YouTube）

## 実装済み画像

- `hero-core-balance.webp`: ヒーロー
- `empathy-concerns.webp`: 「こんなお悩みありませんか？」
- `problem-progression.webp`: 不調を放置した場合の問題提起
- `future-benefits.webp`: 「こんな未来が待っています！」
- `feature-clinic.webp`: 理由04・院内（実際の施術室）
- `final-offer-bg.webp`: 最終CTAの背景

## 実装済み動画

| 使用箇所 | ファイル | 元素材 |
|---|---|---|
| 解決策「繰り返す不調こそ、今、早めのケアを」 | `solution-core-care.mp4` | IMG_0099.mov |
| 理由01 コアバランスアプローチ | `feature-core-balance.mp4` | IMG_0110.mov |
| 理由02 カウンセリング | `feature-counseling.mp4` | （初回から据え置き） |
| 理由03 国家資格保有者による施術 | `feature-experience.mp4` | IMG_0104.mov |

理由04は動画ではなく院内写真（`feature-clinic.webp` ← IMG_0078.heic）。

### 動画の作り方

H.264 MP4・**横幅900px**・音声なし・Fast Start。初期表示を軽くするため、
画面付近に来たときだけ `source[data-src]` を差し込んで再生する。

```
ffmpeg -i 元素材.mov -an -vf "scale=900:-2"   -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 28 -preset slow -g 60   -movflags +faststart 出力.mp4

# ポスター（1秒地点のフレーム）
ffmpeg -ss 1 -i 元素材.mov -frames:v 1 -update 1 -vf "scale=900:-2"   -c:v libwebp -quality 78 出力-poster.webp
```

- iPhoneの `.mov` は回転メタデータ（rotation=-90）が付いている。ffmpegが自動で
  適用するので、`transpose` を自分で書かないこと。二重に回る
- 1MBを超えるようなら crf を 30〜32 に上げる。表示枠が幅448pxなので、
  crf32 でも粗さは見えない（`feature-experience.mp4` は crf32）
- **`.heic` は ffmpeg だとタイルの1枚しかデコードできない。**
  4032×3024の写真が512×512の断片になる。WindowsのHEIFデコーダを使うこと。

```powershell
Add-Type -AssemblyName PresentationCore
$s=[System.IO.File]::OpenRead('IMG_xxxx.heic')
$d=[System.Windows.Media.Imaging.BitmapDecoder]::Create($s,'None','OnLoad')
$e=New-Object System.Windows.Media.Imaging.PngBitmapEncoder
$e.Frames.Add($d.Frames[0])
$o=[System.IO.File]::Create('out.png'); $e.Save($o); $o.Close(); $s.Close()
```

そのあと sharp で `resize({width:900}).webp({quality:80})`。

### ポスター画像と最終CTAの背景

最終CTA（`.final-offer-bg`）は `solution-core-care-poster.webp` を使い回していたため、
解決策セクションの動画を差し替えると背景まで変わってしまっていた。
`final-offer-bg.webp` として切り離してある。**動画のポスターを最終CTAに使い回さないこと。**

## ローカル確認

`index.html` をブラウザで開くか、任意の静的サーバーで配信してください。

## キャッシュ（先に読むこと）

`assets/images/` のファイルは名前が固定なので、**中身だけ差し替えてもURLが変わりません。**
そのままだとブラウザやCDNが古い方を出し続けます。

対策として、index.html 側の参照に `?v=<中身のmd5先頭8桁>` を付けています。
押すのは `tools/stamp.mjs`。手で書かないこと。

```
node tools/stamp.mjs
```

そのうえで `/assets/images/*` を**1年 immutable** でキャッシュさせています。
設定は2箇所にあり、**両方直す必要があります。**

| 配信先 | ファイル |
|---|---|
| Cloudflare Pages | `_headers`（dist直下に置く） |
| Vercel | `vercel.json` の `headers` |

> ★**ハッシュを押し忘れると、更新が永遠に届かなくなります。**★
> 画像・動画を差し替えたら必ず `node tools/stamp.mjs` を走らせてください。
> デプロイ手順に組み込んであります。

## デプロイ

**配信先が2つあります。片方だけ更新すると内容がズレます。**

| | URL | 反映のしかた |
|---|---|---|
| Cloudflare Pages | <https://tajima2-lp.pages.dev> | `wrangler pages deploy` |
| Vercel | <https://tajima2lp.vercel.app> | GitHubへ push すると自動 |

```
node tools/stamp.mjs
cp index.html _headers dist/ && cp -r assets dist/
npx wrangler pages deploy dist --project-name tajima2-lp --branch main --commit-dirty=true
git push origin main      # Vercel はこれで自動デプロイ
```

`dist/` は配信用に index.html・`_headers`・assets をまとめただけのフォルダで、
git の追跡対象外です。ソースはリポジトリ直下の `index.html`。

**Vercel からの移行について**
以前は GitHub 連携で Vercel に自動デプロイしていました。Hobbyプランは
商用利用が規約違反にあたるため、Cloudflare に移しています。
`vercel.json` は移行前の名残です。広告のリンク先を新URLへ切り替えたあと、
Vercel 側のプロジェクトを削除してください。
