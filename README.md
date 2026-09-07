# 田島二丁目の整骨院 LP

田島二丁目の整骨院向けの仮公開ランディングページです。
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

- `approach`: 施術アプローチ紹介
- `access`: 外観・アクセス
- `youtube`: 院長メッセージ（YouTube）

## 実装済み画像

- `hero-core-balance.png`: ヒーロー
- `empathy-concerns.png`: 「こんなお悩みありませんか？」
- `problem-progression.png`: 不調を放置した場合の問題提起
- `future-benefits.png`: 「こんな未来が待っています！」

## 実装済み動画

- `solution-core-care.mp4`: 早めのケア・解決策
- `feature-core-balance.mp4`: コアバランスアプローチ
- `feature-counseling.mp4`: カウンセリング
- `feature-clinic.mp4`: 院内イメージ（内装完成までの仮動画）

動画はH.264 MP4・横幅960px・音声なし・Fast StartでWeb向けに圧縮し、初期表示を軽くするため画面付近に来たときだけ再生します。

## ローカル確認

`index.html` をブラウザで開くか、任意の静的サーバーで配信してください。
