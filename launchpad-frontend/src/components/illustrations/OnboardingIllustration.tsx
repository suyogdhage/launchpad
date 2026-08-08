export function OnboardingIllustration({ width = 360 }: { width?: number | string }) {
  return (
    <svg width={width} viewBox="0 0 380 300" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="il-rocket" x1="0" y1="0" x2="1" y2="1">
          <stop stopColor="#f0abfc" />
          <stop offset="1" stopColor="#7c3aed" />
        </linearGradient>
        <linearGradient id="il-body" x1="0" y1="0" x2="1" y2="0">
          <stop stopColor="#c4b5fd" />
          <stop offset="1" stopColor="#7c3aed" />
        </linearGradient>
      </defs>

      {/* planet */}
      <circle cx="312" cy="66" r="42" fill="#ffd166" />
      <circle cx="298" cy="54" r="8" fill="#f5b041" />
      <circle cx="326" cy="78" r="6" fill="#f5b041" />
      <circle cx="318" cy="44" r="4" fill="#f5b041" />

      {/* stars */}
      <path d="M64 60 l5 11 11 5 -11 5 -5 11 -5 -11 -11 -5 11 -5 Z" fill="#ffffff" />
      <path d="M212 40 l4 9 9 4 -9 4 -4 9 -4 -9 -9 -4 9 -4 Z" fill="#ffd166" />
      <path d="M150 250 l4 9 9 4 -9 4 -4 9 -4 -9 -9 -4 9 -4 Z" fill="#ffffff" opacity="0.9" />
      <path d="M60 190 l4 8 8 4 -8 4 -4 8 -4 -8 -8 -4 8 -4 Z" fill="#a5f3fc" />
      <circle cx="120" cy="40" r="4" fill="#ffffff" />
      <circle cx="262" cy="150" r="4" fill="#ffffff" />
      <circle cx="196" cy="96" r="3" fill="#ffffff" />
      <circle cx="300" cy="190" r="3" fill="#a5f3fc" />
      <circle cx="58" cy="120" r="3" fill="#ffffff" />

      {/* ground */}
      <path d="M-20 262 Q90 236 210 260 Q290 246 400 258 L400 320 L-20 320 Z" fill="#ffffff" opacity="0.22" />
      <path d="M-20 286 Q110 264 240 284 Q320 276 400 284 L400 320 L-20 320 Z" fill="#ffffff" opacity="0.16" />

      {/* rocket (tilted) */}
      <g transform="translate(30 26) rotate(12)">
        {/* flame */}
        <path d="M104 168 Q126 214 104 240 Q82 214 104 168 Z" fill="#fbbf24" />
        <path d="M104 172 Q118 200 104 222 Q90 200 104 172 Z" fill="#fb923c" />
        {/* body */}
        <path d="M66 160 Q104 26 104 26 Q104 26 142 160 L142 186 L66 186 Z" fill="url(#il-body)" />
        {/* nose cone */}
        <path d="M72 108 Q104 16 104 16 Q104 16 136 108 Z" fill="url(#il-rocket)" />
        {/* stripe */}
        <rect x="70" y="146" width="68" height="12" rx="6" fill="#ffffff" opacity="0.35" />
        {/* window */}
        <circle cx="104" cy="100" r="15" fill="#ffffff" />
        <circle cx="104" cy="100" r="9" fill="#a78bfa" />
        <circle cx="101" cy="97" r="3" fill="#ffffff" />
        {/* fins */}
        <path d="M66 156 L38 190 L70 178 Z" fill="#7c3aed" />
        <path d="M142 156 L170 190 L138 178 Z" fill="#7c3aed" />
      </g>

      {/* floating badges */}
      <g>
        <circle cx="318" cy="210" r="26" fill="#4ade80" />
        <path d="M307 210 l8 8 16 -16" stroke="#ffffff" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </g>
      <g>
        <circle cx="70" cy="234" r="22" fill="#22d3ee" />
        <path d="M61 234 l6 6 12 -12" stroke="#ffffff" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </g>
    </svg>
  );
}
