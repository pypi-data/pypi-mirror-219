<p align="center">
    <a href="https://github.com/Noelgram/Noelgram">
        <img src="https://docs.Noelgram.org/_static/Noelgram.png" alt="Noelgram" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://noelgram.org">
        Homepage
    </a>
    •
    <a href="https://docs.noelgram.org">
        Documentation
    </a>
    •
    <a href="https://docs.noelgram.org/releases">
        Releases
    </a>
    •
    <a href="https://t.me/noelgram">
        News
    </a>
</p>

## Noelgram

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

``` python
from noelgram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Noelgram!")


app.run()
```

**Noelgram** is a modern, elegant and asynchronous [MTProto API](https://docs.noelgram.org/topics/mtproto-vs-botapi)
framework. It enables you to easily interact with the main Telegram API through a user account (custom client) or a bot
identity (bot API alternative) using Python.

### Support

If you'd like to support Noelgram, you can consider:

- [Become a GitHub sponsor](https://github.com/sponsors/delivrance).
- [Become a LiberaPay patron](https://liberapay.com/delivrance).
- [Become an OpenCollective backer](https://opencollective.com/noelgram).

### Key Features

- **Ready**: Install Noelgram with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by [TgCrypto](https://github.com/noelgram/tgcrypto), a high-performance cryptography library written in C.  
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.

### Installing

``` bash
pip3 install noelgram
```

### Resources

- Check out the docs at https://docs.noelgram.org to learn more about Noelgram, get started right
away and discover more in-depth material for building your client applications.
- Join the official channel at https://t.me/noelgram and stay tuned for news, updates and announcements.
