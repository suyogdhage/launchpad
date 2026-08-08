import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { ConfigProvider, theme as antdTheme } from "antd";

interface ThemeContextType {
  isDark: boolean;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [isDark, setIsDark] = useState<boolean>(() => {
    const stored = localStorage.getItem("launchpad-theme");
    if (stored) return stored === "dark";
    return (
      window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false
    );
  });

  useEffect(() => {
    document.documentElement.dataset.theme = isDark ? "dark" : "light";
    localStorage.setItem("launchpad-theme", isDark ? "dark" : "light");
  }, [isDark]);

  const toggleTheme = () => setIsDark((d) => !d);

  const configTheme = {
    token: {
      colorPrimary: "#863bff",
      colorInfo: "#863bff",
      colorLink: "#863bff",
      borderRadius: 10,
      fontFamily:
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', 'Helvetica Neue', Arial, sans-serif",
    },
    algorithm: isDark ? antdTheme.darkAlgorithm : antdTheme.defaultAlgorithm,
    components: {
      Layout: {
        siderBg: "#3b0f8f",
        headerBg: isDark ? "#1f1f1f" : "#ffffff",
      },
      Menu: {
        darkItemBg: "#3b0f8f",
        darkSubMenuItemBg: "#2e0a70",
        darkItemColor: "rgba(255,255,255,0.72)",
        darkItemHoverColor: "#ffffff",
        darkItemSelectedBg: "#863bff",
        darkItemSelectedColor: "#ffffff",
      },
      Card: {
        borderRadiusLG: 14,
      },
    },
  };

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      <ConfigProvider theme={configTheme}>{children}</ConfigProvider>
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within a ThemeProvider");
  return ctx;
}
