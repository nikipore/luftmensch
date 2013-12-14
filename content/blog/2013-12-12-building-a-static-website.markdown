Title: Static website hosting
date: 2013-12-12 19:58
Category: blog
Tags: aws, cloudfront, cdn, fabric, pelican, s3, static-website, web

### Why a dynamic website is oversized for a simple blog ###

I've been quite busy over the last couple of weeks revamping my blog. I had originally started with a dynamic site built upon [Drupal](https://drupal.org/): I wanted to learn how modern content management systems (CMS) separate content, style and functionality. I took a bit of a learning curve around topics like CSS, responsive website layout, some PHP, database management and whatnot. A lot of the problems I had to deal with stemmed from the sheer complexity of Drupal and its plethora of the available modules of varying quality, at least when the result had to be perfect in terms of code highlighting, typographic finesses, color schemes, web editor, anti-spam measures. There are also rather great components like the [Omega](https://drupal.org/project/omega) theme on which I finally settled to base my design upon. In the end, I was pretty content with the look-and-feel and with what I've learned.

But all I'm after is to write a blog post every now and then, and to experiment a little here and there with CSS and Javascript to improve the design and user experience. For this use case, a dynamic website is like using a sledgehammer to crack a nut. The maintenance was a nightmare. Even with the assistance of the awesome [drush](https://github.com/drush-ops/drush) and quite a bit of background from my daytime job about how to properly build, deploy and version software, it was too much effort to get a proper deployment pipeline with a local test site, a remote staging site and a production site up and running, so I basically found myself crossing my fingers that my productive website wouldn't go boink because of some obscure database update or unresolved dependency nightmare. I had to fight off spam attacks. And the site was slow: PHP code and database lookups are server-side operations, which means they are a potential bottleneck -- in particular if you share the resources with other users -- and don't scale well when your site becomes crowded suddenly.

### Enter static websites ###

The "static" part refers to the absence of server-side logic, meaning that the content just consists of flat files which come to life by means of the client-side technology stack HTML (content), CSS and webfonts (style), and Javascript (client-side program logic). Flat files mean that

* you can edit them in your editor of choice as opposed to some crappy and buggy web interface,
* organize them in a version control system,
* build, preview and deploy your site using your favorite standard tool chain,
* no-one can hack your site because it is just a bunch of dead files on a read-only share.

Static content providers are available on very high quality, performance and availability standards. If you leverage the power of content delivery networks (CDN) -- which are optimized to serve static content -- your site will become blazing fast all around the globe (mine typically loads in half a second or less) and will cost you close to nothing in terms of money _and_ time. This site's sole fixed costs are 50 cents per month for DNS services, and deploying an update is one short command-line statement away.

### The series ###

I am planning to share the cool stuff and the gotchas I've come across in a series of posts. The topics I've got in mind so far are

* choosing a static website generator and setting it up
* ditto for a static content provider
* setting up a toolchain for build, preview and version control
* supercharge your website using a CDN
* styling your website (theming, responsive layout, code snippets and syntax highlighting)
* fine-tuning of the static website generator
* setting up web services (sharing, discussions, traffic analysis)

I've built the site you are looking at with the following stack:

* The Python-based [Pelican](https://github.com/getpelican) generates the website content.
* The source code is under version control by [Git](http://git-scm.com/).
* [Fabric](https://github.com/fabric/fabric) -- which is also Python-based -- powers the build and deployment chain.
* I use [Amazon Web Services](http://aws.amazon.com/) for DNS services (Route 53), content hosting (S3) and CDN (CloudFront), plus [`s3cmd`](http://s3tools.org/s3cmd) as a command-line API to S3 and CloudFront.
* My theme is based upon Twitter's [Bootstrap](http://getbootstrap.com/) style framework.

### The sources ###

The [LESS](http://lesscss.org/) sources for the luft·mensch bootstrap theme are [here](https://github.com/nikipore/my-bootstrap/tree/master/luftmensch). My Pelican [bootstrap theme](https://github.com/nikipore/my-pelican-themes/tree/master/bootstrap3) started out from [pelican-boostrap3](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3), but it has sinced moved in a different direction, so I put in into a repository of its own.

Stay tuned on my [feed](http://localhost:8000/feeds/all.atom.xml) and feel free to share comments and thoughts.