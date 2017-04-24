#!/usr/bin/python3

"""
freqy.py

Calculates the frequency of ascii characters in a string, and compares it to
the frequency of characters in an English sentence.

https://en.wikipedia.org/wiki/Letter_frequency

According to Lewand, arranged from most to least common in appearance,
the letters are: 

    etaoinshrdlcumwfgypbvkjxqz 

Lewand's ordering differs slightly from others, such as Cornell University 
Math Explorer's Project, which produced a table after measuring 40,000 words.

In English, the space is slightly more frequent than the top letter (e) and 
the non-alphabetic characters (digits, punctuation, etc.) collectively occupy 
the fourth position (having already included the space) between t and a.

A simple way of testing two distributions can be found here:

https://en.wikipedia.org/wiki/Chi-squared_test
"""

from collections import Counter

expected_freq = {'e': 12.70,
                 't': 9.06,
                 'a': 8.17,
                 'o': 7.51,
                 'i': 6.97,
                 'n': 6.75,
                 's': 6.33,
                 'h': 6.09,
                 'r': 5.99,
                 'd': 4.25,
                 'l': 4.03,
                 'c': 2.78,
                 'u': 2.76,
                 'm': 2.41,
                 'w': 2.36,
                 'f': 2.23,
                 'g': 2.02,
                 'y': 1.97,
                 'p': 1.93,
                 'b': 1.29,
                 'v': 0.98,
                 'k': 0.77,
                 'j': 0.15,
                 'x': 0.15,
                 'q': 0.10,
                 'z': 0.07,
                 ' ': 19.7,}

def chi_squared(message):
    """Calculate the Chi-Squared statistic value.
    
    If the two distributions are identical, the chi-squared statistic is 0.
    If the two distributions are quite different, expect a higher number.

    X^2(C,E) = sum of (Ci - Ei)^2 / Ei, where i = A -> Z
    """
    c = Counter(message.lower())
    # Normalize the expected probabilities into counts
    e = { k: v * len(message) for k, v in expected_freq.items() }
    # penalise non ascii characters dramatically
    penalty = int(max(e.values())) ** 3
    # chi squared algo with penalty
    return sum(((c[i] - e[i])**2 / e[i]) if i in e else penalty for i in c)


if __name__ == "__main__":
    """Test the score of a random string."""
    test_strings = [ b'\\pptvqx?R\\8l?svtz?~?opjq{?py?}~|pq',
                     b'Q}}y{|u2_Q5a2~{yw2s2b}g|v2}t2psq}|',
                     b'Vzz~|{r5XV2f5y|~p5t5ez`{q5zs5wtvz{',
                     b'Txx|~yp7ZT0d7{~|r7v7gxbys7xq7uvtxy',
                     b'Kggcafo(EK/{(dacm(i(xg}fl(gn(jikgf',
                     b'Jffb`gn)DJ.z)e`bl)h)yf|gm)fo)khjfg',
                     b'Hdd`bel+FH,x+gb`n+j+{d~eo+dm+ijhde',
                     b'Nbbfdcj-@N*~-adfh-l-}bxci-bk-olnbc',
                     b'Maaeg`i.CM)}.bgek.o.~a{`j.ah.loma`',
                     b"Cooking MC's like a pound of bacon",
                     b'Bnnjhof!LB&r!mhjd!`!qntoe!ng!c`bno',
                     b'Ammikle"OA%q"nkig"c"rmwlf"md"`caml',
                     b'@llhjmd#N@$p#ojhf#b#slvmg#le#ab`lm',
                     b'Gkkomjc$IG#w$hmoa$e$tkqj`$kb$fegkj',
                     b'Fjjnlkb%HF"v%iln`%d%ujpka%jc%gdfjk',
                     b'Eiimoha&KE!u&jomc&g&vishb&i`&dgeih',
                     b"Dhhlni`'JD t'knlb'f'whric'ha'efdhi",]

    for test in test_strings:
        result = chi_squared(test.decode('utf-8'))
        print('{}: {}'.format(result, test))
