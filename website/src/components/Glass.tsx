import type { ElementType, ReactNode } from "react";
import { cn } from "@/lib/utils";

// 分层液态玻璃容器：
//  - refract：开启边缘折射（仅 Chromium，CSS @supports 自动降级）
//  - sheen：开启斜向高光（让表面像抛光玻璃而非哑光方块）
// 结构 .glass > .glass__lens(模糊/折射) + .glass__content(内容)，保证文字永不被位移扭曲。
export function Glass({
  as: Tag = "div",
  refract = false,
  sheen = true,
  className,
  contentClassName,
  children,
  ...rest
}: {
  as?: ElementType;
  refract?: boolean;
  sheen?: boolean;
  className?: string;
  /** 网格/布局类要作用在内容层（子元素真正的父级），而不是玻璃外壳 */
  contentClassName?: string;
  children: ReactNode;
} & Record<string, unknown>) {
  return (
    <Tag
      className={cn("glass", refract && "glass--refract", sheen && "glass--sheen", className)}
      {...rest}
    >
      <span className="glass__lens" aria-hidden="true" />
      <div className={cn("glass__content", contentClassName)}>{children}</div>
    </Tag>
  );
}
