# `python-mommy-venv`

[![PyPi version](https://img.shields.io/pypi/v/python-mommy-venv)](https://pypi.org/project/python-mommy-venv/)
[![publishing workflow](https://github.com/acute-interpreter-panic/python-mommy-venv/actions/workflows/python-publish.yml/badge.svg)](https://github.com/acute-interpreter-panic/python-mommy-venv/actions)

Mommy's here to support you when running python~ ❤️

`python-mommy-venv` tries to be as compatible with [`cargo-mommy`](https://github.com/Gankra/cargo-mommy). It used some code from [`python-mommy`](https://github.com/Def-Try/python-mommy) as starting point. The configuration is way different to make greater compatibility with `cargo-mommy` and to add more features. For more information check the section [why not `python-mommy`](#why-not-python-mommy).

# buttplug.io integration

I really want to integrate buttplug.io with [`buttplug-py`](https://github.com/Siege-Wizard/buttplug-py) into this project. This should make mommy support [buttplug.io](https://buttplug.io/). Unfortunately I am currently in a really bad place monetarily and don't own a device to test this on.

So if you want to see this implemented or just want to improve the day of a fellow trans girl, shoot me a mail at [acute_interpreter_panic@proton.me](mailto:acute_interpreter_panic@proton.me) and then you can buy me one. Of course I will update it once I got my hands on a... device

# Installation

Mommy can be found on `pip`~

```sh
pip install python-mommy-venv
```

# Usage

Run whatever python command you would normally but add `-m mommy` after python~

```
python -m mommy meow.py

  File "/home/fname/Projects/OpenSource/python-mommy-venv/meow.py", line 4
    time.sleep(0)dfsadfas
                 ^^^^^^^^
SyntaxError: invalid syntax

does mommy's little girl need a bit of a break~?
```

If you want to configure aliases to do so you can run `mommy_config`. This will prompt you for the options to print the aliases you could set, or to automatically configure the aliases inside of a virtual environment.

```
python -m mommy_config
```

Alternatively you can choose to wrap the interpreter inside a virtual environment to automatically execute mommy without an alias. This is not recommended though

> NOTE: all mommy's commands can also be run with daddy instead. 

# Configuration

## Environment Variable

_this is mainly implemented to get compatibility to `cargo-mommy`_

Mommy will read the following environment variables to make her messages better for you~ ❤️

* `PYTHON_MOMMYS_LITTLE` - what to call you~ (default: "girl")
* `PYTHON_MOMMYS_PRONOUNS` - what pronouns mommy will use for themself~ (default: "her")
* `PYTHON_MOMMYS_ROLES` - what role mommy will have~ (default "mommy")
* `PYTHON_MOMMYS_EMOTES` - what emotes mommy will have~ (default "❤️/💖/💗/💓/💞")

All of these options can take a `/` separated list. Mommy will randomly select one of them whenever she talks to you~

For example, the phrase "mommy loves her little girl~ 💞" is "PYTHON_MOMMYS_ROLE loves PYTHON_MOMMYS_PRONOUNS little PYTHON_MOMMYS_LITTLE~"

So if you set `PYTHON_MOMMYS_ROLES="daddy"`, `PYTHON_MOMMYS_PRONOUNS="his/their"`, and `PYTHON_MOMMYS_LITTLE="boy/pet/baby"` then you might get any of

* daddy loves their little boy~ ❤️
* daddy loves his little pet~ 💗
* daddy loves their little baby~ 💗

And so on~ 💓

## Config file

The you can write a config file in the following locations:

- `~/.config/mommy/mommy.toml`
- `~/.config/mommy/python-mommy.toml`

The general mommy config file is supposed to be used by other mommies, but up to this point there is no mommy that supports that.

Mommy reads toml and here is an example of the config file with the default config.

```toml
moods = ["chill"]

[vars]
role = ["mommy"]
emote = ["❤️", "💖", "💗", "💓", "💞"]
pronoun = ["her"]
affectionate_term = ['girl']
denigrating_term = ['slut', 'toy', 'pet', 'pervert', 'whore']
part = ['milk']
```

In the moods you can select which responses you can get, and under vars you can define what mommy would fill in the blanks.

To check what moods and vars mommy currently supports, look at [this file in `cargo-mommy`](https://github.com/Gankra/cargo-mommy/blob/main/responses.json).

# Configuration (kink)

<details>

<summary>
<b>THIS IS NSFW, STOP READING IF YOU WANT MOMMY TO REMAIN INNOCENT!</b>
</summary>

...

...

Good pet~ ❤️

All of mommy's NSFW content is hidden behind PYTHON_MOMMYS_MOODS, where "thirsty" is heavy teasing/flirting and "yikes" is full harsh dommy mommy kink~

You can enable "true mommy chaos mode" by setting `PYTHON_MOMMYS_MOODS="chill/thirsty/yikes"` or by editing the `moods` field in the config, making mommy oscillate wildly between light positive affirmation and trying to break you in half~

* `PYTHON_MOMMYS_MOODS` - how kinky mommy will be~ (default: "chill", possible values "chill", "thirsty", "yikes")
* `PYTHON_MOMMYS_PARTS` - what part of mommy you should crave~ (default: "milk")
* `PYTHON_MOMMYS_FUCKING` - what to call mommy's pet~ (default: "slut/toy/pet/pervert/whore")

-----

**Here's some examples of mommy being thirsty~ ❤️**

*tugs your leash*
that's a VERY good girl~ 💞

*smooches your forehead*
good job~ 💗

are you just keysmashing now~?
cute~ 💖

if you don't learn how to code better, mommy is going to put you in time-out~ 💓

-----

**And here's some examples of mommy being yikes~ 💞**

good slut~
you've earned five minutes with the buzzy wand~ 💗

*slides her finger in your mouth*
that's a good little toy~ ❤️

get on your knees and beg mommy for forgiveness you pervert~ 💗

mommy is starting to wonder if you should just give up and become her breeding stock~ 💗

</details>

# Why not `python-mommy`

My project has way more options to configure it.

`python-mommy` has many minor faults that should be fixed. Each of those aren't that bad, but they add up.

`python-mommy` wasn't updated for one year. That means the responses are way to outdated, and also don't automatically update.

# Licensing
mommy likes freedom~ ❤️, and is licensed under [MIT](LICENSE-MIT).
