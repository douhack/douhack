var gulp = require('gulp'),
	concat = require('gulp-concat'),
	minifyCss = require('gulp-minify-css'),
	autoprefixer = require('gulp-autoprefixer'),
	sass = require('gulp-sass'),
  livereload = require('gulp-livereload');

gulp.task('sass', function () {
    gulp.src('./scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('./css'));
});

gulp.task('cssMin', function() {
  gulp.src('./css/*.css')
    .pipe(autoprefixer())
    .pipe(minifyCss())
    .pipe(concat('all.min.css'))
    .pipe(gulp.dest('./css/min/'));
});

gulp.task('watch', function() {
	gulp.watch('./sass/*.scss', ['sass']);
	gulp.watch('./css/*.css', ['cssMin']).on('change', livereload.changed);
});

gulp.task('default', ['sass','cssMin', 'watch']);