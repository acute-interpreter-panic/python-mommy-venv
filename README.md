# `python-mommy-venv`

[![PyPi version](https://img.shields.io/pypi/v/python-mommy-venv)](https://pypi.org/project/python-mommy-venv/)
[![publishing workflow](https://github.com/acute-interpreter-panic/python-mommy-venv/actions/workflows/python-publish.yml/badge.svg)](https://github.com/acute-interpreter-panic/python-mommy-venv/actions)

Mommy's here to support you when running python~ ❤️

`python-mommy-venv` tries to be as compatible with [`cargo-mommy`](https://github.com/Gankra/cargo-mommy). It used some code from [`python-mommy`](https://github.com/Def-Try/python-mommy) as starting point. The execution is completely different as it was very flawed, and the configuration is way different to make greater compatibility with `cargo-mommy`. For more information check the section [why not `python-mommy`](#why-not-python-mommy).

# buttplug.io integration

I really want to integrate buttplug.io with [`buttplug-py`](https://github.com/Siege-Wizard/buttplug-py) into this project. This should make mommy support [buttplug.io](https://buttplug.io/). Unfortunately I am currently in a really bad place monetarily and don't own a device to test this on.

So if you want to see this implemented or just want to improve the day of a fellow trans girl, shoot me a mail at [acute_interpreter_panic@proton.me](mailto:acute_interpreter_panic@proton.me) and then you can buy me one. Of course I will update it once I got my hands on a... device

# Installation

You can `pip install python-mommy-venv`~

```sh
pip install python-mommy-venv
```

# Usage

## Concept you should know

If you work with python there are many things you might need hinder mommy from running explicitly. For example:

- installing a local project with the `-e` flag and running the generated command
- running any python module 
- installing a package with `pip`

They all have something in common, they call the python interpreter. So mommy's approach was to wrap the interpreter. However if mommy would do this globally, she would break many systems like Debian that rely on python~

So what mommy does, is patch the virtual environment you (hopefully) run the python packages you develop in. 

## Actually using the tool

You need to make sure `python-mommy-venv` is installed in your virtual environment. Else mommy can't find the directory to patch~ 

To patch the virtual env you can run the following command. Look at `mommify-venv -h` for more options.

```
mommify-venv  
```

Mommy will fetch the new responses from `cargo-mommy`, if you don't want her to you can turn it of.
She will then compile a config file with the parameters defined in the [configuration section](#configuration) and the fetched responses.

If you want to change the config, you can run, and mommy will recompile the config with the updated environment:

```
mommify-venv-compile
```

Here are examples of mommy responding to you~

```sh
$ pip install requests
Requirement already satisfied: requests in ./.venv/lib/python3.10/site-packages (2.32.4)
[...]

mommy loves you~

$ python test.py
Hello World

what a good girl you are~

$ python doesnt_exist.py .venv/bin/inner_python: can't open file 'doesnt_exist.py': [Errno 2] No such file or directory

don't forget to hydrate~
```

## Daddy

If you want mommy to call you daddy and never wanna touch mommy at all, then this program provides the following commands:

```sh
daddify-venv
daddify-venv-compile
```

This will set the default values to daddy instead of mommy, but will still be overwritten by config files or environment variables, if either of those are set.

The `--you` argument works the exact way, but you can tell mommy/daddy how to call you. The default is `girl`:

```
daddify-venv --you boy
```

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

`python-mommy` has to be explicitly run by running `python -m python_mommy test.py` which won't work in real life scenarios. Read the [concept section](#concept-you-should-know) if you want to know why.

`python-mommy` has many minor improvements that should be made. Those all aren't really bad but they add up.

`python-mommy` wasn't updated for one year. That means the responses are way to outdated, and also don't automatically update.

The last two reasons can be easily fixed, but the first one requires a complete rewrite.... which `python-mommy-venv` is.

# Licensing
mommy likes freedom~ ❤️, and is licensed under [MIT](LICENSE-MIT).
