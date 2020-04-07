// don't forget to npm run css after making changes
module.exports = {
  theme: {
    // https://tailwindcss.com/docs/height#customizing
    // extending to add customized tailwind class
    extend: {
      // vh is view height: window size relative to the screen size
      // tailwind class for vh as {"name of the class": "input for css"}
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh"
      },
      // https://tailwindcss.com/docs/border-radius#customizing
      borderRadius: {
        xl: "1.5rem"
      },
      gridTemplateColumns: {
        card: "minmax(250px, 1fr);"
      },
      theme: {
        maxHeight: {
          "0": "0",
          "1/4": "25%",
          "1/2": "50%",
          "3/4": "75%",
          full: "100%"
        },
        fontSize: {
          cardsmall: ".825rem"
        }
      }
    },
    variants: {},
    plugins: []
  }
};
