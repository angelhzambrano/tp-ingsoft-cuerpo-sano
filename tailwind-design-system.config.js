/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        // Primary colors
        primary: {
          50: '#F0FDFB',
          100: '#CCFBF1',
          200: '#99F6E4',
          300: '#5EEAD4',
          400: '#2DD4BF',
          500: '#14B8A6',
          600: '#0D9488',
          700: '#0D7377',
          800: '#155E75',
          900: '#164E63',
        },

        // Semantic colors
        success: {
          50: '#F0FDF4',
          100: '#DCFCE7',
          200: '#BBEF63',
          300: '#86EFAC',
          400: '#4ADE80',
          500: '#10B981',
          600: '#059669',
          700: '#047857',
          800: '#065F46',
          900: '#064E3B',
        },

        warning: {
          50: '#FFFBEB',
          100: '#FEF3C7',
          200: '#FDE68A',
          300: '#FCD34D',
          400: '#FBBF24',
          500: '#F59E0B',
          600: '#D97706',
          700: '#B45309',
          800: '#92400E',
          900: '#78350F',
        },

        danger: {
          50: '#FEF2F2',
          100: '#FEE2E2',
          200: '#FECACA',
          300: '#FCA5A5',
          400: '#F87171',
          500: '#EF4444',
          600: '#DC2626',
          700: '#B91C1C',
          800: '#991B1B',
          900: '#7F1D1D',
        },

        neutral: {
          50: '#FAFAFA',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          900: '#111827',
        },
      },

      spacing: {
        xs: '0.25rem',
        sm: '0.5rem',
        md: '1rem',
        lg: '1.5rem',
        xl: '2rem',
        '2xl': '3rem',
      },

      borderRadius: {
        sm: '0.375rem',
        md: '0.5rem',
        lg: '0.75rem',
        xl: '1rem',
      },

      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
      },
    },
  },

  // Plugins para componentes personalizados
  plugins: [
    function ({ addComponents, theme }) {
      addComponents({
        // Buttons
        '.btn-primary': {
          '@apply px-4 py-2 rounded-md font-semibold text-white bg-primary-600 hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed':
            {},
        },
        '.btn-secondary': {
          '@apply px-4 py-2 rounded-md font-semibold text-primary-600 border-2 border-primary-600 hover:bg-primary-600 hover:text-white transition-colors':
            {},
        },
        '.btn-ghost': {
          '@apply px-4 py-2 rounded-md font-medium text-neutral-700 border border-neutral-300 hover:bg-neutral-100 transition-colors':
            {},
        },
        '.btn-sm': {
          '@apply px-3 py-1 text-sm': {},
        },
        '.btn-lg': {
          '@apply px-6 py-3 text-lg': {},
        },

        // Cards
        '.card': {
          '@apply bg-white border border-neutral-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow':
            {},
        },
        '.card-title': {
          '@apply text-xl font-bold text-neutral-900 mb-4': {},
        },
        '.card-body': {
          '@apply p-0': {},
        },

        // Badges
        '.badge': {
          '@apply inline-block px-3 py-1 rounded-md text-xs font-semibold': {},
        },
        '.badge-primary': {
          '@apply bg-primary-100 text-primary-700': {},
        },
        '.badge-success': {
          '@apply bg-success-100 text-success-700': {},
        },
        '.badge-warning': {
          '@apply bg-warning-100 text-warning-700': {},
        },
        '.badge-danger': {
          '@apply bg-danger-100 text-danger-700': {},
        },

        // Forms
        '.form-label': {
          '@apply block mb-2 text-sm font-semibold text-neutral-600': {},
        },
        '.form-control': {
          '@apply w-full px-4 py-2 border border-neutral-300 rounded-md text-base focus:outline-none focus:border-primary-600 focus:ring-2 focus:ring-primary-100 transition-colors':
            {},
        },

        // Alerts
        '.alert': {
          '@apply p-4 rounded-lg mb-4': {},
        },
        '.alert-info': {
          '@apply bg-info-50 text-info-900 border-l-4 border-info-500': {},
        },
        '.alert-success': {
          '@apply bg-success-50 text-success-900 border-l-4 border-success-500': {},
        },
        '.alert-warning': {
          '@apply bg-warning-50 text-warning-900 border-l-4 border-warning-500': {},
        },
        '.alert-danger': {
          '@apply bg-danger-50 text-danger-900 border-l-4 border-danger-500': {},
        },
      });
    },
  ],
};
