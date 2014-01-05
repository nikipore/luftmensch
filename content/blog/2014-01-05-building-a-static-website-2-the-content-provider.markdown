Title: Building a static website: the content provider
date: 2014-01-05 12:00
Category: blog
Tags: fabric, make, pelican, python, web, static-website, aws, cdn, s3

Now that you have a basic skeleton up and running, it is time to think about how to push your content into the open. I currently am on a solution using Amazon Web Services but I've tried four different approaches so far. I'd like to discuss their respective advantages and disadvantages in this article. I had the following boundary conditions in mind:

* Since it's a static website, simple webspace without intelligent server-side technology is good enough.
* There is no need for an HTTPS version.
* The website must be served on my personal domain `luftmensch.net`.
* The website must be highly available and responsive around the globe.
* If my site ever got popular -- which it isn't at the time of this writing -- it must scale well.
* The mere presence must cost very little or nothing. I am willing to pay as I go whenever the traffic increases.
* Deployment should be very simple and scriptable using a command-line sync mechanism such as `rsync`, `git push`, or `s3 sync`.

###Uberspace###

I ran the Drupal version of my blog on [Uberspace](https://uberspace.de/). I hab been looking for a web space which would grow with my needs in terms of visitor traffic and at the same time allow me to play with most of the available techonologies: custom domains, installation of SSL certificates, unlimited number of databases, SSH access, Perl, Ruby, Node, Python, version control ... Add to that list whatever comes to your mind, and I am sure that Uberspace has it all, or if they haven't yet, they'll make it possible in virtually no time. Their service is very friendly, competent and quick. And beyond a symbolic minimum amount of €1, you pay what you believe is appropriate.

I highly recommend Uberspace for playing around with web technologies, but for a static website you won't need all their features. Although two of them are really interesting even for this use case: SSH access makes deployment via `rsync` a breeze, and you can tell the default web server Apache to redirect all requests to a local instance of your preferred web server, which in my case would be [nginx](http://wiki.nginx.org/Main). I am still not sure whether I'll migrate from my current backend setup (an S3 bucket) back to Uberspace because it's just so much simpler and nicer to use.

###Heroku###

When I was playing with [Octopress](http://octopress.org/), they had recommended [Heroku](https://www.heroku.com/) for deployment. It all went swift and straightforward: Deployment amounts to a simple `git push`, and my website was up and running. But then I was wondering how I could trade the subdomain `luftmensch.herokuapp.com` for my own domain. But the website is HTTPS only, and Heroku would charge me for installing an SSL certificate for my domain. I was looking for something free, or close to free, so the Heroku story ended here. Heroku looks great for hosting a large-scale web app, though.

###GitHub###

The even more obvious choice is [GitHub](https://github.com/nikipore/). The repositories of both Octopress and [Pelican](https://github.com/getpelican) are hosted on GitHub. I already had GitHub pages running for the [documentation](http://nikipore.github.io/stompest/) of one of my projects.[^1] Deployment consists of a `git push origin gh-pages` which is the same dead-simple approach that Heroku uses. Yet, I ran into the same problem as with Heroku that I couldn't get the site running under my own domain.

###Amazon Web Services###

I could have stayed with my Uberspace setup, but I wanted to check out how far I could get with a free, or close to free, setup. And I have always wanted to play with [Amazon Web Services](http://aws.amazon.com/), so I gave it a go, and I am still there. The basic setup is very simple. You need to create an S3 bucket, configure it to serve its content as web pages, and use the command-line tool `s3cmd` to sync your content to S3. If you wish to use your own domain, it depends on your domain provider whether you can forward all requests to S3 directly or not. I decided against any weak links in the chain and to invest 50 cents per month to let Amazon's Route 53 service handle the DNS part of availability.

A pure S3 website is relatively fast in its native region, but a bit slow in the rest of the world, so I've moved on to proxy the S3 backend by a cloud delivery network. The obvious free -- or rather: pay-as-you-go -- variant is Amazon CloudFront. The setup is by no means straightforward, but I've learned a lot from it, and it works quite well now -- with some caveats. I'll go deeper into the quirks and workarounds in the follow-up posts. I can say so much for now that most of the problems are caused by S3, and not by CloudFront, which is why I am still considering to replace the backend S3 by an nginx instance on Uberspace.

###Summary###

Heroku and GitHub are free and very good choices as long as you don't need a custom domain. Both are big providers, so global availability and reponsiveness should be very ok. S3 plus CloudFront is a very powerful and common setup for static blogs, but the limitations of S3's backend capabilities do hurt at times. For now, this solution is fine for me, but I seriously consider to replace S3 as a backend by an nginx instance on Uberspace.

[^1]: Those were built with [Sphinx](http://sphinx-doc.org/), the documentation generator used and recommended by Python itself, which in fact is also a static websie generator, but with a focus on generating software documentation instead of blogs. 