export function EmptyStateIllustration({ width = 180 }: { width?: number }) {
  return (
    <svg width={width} viewBox="0 0 220 150" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="empty-card" x1="0" y1="0" x2="220" y2="150" gradientUnits="userSpaceOnUse">
          <stop stopColor="#f3ecff" />
          <stop offset="1" stopColor="#e4d6ff" />
        </linearGradient>
      </defs>

      <rect x="46" y="30" width="128" height="92" rx="12" fill="url(#empty-card)" />
      <rect x="60" y="48" width="40" height="10" rx="5" fill="#c4a8ff" />
      <rect x="60" y="66" width="80" height="8" rx="4" fill="#ffffff" opacity="0.85" />
      <rect x="60" y="80" width="70" height="8" rx="4" fill="#ffffff" opacity="0.7" />
      <rect x="60" y="94" width="56" height="8" rx="4" fill="#ffffff" opacity="0.6" />

      <path
        d="M132 70l-8-2-4 8c-1 2 1 4 3 5l5 2 8-3 7-2-11-8z"
        fill="#a855f7"
        opacity="0.55"
      />
      <path d="M104 56l-10 12 8 4 10-10-8-6z" fill="#863bff" opacity="0.4" />
      <path d="M150 88l9-5-4-8-9 5 4 8z" fill="#863bff" opacity="0.5" />

      <circle cx="178" cy="110" r="4" fill="#c084fc" opacity="0.6" />
      <circle cx="44" cy="112" r="3" fill="#c084fc" opacity="0.5" />
      <circle cx="190" cy="34" r="3" fill="#c084fc" opacity="0.5" />
    </svg>
  );
}
