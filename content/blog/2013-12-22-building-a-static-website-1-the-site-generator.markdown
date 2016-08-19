Title: Building a static website: the website generator
date: 2013-12-22 20:00
Category: blog
Tags: fabric, make, pelican, python, web, static-website

I became aware of static website generators when I read a blog which was built using [Octopress](http://octopress.org/). I was surprised how many of the features worked out of the box that I had wrestled with using Drupal, among them a proper support of Markdown, typographic refinements, code inclusion and sytax highlighting, a tag cloud, easy access to page layout and so forth.

I would be able to write posts in Markdown in a proper text editor.[^1] To put all content, templates, styles and scripts under version control in a very natural fashion. To use `rsync` or `git push` to deploy the site. To have the full power of a script language at my fingertips, in the case of Octopress this would be Ruby with all its third-party libraries and the Jekyll ecosystem. Hey, an opportunity to add some Ruby skills on top of Python! To cut a long story short, I was immediately psyched. But first things first:

###What is a static website generator?###

A *static website generator* is a toolchain which transforms a bunch of source files into -- guess what -- a static website. That is, a system of interlinked HTML pages with special pages for a table of content or blogroll, tag and category pages, archive pages, ... plus style sheets and *client*-side
 magic in the form of advanced CSS and JavaScript. The word *static* refers to the absence of *server*-side logic such as PHP, CGI, WSGI, ...

A static website generator toolchain typically consists of

* the generator itself
* text parsers and compilers
* a templating engine
* a build system (think of `make` and its kin)
* optional generator plugins

The generator organizes the metadata into a HTML site tree,
leverages upon the parsers and templating engine in order to transform content source code -- written in [Markdown](http://daringfireball.net/projects/markdown/), [reStructuredText](http://docutils.sourceforge.net/rst.html), or whatever -- into HTML content, takes care of web asset management like minifying CSS or JavaScript, code inclusion and highlighting. The generators which I came across are all implemented in some scripting language and open to your customizations by means of plugins, configuration modules, and contributions to the source code (say, via a pull request to a project on GitHub).

###Which website generator is for me?###

Well, I cannot answer this question for you, but I'll illustrate how I found the website generator I am using now. As I said, I started out with [Octopress](http://octopress.org/) because it just was the first I came across. My motivation to learn Ruby was undermined by my troubles getting a Ruby package manager running on OS X Mavericks. I had some issues with the Ruby ecosystem on [MacPorts](http://www.macports.org/), and [Homebrew](http://brew.sh/) didn't work so well either. In both cases I had to fiddle with the compiler settings because the required Ruby packages would only compile with GCC as opposed to the default Apple compiler. I got it working more or less, but I did never really understand why and how so. Being tired of it, I turned to my good old friend Python plus virtualenv. The two choices that came up instantly in a search were [Pelican](https://github.com/getpelican) and [Nikola](http://nikola.ralsina.com.ar/). I started out with Pelican because of its more vibrant GitHub activity and plugin ecosystem, and I'm still there. Although almost certainly I'll give Nikola a test drive as soon as I'm feeling that itch the next time ...

Summarizing, I believe you're well-advised  to let your choice be influenced strongly by which programming language and corresponding ecosystem you feel most comfortable with. There is a plethora of [choices](http://staticsitegenerators.net/) not only for Python and Ruby, but also for JavaScript, Groovy, Perl, PHP, Node.js, Go, ...

###Setting up Pelican###

You just follow Pelican's [documentation](http://docs.getpelican.com/en/latest/install.html). It explains the installation process well and completely, so I do not write that down here. I rather would like to stress some points which I find important:

* I *highly* recommend that you create a virtual Python environment for your Pelican installation. If you don't know how and why you should do this, read the [virtualenv](www.virtualenv.org/) documentation. Really, you should never, ever mess up your system's Python installation with anything.[^2]
* You should take your site under version control. I am using Git and store the contents of my site [here](https://github.com/nikipore/luftmensch). Create a new repo following these [instructions](https://help.github.com/articles/create-a-repo).
* Use the wizard `pelican-quickstart` to rise a scaffolding for your site in the repository's folder.
* The wizard generates build configurations for `make` and the Python-based build tool [Fabric](https://github.com/fabric/fabric). I went with Fabric, because I prefer writing Python to shell code, and because I find it more portable across platforms than `make`.[^3] But the necessary commands to drive a Pelican build chain are so simple that anything will do, be it Ant, Maven, or even a bunch of simple shell scripts. I'll come back to tweaking the build chain later.

If you've got your site up and running, and you have added a little test content, it is time to think about finding a content provider for your website. This will be the topic of the next post.

[^1]: I am using [Sublime Text 3](http://www.sublimetext.com/3) and [vim](http://www.vim.org/), plus [Marked](http://markedapp.com/) as a previewer.

[^2]: I recommend that you also install the convenience [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/#). I activate my Pelican project with a simple `workon pelican && cd ~/git/luftmensch/` which I usually grab from the shell command history by pressing `Ctrl-R`, and then typing `wor...`.

[^3]: Even on a Windows platform, though, I recommend to run a small Linux installation somewhere, either in a multiboot or virtual machine environment on your local machine, or remotely on a virtual server. Windows just sucks for any development activities.
