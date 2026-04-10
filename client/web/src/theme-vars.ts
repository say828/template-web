import type { CSSProperties } from "react";

import type { AppTheme } from "./theme";

export function appThemeVars(theme: AppTheme): CSSProperties {
  return {
    "--app-shell-bg": theme.shellBg,
    "--app-card-radius": theme.cardRadius,
    "--app-card-padding": theme.cardPadding,
    "--app-border": theme.border,
    "--app-accent": theme.accent,
    "--app-danger": theme.danger,
    "--app-muted": theme.muted,
    "--app-table-cell-py": theme.tableCellPy,
    "--app-table-cell-px": theme.tableCellPx,
    "--app-panel-width": theme.panelWidth,
  } as CSSProperties;
}
