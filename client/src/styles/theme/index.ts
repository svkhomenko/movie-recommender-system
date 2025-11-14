import { createSystem, defaultConfig } from '@chakra-ui/react';

export const system = createSystem(defaultConfig, {
  globalCss: {
    html: {
      colorPalette: 'accent',
    },
  },
  theme: {
    tokens: {
      colors: {
        pageBg: { value: '#17233b' },
        pageBgShadow: { value: '#131d36' },
        primaryText: { value: '#ffffff' },
        cardBg: { value: '#36395a' },
        accent: {
          50: { value: '#fff8f0' },
          100: { value: '#fef1df' },
          200: { value: '#fbe4c5' },
          300: { value: '#fcd39f' },
          400: { value: '#fabf8a' },
          500: { value: '#f9bc85' },
          600: { value: '#e2945d' },
          700: { value: '#b57041' },
          800: { value: '#8a4e2a' },
          900: { value: '#5f3216' },
          950: { value: '#301807' },
        },
        neutral: {
          50: { value: '#f4f4f7' },
          100: { value: '#e2e3eb' },
          200: { value: '#c7c9d9' },
          300: { value: '#a9acce' },
          400: { value: '#9699bf' },
          500: { value: '#737aa8' },
          600: { value: '#4e5076' },
          700: { value: '#434668' },
          800: { value: '#36395a' },
          900: { value: '#2e314d' },
          950: { value: '#1a1b2b' },
        },
      },
    },
    semanticTokens: {
      colors: {
        bg: {
          value: '{colors.pageBg}',
        },
        fg: {
          value: '{colors.primaryText}',
        },
        card: {
          value: '{colors.cardBg}',
        },
        hover: {
          value: '{colors.neutral.600}',
        },
        focusRing: {
          value: '{colors.accent.300}',
        },
        accent: {
          solid: { value: '{colors.accent.500}' },
          contrast: { value: '{colors.primaryText}' },
          fg: { value: '{colors.accent.600}' },
          muted: { value: '{colors.accent.200}' },
          subtle: { value: '{colors.accent.100}' },
          emphasized: { value: '{colors.accent.300}' },
          focusRing: { value: '{colors.accent.500}' },
          hover: { value: '{colors.accent.700}' },
        },
        neutral: {
          solid: { value: '{colors.neutral.600}' },
          contrast: { value: '{colors.primaryText}' },
          fg: { value: '{colors.neutral.500}' },
          muted: { value: '{colors.neutral.300}' },
          subtle: { value: '{colors.neutral.200}' },
          emphasized: { value: '{colors.neutral.400}' },
          focusRing: { value: '{colors.neutral.500}' },
          hover: { value: '{colors.neutral.700}' },
        },
      },
    },
  },
});
