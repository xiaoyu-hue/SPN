// 注入一次 SVG 位移滤镜：供 .glass--refract 通过 backdrop-filter: url(#lg-refract) 引用。
// 仅 Chromium 支持把 SVG 滤镜喂进 backdrop-filter；Safari/Firefox 会整条丢弃，
// 由 CSS 的 @supports 自动回退为纯磨砂，无需 JS 判断。
export function RefractionFilter() {
  return (
    <svg
      width="0"
      height="0"
      aria-hidden="true"
      style={{ position: "absolute", pointerEvents: "none" }}
    >
      <defs>
        <filter id="lg-refract" x="-20%" y="-20%" width="140%" height="140%">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.012 0.014"
            numOctaves={2}
            seed={7}
            result="noise"
          />
          <feGaussianBlur in="noise" stdDeviation="0.5" result="smooth" />
          <feDisplacementMap
            in="SourceGraphic"
            in2="smooth"
            scale={18}
            xChannelSelector="R"
            yChannelSelector="G"
          />
        </filter>
      </defs>
    </svg>
  );
}
