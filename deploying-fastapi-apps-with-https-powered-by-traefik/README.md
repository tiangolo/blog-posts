# Deploying FastAPI (and other) apps with HTTPS powered by Traefik

This article lives in:

* [Dev.to](https://dev.to/tiangolo/)
* [Medium](https://tiangolo.medium.com/)
* [GitHub](https://github.com/tiangolo/blog-posts/blob/master/deploying-fastapi-apps-with-https-powered-by-traefik/README.md)

## Intro

<img src="https://raw.githubusercontent.com/tiangolo/blog-posts/master/deploying-fastapi-apps-with-https-powered-by-traefik/fastapi-with-traefik.png" />

Let's say you have a **FastAPI** application... or actually, any other type of web application, including a [Panel](https://panel.holoviz.org/) dashboard with Pandas DataFrames and Bokeh visualizations, or a [Streamlit](https://www.streamlit.io/) application. These are, in the end, web applications. You could think of many other examples.

Now let's say it all works well locally, on your machine.

But in most of the cases, the purpose of these web apps is to be available on the real web (not only on your machine), so that others can actually access them.

So you need to "deploy" them somewhere, on a remote server.

And then you would want to have secure comunication between your app clients (web browsers, mobile apps, etc.) and your server web application.

So, you should have **HTTPS**. 🔒

But although it might sound like a simple "option" to enable, it's quite more complex than than... and [Traefik](https://doc.traefik.io/traefik/) can help you a lot.

---

I have been a long time fan of Traefik, even before creating FastAPI.

And recently I had the chance to make an event/webinar with them. 🎉

You can watch the recording of the [video here on the Traefik resources' website](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/?utm_campaign=Influencer:%20Sebastian%20Ramirez,%20FastAPI%20&utm_content=155438367&utm_medium=social&utm_source=twitter&hss_channel=tw-4890312130).

## About HTTPS

HTTPS is quite more complex than "enabling an option".

The protocol any of your applications will need to "talk" is actually the same HTTP, so you don't have to change anything in your web apps to change from HTTP to HTTPS.

But that HTTP communication has to go through a secure connection (TLS/SSL), that's where the "S" in HTTPS comes from, "HTTP Secure".

There's a whole process required, including acquiring HTTPS (TLS/SSL) certificates. But fortunately, [Let's Encrypt](https://letsencrypt.org/) provides them for free... you just have to set everything up.

But then, "setting everything up" including acquiring the certificates, installing them where appropriate, renewing them every three months, etc. It's all a relatively complex process. But Traefik can do all that for you.

To quickly learn how HTTPS works from the consumer's perspective, I highly encourage you to go and check [HowHTTPS.works](https://howhttps.works/).

Then you can go and read the short summary of what you need to know as a _developer_ in the [FastAPI docs: About HTTPS](https://fastapi.tiangolo.com/deployment/https/).

## Domain name

HTTPS is tied to a domain name, because the TLS certificate is for that specific domain name.

So, you need to have one, or buy one.

I buy my domains at <a title="This link has my referral code, if you don't want to use it, you can also type it in the browser. 🤷" href="https://www.name.com/referral/16bb2">Name.com</a>, it's quite cheap and it has worked quite well for me.

## Remote server

You will also need a "cloud" or remote server.

It's frequently called a "VPS" for "virtual private server". It's a "private server" because you get a full Linux system with full control of it (contrary to a "shared hosting"). And it's "virtual" because what providers do is create a virtual machine and make it available for you, instead of installing a real physical server, that's why they are affordable.

For simplicity, I would suggest these providers:

* <a title="This link has my referral code, if you don't want to use it, you can also type it in the browser. 🤷" href="https://m.do.co/c/fc6c7539f7a9">DigitalOcean</a>
* <a title="This link has my referral code, if you don't want to use it, you can also type it in the browser. 🤷" href="https://www.linode.com/?r=8ee6f60b2ddb258bba3fefe264771bca3660fb97">Linode</a>
* <a title="This link has my referral code, if you don't want to use it, you can also type it in the browser. 🤷" href="https://www.vultr.com/?ref=7529603">Vultr</a>

I personally have things in each one of those. They all work great, they have a simple and nice user experience, and are quite cheap.

Even with $5 or $10 USD a month is enough to have one of the small servers up and running.

You can also go and use one of the giant cloud infrastructure providers if you want, learn all their terminology and components, set up all the accounts, permissions, etc. And then use them. But for this example I would suggest one of the three above as it will be a lot simpler.

## DNS records

When you create a remote server, it will have a public IP.

But now you need to configure your domain to point to that IP, so that when your users go to your domain, they end up talking to your remote server in its IP.

There's a set of "records" that do that, they are called "DNS records" (DNS for "Domain Name System").

Those records are stored in "Name Servers". All of these cloud providers above have free Name Servers, so you can use them to store that information about pointing domains to IPs.

**Tip**: those same DNS records are also used for configuring email, and other related small things.

**Note**: all these Name Server and DNS changes are automatically copied and replicated through the web, so that everyone on the world know where to access the information about your domain, and then, with that they will know to which IP they should talk to when interacting with your domain. Because that replication takes some time, after you save some of these changes, they can take from minutes to hours to be ready.

### Name Servers

The first step is in your "registrar" (the entity that sold you the domain, e.g. Name.com). In there, you define what are the Name Servers for your domain.

You will probably first want to remove the default Name Servers. After buying a domain, the default Name Servers are normally the ones for the same registrar (e.g. Name.com), and normally all they do is have **DNS records** to point the domain to a placeholder page full of ads, but they normally don't allow you to create **DNS records** (like pointing the domain to an IP address).

So, you will probably want to remove those default **Name Servers** and add the ones for your VPS provider.

E.g. you could add the Name Servers for DigitalOcean:

```
ns1.digitalocean.com
ns2.digitalocean.com
ns3.digitalocean.com
```

### DNS Records

After you configure the **Name Servers** for your domain to be the ones for your cloud provider, you can now go to that cloud provider and set up the **DNS records**.

Depending on your cloud provider, they will have some section to configure "domains", "domain zones", or "networks", in the end they all refer to the same configurations for **DNS records** for a specific domain.

So, the next step, is to create a configuration there for your specific domain (sometimes called a "domain zone").

Then, inside of that domain configuration, you need to add a **DNS record** to point any web communication to your cloud server.

There are several types of DNS records, the one we need is an **A record**, when you are creating a DNS record, those are normally the default type as they are the most important one.

An **A record** has an **IP** and a **hostname**.

The **IP** would be be the one for your remote server. You might need to go to the section in the dashboard where your server is located to copy that IP.

The **hostname** would be your domain, or any sub-domain. So, if you bought `example.com`, you can set the record to `example.com`, or to `somesubdomain.example.com` or also `a.long.sub.domain.example.com`. In most cases you can even use `*.example.com`, that will match any sub-domain and point it to the IP you specify.

You can create multiple **A records**, one for each domain or sub-domain. And each of them can point to different IPs. That's also why you see some applications that use several domains, like `dashboard.example.com` and `api.example.com`, to handle different parts of the same system in different servers.

**Note**: depending on the provider, you might need to use the symbol `@` in the hostname to mean "the same domain I'm configuring", so, for the domain configurations for `example.com`, creating an **A record** with some IP and the hostname `@` would mean "point the same domain `example.com` to that IP address".

### Wait

You might have to wait some time for these DNS changes to replicate.

You can test if your computer already has access to the most recent version of your records with the tool `ping` from the command line. For example, checking for the domain `tiangolo.com`:

```console
$ ping tiangolo.com                               
PING tiangolo.com (104.198.14.52) 56(84) bytes of data.
64 bytes from 52.14.198.104.bc.googleusercontent.com (104.198.14.52): icmp_seq=1 ttl=103 time=204 ms
64 bytes from 52.14.198.104.bc.googleusercontent.com (104.198.14.52): icmp_seq=2 ttl=103 time=226 ms
```

you can see the IP address is `104.198.14.52`. If that's what you just configured, congrats!

The DNS records are ready. 🎉

## Check the video

From this point, you should be able to [follow the video recording](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/?utm_campaign=Influencer:%20Sebastian%20Ramirez,%20FastAPI%20&utm_content=155438367&utm_medium=social&utm_source=twitter&hss_channel=tw-4890312130) with all the explanations.

So I'll keep the rest of this post as simple as possible, mainly showing you the config files so you can copy all the examples.

## Simple FastAPI app

Let's start with a basic [**FastAPI**](https://fastapi.tiangolo.com/) app.

I'm assuming that you know a bit about FastAPI, if you don't, feel free to check the documentation, it is written as a tutorial.

If you want to see the explanation step by step, feel free to check the video.

The basic app we will use is in a file at `./app/main.py`, with:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "Hello World of FastAPI with Traefik"}
```

## Dockerfile

We will use [Docker](https://www.docker.com/) to deploy everything.

So, make sure you install it.

Then we need a file at `./app/Dockerfile` with:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/
```

Notice that we are using the official FastAPI Docker image: `tiangolo/uvicorn-gunicorn-fastapi:python3.8`.

The official base Docker image does most of the work for us, so we just have to copy the code inside.

Make sure you have [Docker installed](https://docs.docker.com/get-docker/) in your local computer and in the remote server.

## Prepare your cloud server

* Connect to your remote server from your terminal with SSH, it could be something like:

```bash
ssh root@fastapi-with-traefik.example.com
```

* Update the list of package versions available:

```bash
apt update
```

* Upgrade the packages to the latest version:

```bash
apt upgrade
```

## Docker Compose

We are using Docker Compose to manage all the configurations. So make you you [install Docker Compose](https://docs.docker.com/compose/install/) locally and on the remote server.

To prevent Docker Compose from hanging, install `haveged`:

```console
apt install haveged
```

**Technical Details**: Docker Compose uses the internal pseudo-random number generators of the machine. But in a freshly installed/created cloud server it might not have enough of that "randomness". And that could make the Docker Compose commands to hang forever waiting for enough "randomness" to use. `haveged` prevents/fixes that issue.

After that, you can check that Docker Compose works correctly.

## Docker Compose files

For all the detailed explanation of the Docker Compose files, [check the video recording](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/?utm_campaign=Influencer:%20Sebastian%20Ramirez,%20FastAPI%20&utm_content=155438367&utm_medium=social&utm_source=twitter&hss_channel=tw-4890312130).

Make sure you update the domains from `example.com` to use yours, and the email to register with Let's Encrypt, you will receive notifications about your expiring certificates in that email.

Also make sure you add the right **DNS records** for your main application, and for the Traefik dashboard, and update them in the Docker Compose files accordingly.

Here are the Docker Compose files are for you to copy them easily.

* `docker-compose.traefik.yml`:

```YAML
services:

  traefik:
    # Use the latest v2.3.x Traefik image available
    image: traefik:v2.3
    ports:
      # Listen on port 80, default for HTTP, necessary to redirect to HTTPS
      - 80:80
      # Listen on port 443, default for HTTPS
      - 443:443
    restart: always
    labels:
      # Enable Traefik for this service, to make it available in the public network
      - traefik.enable=true
      # Define the port inside of the Docker service to use
      - traefik.http.services.traefik-dashboard.loadbalancer.server.port=8080
      # Make Traefik use this domain in HTTP
      - traefik.http.routers.traefik-dashboard-http.entrypoints=http
      - traefik.http.routers.traefik-dashboard-http.rule=Host(`traefik.fastapi-with-traefik.example.com`)
      # Use the traefik-public network (declared below)
      - traefik.docker.network=traefik-public
      # traefik-https the actual router using HTTPS
      - traefik.http.routers.traefik-dashboard-https.entrypoints=https
      - traefik.http.routers.traefik-dashboard-https.rule=Host(`traefik.fastapi-with-traefik.example.com`)
      - traefik.http.routers.traefik-dashboard-https.tls=true
      # Use the "le" (Let's Encrypt) resolver created below
      - traefik.http.routers.traefik-dashboard-https.tls.certresolver=le
      # Use the special Traefik service api@internal with the web UI/Dashboard
      - traefik.http.routers.traefik-dashboard-https.service=api@internal
      # https-redirect middleware to redirect HTTP to HTTPS
      - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
      - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
      # traefik-http set up only to use the middleware to redirect to https
      - traefik.http.routers.traefik-dashboard-http.middlewares=https-redirect
      # admin-auth middleware with HTTP Basic auth
      # Using the environment variables USERNAME and HASHED_PASSWORD
      - traefik.http.middlewares.admin-auth.basicauth.users=${USERNAME?Variable not set}:${HASHED_PASSWORD?Variable not set}
      # Enable HTTP Basic auth, using the middleware created above
      - traefik.http.routers.traefik-dashboard-https.middlewares=admin-auth
    volumes:
      # Add Docker as a mounted volume, so that Traefik can read the labels of other services
      - /var/run/docker.sock:/var/run/docker.sock:ro
      # Mount the volume to store the certificates
      - traefik-public-certificates:/certificates
    command:
      # Enable Docker in Traefik, so that it reads labels from Docker services
      - --providers.docker
      # Do not expose all Docker services, only the ones explicitly exposed
      - --providers.docker.exposedbydefault=false
      # Create an entrypoint "http" listening on port 80
      - --entrypoints.http.address=:80
      # Create an entrypoint "https" listening on port 443
      - --entrypoints.https.address=:443
      # Create the certificate resolver "le" for Let's Encrypt, uses the environment variable EMAIL
      - --certificatesresolvers.le.acme.email=admin@example.com
      # Store the Let's Encrypt certificates in the mounted volume
      - --certificatesresolvers.le.acme.storage=/certificates/acme.json
      # Use the TLS Challenge for Let's Encrypt
      - --certificatesresolvers.le.acme.tlschallenge=true
      # Enable the access log, with HTTP requests
      - --accesslog
      # Enable the Traefik log, for configurations and errors
      - --log
      # Enable the Dashboard and API
      - --api
    networks:
      # Use the public network created to be shared between Traefik and
      # any other service that needs to be publicly available with HTTPS
      - traefik-public

volumes:
  # Create a volume to store the certificates, there is a constraint to make sure
  # Traefik is always deployed to the same Docker node with the same volume containing
  # the HTTPS certificates
  traefik-public-certificates:

networks:
  # Use the previously created public network "traefik-public", shared with other
  # services that need to be publicly available via this Traefik
  traefik-public:
    external: true
```

* `docker-compose.yml`:

```YAML
services:

  backend:
    build: ./
    restart: always
    labels:
      # Enable Traefik for this specific "backend" service
      - traefik.enable=true
      # Define the port inside of the Docker service to use
      - traefik.http.services.app.loadbalancer.server.port=80
      # Make Traefik use this domain in HTTP
      - traefik.http.routers.app-http.entrypoints=http
      - traefik.http.routers.app-http.rule=Host(`fastapi-with-traefik.example.com`)
      # Use the traefik-public network (declared below)
      - traefik.docker.network=traefik-public
      # Make Traefik use this domain in HTTPS
      - traefik.http.routers.app-https.entrypoints=https
      - traefik.http.routers.app-https.rule=Host(`fastapi-with-traefik.example.com`)
      - traefik.http.routers.app-https.tls=true
      # Use the "le" (Let's Encrypt) resolver
      - traefik.http.routers.app-https.tls.certresolver=le
      # https-redirect middleware to redirect HTTP to HTTPS
      - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
      - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
      # Middleware to redirect HTTP to HTTPS
      - traefik.http.routers.app-http.middlewares=https-redirect
      - traefik.http.routers.app-https.middlewares=admin-auth
    networks:
      # Use the public network created to be shared between Traefik and
      # any other service that needs to be publicly available with HTTPS
      - traefik-public

networks:
  traefik-public:
    external: true
```

* `docker-compose.override.yml`:

```YAML
services:

  backend:
    ports:
      - 80:80

networks:
  traefik-public:
    external: false
```

## Start the stacks

There are many approaches for putting your code and Docker images in your server.

You could have a very sophisticated Continuous Integration system. But for this example using a simple `rsync` would be enough.

For example:

```console
rsync -a ./* root@fastapi-with-traefik.example.com:/root/code/fastapi-with-traefik/ 
```

Then, inside of your server, make sure you create the Docker network:

```console
docker network create traefik-public
```

Next, create the environment variables for HTTP Basic Auth.

* Create the username, e.g.:

```bash
export USERNAME=admin
```

* Create an environment variable with the password, e.g.:

```bash
export PASSWORD=changethis
```

* Use `openssl` to generate the "hashed" version of the password and store it in an environment variable:

```bash
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
```

And now you can start the **Traefik** Docker Compose stack:

```console
docker-compose -f docker-compose.traefik.yml up
```

Next, start the main Docker Compose stack:

```console
docker-compose -f docker-compose.yml up -d
```

## Check your app

After that, if everything worked correctly (and probably it didn't work correctly the first time 😅), you should be able to check your new application live at your domain, something like:

```
https://fastapi-with-traefik.example.com
```

And the Traefik dashboard at:

```
https://traefik.fastapi-with-traefik.example.com
```

And the Traefik dashboard would be protected by HTTP Basic Auth, so no one can go and tamper with your Traefik.

## Celebrate 🎉

Congrats! That's a very stable way to have a production application deployed.

You can probably improve that a lot, add Continuous Integration, monitoring, logging, use a complete cluster of machines instead of a single one (e.g. use Kubernetes instead of Docker Compose), etc. There's no limit to adding more stuff and improving it all...

But with this, you already have the minimum to serve your users a secure application.

And as your deployment is based on Docker, and can be replicated easily and quickly, you could destroy that server, create a new one from scratch, and be live again in minutes. Because it doesn't depend on _that_  specific server.

All the important configurations and setup is in your Docker Compose files.

And all the important logic and setup of the actual app is in the Docker image (with the `Dockerfile`).

And Docker itself is taking care of having your application running, restarting it after failures or reboots, etc.

## Dessert 🍰

Do you want a bit more?

Check [the source code for this blog post](https://github.com/tiangolo/blog-posts/blob/master/deploying-fastapi-apps-with-https-powered-by-traefik/), including the latest version of the app and config files, including a basic example with Panel, and one with Streamlit. ✨

## Learn More

Here are some extra resources:

* [HowHTTPS.works](https://howhttps.works/).
* [FastAPI docs: HTTPS for developers](https://fastapi.tiangolo.com/deployment/https/).
* Event [video recording in **Traefik resources**](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/?utm_campaign=Influencer:%20Sebastian%20Ramirez,%20FastAPI%20&utm_content=155438367&utm_medium=social&utm_source=twitter&hss_channel=tw-4890312130).
* [Source code in GitHub](https://github.com/tiangolo/blog-posts/blob/master/deploying-fastapi-apps-with-https-powered-by-traefik/).
* [Traefik docs](https://doc.traefik.io/traefik/).
* [FastAPI docs](https://fastapi.tiangolo.com/).

---

I hope that was useful! 🚀

## About me

Hey! 👋 I'm Sebastián Ramírez ([tiangolo](https://tiangolo.com)).

You can follow me, contact me, see what I do, or use my open source code:

* [GitHub: tiangolo](https://github.com/tiangolo)
* [Twitter: tiangolo](https://twitter.com/tiangolo)
* [LinkedIn: tiangolo](https://www.linkedin.com/in/tiangolo/)
* [Dev: tiangolo.to](https://dev.to/tiangolo)
* [Medium: tiangolo](https://tiangolo.medium.com/)
* [Web: tiangolo.com](https://tiangolo.com)
