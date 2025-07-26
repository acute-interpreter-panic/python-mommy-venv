from enum import Enum

class Situation(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

RESPONSES = {
    "chill": {
        Situation.POSITIVE: [
            "*pets your head*",
            "*gives you scritches*",
            "you're such a smart cookie~",
            "that's a good MOMMYS_LITTLE~",
            "MOMMYS_ROLE thinks MOMMYS_PRONOUNS little MOMMYS_LITTLE earned a big hug~",
            "good MOMMYS_LITTLE~\nMOMMYS_ROLE's so proud of you~",
            "aww, what a good MOMMYS_LITTLE~\nMOMMYS_ROLE knew you could do it~",
            "you did it~!",
            "MOMMYS_ROLE loves you~",
            "*gives you a sticker*"
        ],
        Situation.NEGATIVE: [
            "MOMMYS_ROLE believes in you~",
            "don't forget to hydrate~",
            "aww, you'll get it next time~",
            "do you need MOMMYS_ROLE's help~?",
            "MOMMYS_ROLE still loves you no matter what~",
            "oh no did MOMMYS_ROLE's little MOMMYS_LITTLE make a big mess~?",
            "MOMMYS_ROLE knows MOMMYS_PRONOUNS little MOMMYS_LITTLE can do better~",
            "MOMMYS_ROLE still loves you~",
            "just a little further, sweetie~"
        ]
    },
    "thirsty": {
        Situation.POSITIVE: [
            "*tugs your leash*\nthat's a VERY good MOMMYS_LITTLE~",
            "*runs MOMMYS_PRONOUNS fingers through your hair* good MOMMYS_LITTLE~ keep going~",
            "*smooches your forehead*\ngood job~",
            "*nibbles on your ear*\nthat's right~\nkeep going~",
            "*pats your butt*\nthat's a good MOMMYS_LITTLE~",
            "*drags MOMMYS_PRONOUNS nail along your cheek*\nsuch a good MOMMYS_LITTLE~",
            "*bites MOMMYS_PRONOUNS lip*\nmhmm~",
            "give MOMMYS_PRONOUNS a kiss~",
            "*heavy breathing against your neck*"
        ],
        Situation.NEGATIVE: [
            "do you think you're going to get a reward from MOMMYS_ROLE like that~?",
            "*grabs your hair and pulls your head back*\nyou can do better than that for MOMMYS_ROLE can't you~?",
            "if you don't learn how to code better, MOMMYS_ROLE is going to put you in time-out~",
            "does MOMMYS_ROLE need to give MOMMYS_PRONOUNS little MOMMYS_LITTLE some special lessons~?",
            "you need to work harder to please MOMMYS_ROLE~",
            "gosh you must be flustered~",
            "are you just keysmashing now~?\ncute~",
            "is MOMMYS_ROLE's little MOMMYS_LITTLE having trouble reaching the keyboard~?"
        ]
    },
    "yikes": {
        Situation.POSITIVE: [
            "keep it up and MOMMYS_ROLE might let you cum you little MOMMYS_FUCKING~",
            "good MOMMYS_FUCKING~\nyou've earned five minutes with the buzzy wand~",
            "mmm~ come taste MOMMYS_ROLE's MOMMYS_PARTS~",
            "*slides MOMMYS_PRONOUNS finger in your mouth*\nthat's a good little MOMMYS_FUCKING~",
            "you're so good with your fingers~\nMOMMYS_ROLE knows where MOMMYS_PRONOUNS MOMMYS_FUCKING should put them next~",
            "MOMMYS_ROLE is getting hot~",
            "that's a good MOMMYS_FUCKING~",
            "yes~\nyes~~\nyes~~~",
            "MOMMYS_ROLE's going to keep MOMMYS_PRONOUNS good little MOMMYS_FUCKING~"
        ],
        Situation.NEGATIVE: [
            "you filthy MOMMYS_FUCKING~\nyou made a mess, now clean it up~\nwith your tongue~",
            "*picks you up by the throat*\npathetic~",
            "*drags MOMMYS_PRONOUNS claws down your back*\ndo it again~",
            "*brandishes MOMMYS_PRONOUNS paddle*\ndon't make me use this~",
            "MOMMYS_FUCKING.\nMOMMYS_FUCKING~\nMOMMYS_FUCKING~~",
            "get on your knees and beg MOMMYS_ROLE for forgiveness you MOMMYS_FUCKING~",
            "MOMMYS_ROLE doesn't think MOMMYS_PRONOUNS little MOMMYS_FUCKING should have permission to wear clothes anymore~",
            "never forget you belong to MOMMYS_ROLE~",
            "does MOMMYS_ROLE need to put you in the MOMMYS_FUCKING wiggler~?",
            "MOMMYS_ROLE is starting to wonder if you should just give up and become MOMMYS_PRONOUNS breeding stock~"
        ]
    }
}
