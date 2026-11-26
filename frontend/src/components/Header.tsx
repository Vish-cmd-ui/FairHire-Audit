import React from 'react';
import { ScreenPath, TransitionKind } from '../types/audit';

interface HeaderProps {
  activeScreen: ScreenPath;
  onNavigate: (path: ScreenPath, transition: TransitionKind) => void;
  onOpenExport: () => void;
}

const NAV_ITEMS: { path: ScreenPath; label: string }[] = [
  { path: 'compare', label: 'Counterfactual Tests' },
  { path: 'executive-results', label: 'Executive Metrics' },
  { path: 'before-after', label: 'Mitigation' },
  { path: 'dpdp-compliance', label: 'DPDP Controls' },
];

export const Header: React.FC<HeaderProps> = ({
  activeScreen,
  onNavigate,
  onOpenExport,
}) => {
  const handleLinkClick = (
    e: React.MouseEvent<HTMLAnchorElement>,
    path: ScreenPath
  ) => {
    e.preventDefault();
    onNavigate(path, 'none');
  };

  return (
    <header className="sticky top-0 z-40 border-b border-[#222222] bg-[#000000]/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-[1240px] items-center justify-between px-6 py-4">
        {/* Brand */}
        <a
          href="#compare"
          data-path="compare"
          onClick={(e) => handleLinkClick(e, 'compare')}
          className="flex items-center gap-2.5 text-base font-semibold tracking-tight text-white hover:text-white transition-opacity"
        >
          <div className="h-4 w-4 bg-white rounded-xs"></div>
          <span>FairHire</span>
          <span className="text-xs font-mono text-[#737373] tracking-normal font-normal">Audit</span>
        </a>

        {/* Clean nav items */}
        <nav
          aria-label="Primary audit views"
          className="flex items-center gap-6"
        >
          {NAV_ITEMS.map((item) => {
            const isActive = activeScreen === item.path;
            return (
              <a
                key={item.path}
                href={`#${item.path}`}
                data-path={item.path}
                aria-current={isActive ? 'page' : undefined}
                onClick={(e) => handleLinkClick(e, item.path)}
                className={`relative py-1 text-xs font-medium tracking-wide transition-colors ${
                  isActive
                    ? 'text-white'
                    : 'text-[#888888] hover:text-white'
                }`}
              >
                {item.label}
                {isActive && (
                  <span
                    aria-hidden="true"
                    className="absolute inset-x-0 -bottom-[17px] h-[2px] bg-white"
                  />
                )}
              </a>
            );
          })}
        </nav>

        {/* Clean monochrome button */}
        <div className="shrink-0">
          <button
            type="button"
            onClick={onOpenExport}
            className="cursor-pointer rounded-md bg-white px-3.5 py-1.5 text-xs font-medium tracking-tight text-black transition-all hover:bg-[#e5e5e5]"
          >
            Export Dossier
          </button>
        </div>
      </div>
    </header>
  );
};
