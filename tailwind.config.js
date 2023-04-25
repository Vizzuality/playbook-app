module.exports = {
    content: [
      "./templates/**/*.html",
      "./static/src/**/*.js"
    ],
    darkMode: 'media',
    theme: {
      extend: {
        fontFamily: {
          sans: ['Inter var']
        },
      },
    },
    variants: {
      extend: {},
    },
    plugins: [
      require('@tailwindcss/forms'),
    ]
  }
  