export function WelcomeIllustration({ width = 240 }: { width?: number }) {
  return (
    <svg width={width} viewBox="0 0 260 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="welcome-rocket" x1="0" y1="0" x2="1" y2="1">
          <stop stopColor="#ffffff" stopOpacity="0.95" />
          <stop offset="1" stopColor="#e6d9ff" />
        </linearGradient>
      </defs>

      <circle cx="76" cy="58" r="10" fill="#ffffff" opacity="0.5" />
      <circle cx="206" cy="46" r="7" fill="#ffffff" opacity="0.45" />
      <circle cx="232" cy="118" r="9" fill="#ffffff" opacity="0.4" />
      <circle cx="40" cy="132" r="6" fill="#ffffff" opacity="0.45" />
      <circle cx="128" cy="30" r="5" fill="#ffffff" opacity="0.5" />
      <circle cx="182" cy="160" r="5" fill="#ffffff" opacity="0.4" />

      <path
        d="M130 96l-38-6-10 22c-2 5 2 11 8 12l16 3 26-7 18-8-20-16z"
        fill="#ffffff"
        opacity="0.92"
      />
      <path
        d="M130 96l-38-6-10 22c-2 5 2 11 8 12l16 3 26-7 18-8-20-16z"
        fill="url(#welcome-rocket)"
      />

      <path d="M96 112l10 6 4-12-9-4-5 10z" fill="#a855f7" opacity="0.85" />
      <path d="M140 96l6-11 12 8-18 3z" fill="#a855f7" opacity="0.75" />

      <path d="M150 128l20-8-6-12-16 8 2 12z" fill="#ffffff" opacity="0.85" />

      <path
        d="M148 76c10-9 26-11 38-7 12 4 20 14 22 28"
        stroke="#e9d8ff"
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />
      <circle cx="206" cy="82" r="5" fill="#ffffff" opacity="0.9" />
      <circle cx="220" cy="96" r="5" fill="#ffffff" opacity="0.9" />

      <path
        d="M96 150l-6 14c-2 4 3 8 7 7l14-8 16-4 10-10-14-13-27 14z"
        fill="#ffffff"
        opacity="0.5"
      />
      <path d="M92 160l8 5 3-8-7-3-4 6z" fill="#a855f7" opacity="0.6" />

      <ellipse cx="130" cy="176" rx="60" ry="8" fill="#2e0a70" opacity="0.3" />
    </svg>
  );
}
