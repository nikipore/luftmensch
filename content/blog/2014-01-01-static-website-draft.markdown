Title: Static website hosting
date: 2013-12-12 19:58
Category: blog
Tags: aws, s3, cloudfront, cdn, gzip, pelican, web, static-website
Status: draft 

I've been quite busy over the last couple of weeks revamping my blog. I had originally started with a dynamic site built upon [Drupal](https://drupal.org/). I did so because I wanted to learn how modern content managment systems (CMS) separate content, style and functionality. I had a steep learning curve around topics like CSS, responsive website layout, a little bit of PHP, database management and whatnot. A lot of the problems I had to deal with stemmed from the sheer complexity of Drupal, and the pitfalls of the available modules, at least when the result had to be perfect in terms of code highlighting, typographic finesses, color schemes, web editor, anti-spam measures. There are also rather great components like the [Omega theme](https://drupal.org/project/omega) on which I finally settled to base my design upon. In the end, I was pretty content with the look-and-feel and with what I've learned.

But all I'm after is to write a blog post every now and then, and to experiment a little here and there with CSS and Javascript to improve the design and user experience. For this use case, a dynamic website is like using a sledgehammer to crack a nut. The maintenance was a nightmare. Even with the assistance of the awesome [`drush`](https://github.com/drush-ops/drush) and quite a bit of knowledge about how to properly build, deploy and version software, it was too much effort to get a proper deployment pipeline with a local test site, a remote staging site and a production site up and running, so I basically found myself crossing my fingers that my productive website wouldn't go boink because of some obscure database update or unresolved dependency nightmare. I had to fight off spam attacks. And the site was slow; PHP code and database lookups are server-side operations, which means they are a potential bottleneck -- in particular if you share the resources with other users -- and don't scale well when your site becomes crowded suddenly.

Enter static websites. The "static" part refers to the absence of server-side logic, meaning that the content just consists of flat files which come to life by means of the client-side technology stack HTML (content), CSS and webfonts (style), and Javascript (client-side program logic). Flat files mean that

* you can edit them in your editor of choice instead of some crappy and buggy web interface,
* you can organize them in a version control system,
* build, preview and deploy your site using your favorite standard tool chain,
* no-one can hack your site with spam because they are just a bunch of files on a read-only share.

Static content providers are available on very high quality, performance and availability standards. If you leverage the power of content delivery networks (CDN) -- which are optimized to serve static content -- your site will become blazing fast all around the globe (mine loads in a third of a second) and will cost you close to nothing in terms of money _and_ time.

I am planning to share the cool stuff and the gotchas I've come across in a series of posts. The topics I've got in mind so far are

* choosing a static website generator
* choosing a static content provider
* setting up a toolchain for build, preview and version control
* supercharge your website using a CDN 
* styling your website
* setting up web services (sharing, discussions, traffic analysis)

Stay tuned on my [news feed](http://localhost:8000/feeds/all.atom.xml) and feel free to share comments and thoughts.

<!--
The providers I came across included [Heroku](https://www.heroku.com/), [GitHub](https://github.com/) pages, or [Amazon Web Services](http://aws.amazon.com/).-->