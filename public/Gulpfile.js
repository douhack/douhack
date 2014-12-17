var gulp = require('gulp'),
	concat = require('gulp-concat'),
	minifyCss = require('gulp-minify-css'),
	autoprefixer = require('gulp-autoprefixer'),
	sass = require('gulp-sass'),
  livereload = require('gulp-livereload');

gulp.task('sass', function () {
    gulp.src('./scss/global.scss')
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(minifyCss())
        .pipe(concat('all.min.css'))
        .pipe(gulp.dest('./css/min/'));
});

gulp.task('watch', function() {
	gulp.watch('./scss/*.scss', ['sass']).on('change', livereload.changed);
});

gulp.task('default', ['sass', 'watch']);