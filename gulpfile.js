const gulp = require("gulp");

const css = () => {
  const postCSS = require("gulp-postcss");
  const sass = require("gulp-sass");
  const minifyCSS = require("gulp-csso");
  sass.compiler = require("node-sass");
  return (
    gulp
      // find source
      .src("assets/scss/styles.scss")
      // compiling style.scss file -> style.css file: https://www.npmjs.com/package/gulp-sass
      .pipe(sass().on("error", sass.logError))
      // transforms tailwind rules, applied rules into actual css code
      // autoprefixer for browser compatibility: https://github.com/browserslist/browserslist
      .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
      // minify CSS for compressing bytes of style.css file: https://www.npmjs.com/package/gulp-csso#api
      .pipe(minifyCSS())
      // find destination and return the result
      .pipe(gulp.dest("static/css"))
  );
};

exports.default = css;
