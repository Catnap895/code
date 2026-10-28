import ctypes
MB_OK = 0x0
run = False
ctypes.windll.user32.MessageBoxW(0, "You have been hacked by CozyFox! All your files have been encrypted. To recover your files, please contact CozyFox at hack@cozyfox.com", "CozyFox Alert", MB_OK)
if run == True:
    ctypes.windll.user32.MessageBoxW(0, """
╔══════════════════════════════════════════╗
║  🦊  Y O U R   F I L E S   H A V E  🦊   ║
║         B E E N   F O X E D !            ║
╚══════════════════════════════════════════╝

      /\   /\
     ( o.o )
      > ^ <
     /|     \
    (_|     |_)
      CUTE-RANSOM v1.0

GREETINGS HUMAN!

Your precious files have been gently booped
by the Fluffiest Fox in the Forest. 🦊

To recover your data, you must pay the ransom:

   🍗 3 (three) chicken nuggets
   🦴 1 (one) squeaky toy
   🐾 Unlimited belly rubs (lifetime)

All payments must be made in SnackCoin
or shiny objects. We also accept pets.

Failure to comply within 24 hours will result in:
   ❌ Continued fox noises
   ❌ Aggressive tail wags
   ❌ One (1) very smug expression

Your decryption key (it is love) is already
inside you. Or check /opt/snackcoin.

     — The Fluffy Fox Syndicate 🐾
       "We encrypt hearts. And docs.""", "CozyFox Alert", MB_OK)
