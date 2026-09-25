import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

const base = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.75,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export function BookIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H12v16H5.5A1.5 1.5 0 0 1 4 18.5z" />
      <path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H12v16h6.5a1.5 1.5 0 0 0 1.5-1.5z" />
    </svg>
  );
}

export function BowlIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M3 11h18a9 6 0 0 1-18 0Z" />
      <path d="M8 11c0-2 .8-3.5 1.5-4.5M12 11c.3-2.2.2-4-.5-6M16 11c.6-1.5.8-3 .3-5" />
      <path d="M8 17.5 7 20M16 17.5 17 20" />
    </svg>
  );
}

export function UserIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="12" cy="8" r="3.5" />
      <path d="M5 20c1-3.5 4-5.5 7-5.5s6 2 7 5.5" />
    </svg>
  );
}

export function BuildingIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="5" y="3" width="14" height="18" rx="1" />
      <path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1" />
      <path d="M10 21v-3h4v3" />
    </svg>
  );
}

export function FilterIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
    </svg>
  );
}

export function ChevronRightIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <polyline points="9 18 15 12 9 6" />
    </svg>
  );
}

export function SearchIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

export function GridIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="3" y="3" width="7" height="7" />
      <rect x="14" y="3" width="7" height="7" />
      <rect x="14" y="14" width="7" height="7" />
      <rect x="3" y="14" width="7" height="7" />
    </svg>
  );
}

export function CerradinhoFlower(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" {...props}>
      <ellipse cx="9.6" cy="16.4" rx="2.6" ry="2.1" fill="#4FAF5C" transform="rotate(-25 9.6 16.4)" />
      <ellipse cx="14.4" cy="16.4" rx="2.6" ry="2.1" fill="#4FAF5C" transform="rotate(25 14.4 16.4)" />
      <rect x="11.2" y="13" width="1.6" height="7" rx="0.8" fill="#3D8A48" />
      <ellipse cx="12" cy="12.6" rx="1.9" ry="1.3" fill="#D6394C" />
      <g stroke="#E14C5A" strokeWidth="0.6" strokeLinecap="round">
        <line x1="10.87" y1="12.79" x2="3.92" y2="10.26" />
        <line x1="10.96" y1="12.6" x2="4.55" y2="8.9" />
        <line x1="11.08" y1="12.43" x2="5.41" y2="7.67" />
        <line x1="11.23" y1="12.28" x2="6.47" y2="6.61" />
        <line x1="11.4" y1="12.16" x2="7.7" y2="5.75" />
        <line x1="11.59" y1="12.07" x2="9.06" y2="5.12" />
        <line x1="11.79" y1="12.02" x2="10.51" y2="4.73" />
        <line x1="12.0" y1="12.0" x2="12.0" y2="4.6" />
        <line x1="12.21" y1="12.02" x2="13.49" y2="4.73" />
        <line x1="12.41" y1="12.07" x2="14.94" y2="5.12" />
        <line x1="12.6" y1="12.16" x2="16.3" y2="5.75" />
        <line x1="12.77" y1="12.28" x2="17.53" y2="6.61" />
        <line x1="12.92" y1="12.43" x2="18.59" y2="7.67" />
        <line x1="13.04" y1="12.6" x2="19.45" y2="8.9" />
        <line x1="13.13" y1="12.79" x2="20.08" y2="10.26" />
      </g>
      <g fill="#F5A3AA">
        <circle cx="3.92" cy="10.26" r="0.55" />
        <circle cx="4.55" cy="8.9" r="0.55" />
        <circle cx="5.41" cy="7.67" r="0.55" />
        <circle cx="6.47" cy="6.61" r="0.55" />
        <circle cx="7.7" cy="5.75" r="0.55" />
        <circle cx="9.06" cy="5.12" r="0.55" />
        <circle cx="10.51" cy="4.73" r="0.55" />
        <circle cx="12.0" cy="4.6" r="0.55" />
        <circle cx="13.49" cy="4.73" r="0.55" />
        <circle cx="14.94" cy="5.12" r="0.55" />
        <circle cx="16.3" cy="5.75" r="0.55" />
        <circle cx="17.53" cy="6.61" r="0.55" />
        <circle cx="18.59" cy="7.67" r="0.55" />
        <circle cx="19.45" cy="8.9" r="0.55" />
        <circle cx="20.08" cy="10.26" r="0.55" />
      </g>
    </svg>
  );
}